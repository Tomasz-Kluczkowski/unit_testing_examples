import pytest

from unittest import mock
from fridge import Fridge


# Scope argument in fixture allows running it once per event.
# function (default), module, class, session as argument are allowed.
# autouse=True runs the fixture after launching tests automatically without
# having to "use it up" in a test.
@pytest.fixture(scope="function")
def loaded_fridge():
    """Create Fridge object for testing."""

    _fridge = Fridge("INV4403PH", load=10, temp=10, base_speed=1000)

    return _fridge


# This fixture allows parametrizing it from the test.
@pytest.fixture(scope="function")
def loaded_fridge_param(request):
    """Create Fridge object for testing with adjustable attributes."""

    inverter, load, temp, base_speed = request.param

    _fridge = Fridge(inverter, load, temp, base_speed)

    return _fridge


@pytest.fixture(scope="function")
def mock_inverter():
    """Substitute our _inverter object with a fake one."""

    _inverter = mock.Mock()

    return _inverter


# We will prove later on that thanks to indirect testing we can get rid of this
# test function altogether.
def test_instantiation(loaded_fridge):
    """Test initialization of the Fridge class."""

    assert loaded_fridge.load == 10
    assert loaded_fridge.temp == 10


def test_raises_exception_when_temp_too_low():
    """Checks if exception is raised if Fridge class is instantiated with temp
    below 1."""

    with pytest.raises(ValueError, message="Ice cream or beer Sir?"):

        wrong_temp_fridge = Fridge("INV2401PH", temp=0)


# Test incoming query - notice that due to dependency on calculation in
# _fan_speed_factor we test 2 methods at the same time with just one test.
def test_get_fan_speed_setting(loaded_fridge):
    """Test correct adjustment to the fan speed."""

    assert loaded_fridge.get_fan_speed_setting() == 1500


# ((_inverter, load, temp, _base_speed), expected fan_speed_setting)
fridge_parameters = [(("INV2401PH", 0, 5, 500), 500),
                     (("INV2403PH", 5, 2, 100), 125),
                     (("INV4401PH", 15, 15, 700), 1225),
                     (("INV4403PH", 3, 9, 300), 345)]


# Indirect parametrization - passing arguments to fixtures.
@pytest.mark.parametrize("loaded_fridge_param, expected", fridge_parameters,
                         indirect=["loaded_fridge_param"])
def test_get_fan_speed_setting_multiple(loaded_fridge_param, expected):
    """Test initialization of the Fridge class."""

    assert loaded_fridge_param.get_fan_speed_setting() == expected


temp_data = [(10, 10),
             (8, 8),
             (14, 14),
             (6, 6)]


# Simple parametrization of test variables.
# Test an incoming command (from the display PCB).
@pytest.mark.parametrize("test_temp, expected", temp_data)
def test_set_temp(loaded_fridge, test_temp, expected):
    """Test correct setting of the target temperature."""

    loaded_fridge.set_temp(test_temp)

    assert loaded_fridge.temp == expected


# def test_get_temp(loaded_fridge):
#     """Test getting temperature reading for the display PCB."""
#
#     assert loaded_fridge.get_temp() == loaded_fridge.temp
#
#
# Test outgoing command was sent out to the _inverter with correct a parameter.
def test_set_target_speed(mock_inverter):
    """Test outgoing command called with correct parameter."""

    fridge = Fridge(mock_inverter)
    fridge.set_target_speed(1000)

    mock_inverter.set_target_speed.assert_called_once_with(1000)


if __name__ == "__main__":
    pytest.main()

