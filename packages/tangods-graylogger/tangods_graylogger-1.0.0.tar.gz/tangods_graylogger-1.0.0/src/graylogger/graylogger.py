from tango.server import Device, device_property, attribute, command
from tango import Database, DeviceProxy, DevState
from requests import post, HTTPError
from datetime import datetime
import json

LEVEL_CONVERTER = {
    "DEBUG": 7,
    "INFO": 6,
    "WARN": 5,
    "ERROR": 4,
    "FATAL": 3,
}

TANGO_LEVELS_TO_INT = {
    "OFF": 0,
    "FATAL": 1,
    "ERROR": 2,
    "WARNING": 3,
    "INFO": 4,
    "DEBUG": 5,
}

# Assemble a dictionary that works both ways
TANGO_INT_TO_LEVELS = {}

for key, item in TANGO_LEVELS_TO_INT.items():
    TANGO_INT_TO_LEVELS[item] = key


NO_LOG_CLASSES = (
    # dserver
    "dserver",  # logging one of those in debug mode will create infinite loops
    # Sardana pool
    "Pool",
    "Controller",
    "Motor",
    "IORegister",
    "CTExpChannel",
    "ZeroDExpChannel",
    "OneDExpChannel",
    "TwoDExpChannel",
    "PseudoMotor",
    "PseudoCounter",
    "TriggerGate",
    "MotorGroup",
    "MeasurementGroup",
    # Sardana macroserver
    "MacroServer",
    "Door",
    # Jive temporary logconsumers
    "LogConsumer",
)


class Graylogger(Device):
    host = device_property(
        dtype=str,
        doc="Graylog host, logs are going to be sent to this address",
        default_value="localhost",
    )
    port = device_property(
        dtype=int,
        doc="Graylog port, logs are going to be sent through this port",
        default_value=12201,
    )
    timeout = device_property(
        dtype=float,
        doc="Timeout for HTTP posting of GELF messages",
        default_value=0.5,
    )

    # These will be evaluated at init
    first_init = True
    tango_db_host = None
    tango_db_port = None
    tangoDatabase = None
    graylog_url = None
    target_to_self = ""
    headers = {"Content-Type": "application/json"}

    _logged_messages = 0
    _failed_messages = 0
    last_log_received_time = "Never"

    logged_messages = attribute(
        dtype=int,
        label="Succesfully logged messages",
    )

    failed_messages = attribute(
        dtype=int,
        label="Failed loggings",
    )

    last_time_log = attribute(
        dtype=str,
        label="Last time log received",
    )

    def init_device(self):
        super().init_device()

        self.set_state(DevState.INIT)
        self.set_status("Initializing")

        # get tango database name and port
        try:
            self.tangoDatabase = Database()
            self.tango_db_host = self.tangoDatabase.get_db_host()
            self.tango_db_port = self.tangoDatabase.get_db_port_num()
            self.target_to_self = f"device::{self.get_name()}"
        except Exception as exc:
            self.set_state(DevState.FAULT)
            self.set_status(
                "Could not connect to tango database. " f"Exception was {exc}."
            )
            return

        # Graylog url and port
        self.graylog_url = f"http://{self.host}:{self.port}/gelf"

        self.last_log_received_time = (
            f"No message since init (at {datetime.now()})"
        )

        if not self.first_init:
            # The first time it has to be called from server_init_hook,
            # Otherwise the log producer will fail to connect to Graylogger
            self.reset_logging_targets()
            self.info_stream(f"Re-initialized {self.get_name()}")

        self.set_state(DevState.ON)
        self.set_status(
            f"On tango database {self.tango_db_host}:{self.tango_db_port}.\n"
            f"Ready to send to Graylog using {self.host}:{self.port}."
        )

    def server_init_hook(self):
        # This function is run only when the device is exported
        # (server started), not when calling additional init commands
        self.first_init = False
        self.reset_logging_targets()
        self.info_stream(f"First start of {self.get_name()}")

    def read_logged_messages(self):
        return self._logged_messages

    def read_failed_messages(self):
        return self._failed_messages

    def read_last_time_log(self):
        return self.last_log_received_time

    @command
    def reset_logging_targets(self):
        """Remove and adds Graylogger as a logging target for the
        devices that are configured to use Graylogger. This is
        needed when Graylogger is initialized, for threading reasons.
        """
        for dev in self.get_safe_devices():
            try:
                proxy = DeviceProxy(dev)
                log_property = proxy.get_property("logging_target")[
                    "logging_target"
                ]
                targets = proxy.get_logging_target()
            except Exception as exc:
                self.warn_stream(
                    f"Could not get logging target for device {dev}. "
                    f"Exception was {exc}."
                )
            else:
                if (
                    self.target_to_self in log_property
                    or self.target_to_self in targets
                ):
                    proxy.remove_logging_target(self.target_to_self)
                    proxy.add_logging_target(self.target_to_self)

    @command
    def acquire_logging_targets(self):
        """Add Graylogger as a logging target to all safe devices, regardless
        of their configuration.
        """
        for dev in self.get_safe_devices():
            try:
                proxy = DeviceProxy(dev)
            except Exception as exc:
                self.warn_stream(
                    f"Could not get logging target for device {dev}. "
                    f"Exception was {exc}."
                )
            else:
                proxy.add_logging_target(self.target_to_self)

    @command(
        dtype_in=str,
        doc_in=(
            "The desired logging level. Must be one of the following: DEBUG, "
            "INFO WARNING ERROR FATAL OFF. This level will be applied to all "
            "devices that are currently logging to Graylogger"
        ),
    )
    def impose_all_logging_levels(self, data):
        """Set logging level for all safe devices to the desired level,
        regardless of their configuration.
        """
        if data not in TANGO_LEVELS_TO_INT:
            raise ValueError(
                "Level must be one of those: "
                f"{list(TANGO_LEVELS_TO_INT.keys())}"
            )
        for dev in self.get_safe_devices():
            try:
                proxy = DeviceProxy(dev)
                targets = proxy.get_logging_target()
            except Exception as exc:
                self.warn_stream(
                    f"Could not get logging target for device {dev}. "
                    f"Exception was {exc}."
                )
            else:
                if self.target_to_self in targets:
                    proxy.set_logging_level(TANGO_LEVELS_TO_INT[data])

    @command(
        dtype_in=str,
        doc_in=(
            "The desired logging level to use if one is not defined in the"
            "device property. Use IGNORE to ignore the devices that do not "
            "Have a property defined. Otherwise, choose one "
            "from the following: DEBUG, INFO WARNING ERROR FATAL OFF. "
            "This level will be applied to all devices that are currently "
            "logging to Graylogger, or configured to do so."
        ),
    )
    def impose_logging_levels_from_property(self, data):
        if data != "IGNORE" and data not in TANGO_LEVELS_TO_INT:
            raise ValueError(
                "Level must be one of those: 'IGNORE' or "
                f"{list(TANGO_LEVELS_TO_INT.keys())}"
            )
        for dev in self.get_safe_devices():
            try:
                proxy = DeviceProxy(dev)
                targets = proxy.get_logging_target()
                log_level = proxy.get_property("logging_level")[
                    "logging_level"
                ]
                log_targets = proxy.get_property("logging_target")[
                    "logging_target"
                ]
                if log_level and log_level[0]:
                    value = TANGO_LEVELS_TO_INT[log_level[0]]
                elif data != "IGNORE":
                    value = TANGO_LEVELS_TO_INT[data]
                else:
                    value = None
            except Exception as exc:
                self.warn_stream(
                    f"Could not get logging target for device {dev}. "
                    f"Exception was {exc}."
                )
            else:
                if value is not None and (
                    self.target_to_self in targets
                    or self.target_to_self in log_targets
                ):
                    proxy.set_logging_level(value)

    @command(
        dtype_out=str,
        doc_out="Logging status report of all safe devices.",
    )
    def status_report(self):
        """Returns a text detailing the status of logging for all devices
        that are exported and considered 'safe devices' for logging.
        For the definition of 'safe devices' please refer to the Graylogger
        documentation.
        """
        report = "--- Device logging report"
        for dev in self.get_safe_devices():
            try:
                proxy = DeviceProxy(dev)
                log_property = proxy.get_property("logging_target")[
                    "logging_target"
                ]
                log_level_property = proxy.get_property("logging_level")[
                    "logging_level"
                ]
                targets = proxy.get_logging_target()
                level = proxy.get_logging_level()
            except Exception as exc:
                report = (
                    f"{report}\nCould not get info for device {dev}."
                    f"\nException was {exc}."
                )
            else:
                report = (
                    f"{report}\n{dev} logging_target property: {log_property}"
                )
                report = (
                    f"{report}\n{dev} logging_level property: "
                    f"{log_level_property}"
                )
                report = f"{report}\n{dev} current logging targets: {targets}"
                report = (
                    f"{report}\n{dev} current logging level: "
                    f"{TANGO_INT_TO_LEVELS[level]}"
                )
        report = f"{report}\n--- End of report"
        return report

    def get_safe_devices(self):
        """Queries the database and returns a list of tango devices that are
        valid and safe log producers.

        The exclusions are defined in NO_LOG_CLASSES
        """

        results = []

        no_log_devices = []
        for cl in NO_LOG_CLASSES:
            no_log_devices += list(
                self.tangoDatabase.get_device_exported_for_class(cl)
            )

        for dev in list(self.tangoDatabase.get_device_exported("*")):
            if dev not in no_log_devices:
                try:
                    proxy = DeviceProxy(dev)
                    proxy.ping()
                    results.append(dev)
                except Exception:
                    # ignore unreachable
                    pass

        return results

    @command(dtype_in=[str])
    def Log(self, data):
        """This is the function that tango invokes when you set a device as a
        logging target. The name MUST be 'Log' and dtype_in MUST be a list
        of strings.

        Content of this list is:
        data[0] timestamp in unix time, in milliseconds
        data[1] tango debug level, example 'DEBUG'
        data[2] tango device name where the log originated example 'my/dev/1'
        data[3] log message
        data[4] NDC (contextual info), not implemented
        data[5] thread identifier
        """
        # Update last received
        self.last_log_received_time = str(datetime.now())

        graylog_message = {
            "version": "1.1",
            "host": (
                f"tango://{self.tango_db_host}:{self.tango_db_port}/"
                f"{data[2]}"
            ),
            "short_message": data[3],
            "timestamp": float(data[0]) * 1e-3,  # ms to s
            "level": LEVEL_CONVERTER[data[1]],
            "_tango_log_NDC": data[4],
            "_tango_thread_identifier": data[5],
        }
        data = json.dumps(graylog_message)

        try:
            response = post(
                self.graylog_url,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
            )
        except Exception as exc:
            self._failed_messages += 1
            self.set_state(DevState.FAULT)
            msg = f"Could not log {data}, exception was {exc}"
            self.set_status(msg)
            return
        if response.status_code != 202:  # Graylog always answer 202
            try:
                response.raise_for_status()  # actual http error like 500
            except HTTPError as exc:
                self._failed_messages += 1
                self.set_state(DevState.FAULT)
                msg = f"Could not log {data}, exception was {exc}"
                self.set_status(msg)
        else:
            self._logged_messages += 1
            self.set_state(DevState.RUNNING)
            self.set_status("Logging running.")


def main():
    Graylogger.run_server()


if __name__ == "__main__":
    main()
