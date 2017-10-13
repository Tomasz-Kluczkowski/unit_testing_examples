import pytest

from unittest import mock
from fridge import Fridge


# Scope argument in fixture allows running it once per event.
# function, module, class, session as argument are allowed.
# autouse=True runs the fixture after launching tests automatically without
# having to "use it up" in a test.
@pytest.fixture(scope="module")
def loaded_fridge():
    """Create Fridge object for testing."""

    _fridge = Fridge(load=10, temp=10, base_speed=1000, inverter="Inverter")

    return _fridge


@pytest.fixture(scope="function")
def mock_inverter(current_speed):
    """Substitute our inverter object with a fake one.
    Allows setting current speed to test multiple conditions."""

    _inverter = mock.Mock()
    _inverter.get_current_speed.side_effect = [current_speed]

    return _inverter


def test_instantiation(loaded_fridge):
    """Test initialization of the Fridge class."""

    assert loaded_fridge.load == 10
    assert loaded_fridge.temp == 10
    assert loaded_fridge.base_speed == 1000
    assert loaded_fridge.inverter == "Inverter"


def test_raises_exception_if_no_inverter_parameter_set():
    """Checks if exception is raised if Fridge class is instantiated with no
    inverter parameter."""

    with pytest.raises(ValueError, message="Inverter parameter must be set."):

        no_inverter_fridge = Fridge()


# Test incoming query - notice that due to dependency on calculation in
# _fan_speed_factor we test 2 methods at the same time with just one test.
def test_get_fan_speed_setting(loaded_fridge):
    """Test correct adjustment to the fan speed."""

    assert loaded_fridge.get_fan_speed_setting() == 1500


# Test an incoming command (from the display PCB).
def test_set_temp(loaded_fridge):
    """Test correct setting of the target temperature."""

    loaded_fridge.set_temp(3)

    assert loaded_fridge.temp == 3


# # Test outgoing command with a correct response from dependencies.
# def test_set_target_speed(loaded_fridge, mock_inverter):
#     """Test behavior of fridge when current speed matches set speed."""
#
#     inverter = mock_inverter
#     loaded_fridge.set_target_speed(1200)







if __name__ == "__main__":
    pytest.main()

