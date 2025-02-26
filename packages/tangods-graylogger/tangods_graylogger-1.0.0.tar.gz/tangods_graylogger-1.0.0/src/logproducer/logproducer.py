from tango.server import Device, command
from tango import DevState

from functools import wraps


def log_exceptions(func):
    """This logs exceptions. Additionally it alters state and status.
    Finally, re-raises the exception, to be as transparent as possible.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            message = (
                f"Exception {type(e).__name__} in {func.__name__}, line "
                f"{e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
            self.error_stream(message)
            self.set_status(message)  # Additionally, change state/status
            self.set_state(DevState.FAULT)
            raise

    return wrapper


class LogProducer(Device):
    """A tango device that produces logs, using *_stream functions.

    There is also a wrapper that demonstrate a way of logging exceptions in
    a transparent way.
    """

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("All fine and dandy.")

    @command(dtype_in=int)
    def spam_error_stream(self, value):
        for i in range(value):
            self.error_stream(f"Error message {i} of {value}")

    @command
    def debug_message_test(self):
        self.debug_stream("Debug\ntest")

    @command
    def info_message_test(self):
        self.info_stream("Info\ntest")

    @command
    def warning_message_test(self):
        self.warn_stream("Warning\ntest")

    @command
    def error_message_test(self):
        self.error_stream("Error\ntest")

    @command
    def fatal_message_test(self):
        self.fatal_stream("Fatal\ntest")

    @command
    @log_exceptions
    def raise_exception(self):
        raise RuntimeError("Exception\ntest")


def main():
    LogProducer.run_server()


if __name__ == "__main__":
    main()
