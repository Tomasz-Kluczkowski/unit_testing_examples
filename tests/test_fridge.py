import pytest

from unittest import mock
from fridge import Fridge


# Scope argument in fixture allows running it once per event.
# function (default), module, class, session as argument are allowed.
# autouse=True runs the fixture after launching tests automatically without
# having to "use it up" in a test (and it obeys the scope rules).
@pytest.fixture(scope="function")
def loaded_fridge():
    """Create Fridge object for testing."""

    _fridge = Fridge("INV4403PH", load=10, temp=10, base_speed=1000)

    return _fridge


@pytest.fixture(scope="function")
def mock_inverter():
    """Substitute our _inverter object with a fake one."""

    _inverter = mock.Mock()

    return _inverter


# Test incoming query.
def test_get_temp(loaded_fridge):
    """Test getting temperature reading for the display PCB."""

    assert loaded_fridge.get_temp() == loaded_fridge.temp


# Test incoming query - notice that due to dependency on calculation in
# _fan_speed_factor we test our private method indirectly and can skip writing
# a separate test for it.
def test_get_fan_speed_setting(loaded_fridge):
    """Test correct adjustment to the fan speed."""

    assert loaded_fridge.get_fan_speed_setting() == 1500


# Test an incoming command (from the display PCB).
def test_set_temp(loaded_fridge):
    """Test correct setting of the target temperature."""

    loaded_fridge.set_temp(5)

    assert loaded_fridge.temp == 5


# Test raising an exception on incorrect temp.
def test_raises_exception_when_temp_too_low(loaded_fridge):
    """Test if method raises an exception when temp set < 1."""

    with pytest.raises(ValueError) as info:

        loaded_fridge.set_temp(-10)
    assert str(info.value) == "Ice cream or beer Sir?"


# Test outgoing command was sent out to the inverter with a correct parameter.
def test_set_target_speed(mock_inverter):
    """Test outgoing command called with correct parameter."""

    fridge = Fridge(mock_inverter)
    fridge.set_target_speed(1000)

    mock_inverter.set_target_speed.assert_called_once_with(1000)


def test_check(loaded_fridge):

    assert loaded_fridge.check_some() is None


if __name__ == "__main__":
    pytest.main()

