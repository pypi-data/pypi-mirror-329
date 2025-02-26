import pytest
from unittest.mock import patch

from graylogger import Graylogger
from logproducer import LogProducer

from tango.test_context import DeviceTestContext

from tango import DevState


@pytest.fixture
def loggerProxy():
    logger_device = DeviceTestContext(
        Graylogger,
        process=True,
    )
    yield logger_device


@pytest.fixture
def producerProxy():
    producer_device = DeviceTestContext(
        LogProducer,
        process=True,
    )
    yield producer_device


# patch get_safe_devices because in the test environment
# there is no tango database to query
@patch("graylogger.graylogger.Database")
def testInitLogger(database, loggerProxy):
    """Test device goes into INIT when initialised"""
    with loggerProxy as proxy:
        assert proxy.status().startswith("On tango database")
        assert proxy.state() == DevState.ON


def testInitProd(producerProxy):
    """Test device goes into INIT when initialised"""
    with producerProxy as proxy:
        assert proxy.status().startswith("All fine and dandy")
        assert proxy.state() == DevState.ON
