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
def mock_inverter(request):
    """Substitute our _inverter object with a fake one.
    Allows setting current speed to test multiple conditions."""

    current_speed = request.param

    _inverter = mock.Mock()
    _inverter.get_current_speed.return_value = current_speed

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


def test_get_temp(loaded_fridge):
    """Test getting temperature reading for the display PCB."""

    assert loaded_fridge.get_temp() == loaded_fridge.temp

test_data = [(1000, 1000), (1200, 1200), (1300, 1300), (1400, 1400)]
# Test outgoing command was sent out to the _inverter and a correct response
#  was received.
@pytest.mark.parametrize("mock_inverter, expected", test_data,
                         indirect=["mock_inverter"])
def test_set_target_speed(mock_inverter, expected):
    """Test behavior of fridge when current speed matches set speed."""

    fridge = Fridge(mock_inverter)
    fridge.set_target_speed(expected)

    mock_inverter.set_target_speed.assert_called_once_with(expected)


# Test outgoing command raises exception on incorrect response from _inverter.
@pytest.mark.parametrize("mock_inverter", [1000, 1200, 1300, 1400],
                         indirect=["mock_inverter"])
def test_raises_exception_if_curr_spd_not_target(mock_inverter):
    """Test behavior of fridge when current speed differs from set speed."""

    with pytest.raises(ValueError,
                       message="Unable to confirm fan speed change."):

        fridge = Fridge(mock_inverter)
        fridge.set_target_speed(1500)


class TestApiCalls(object):
    """Test contacting web based API."""

    URL = "https://get_more_beer.com"
    num_of_bottles = 20
    payload = {"num_bot": num_of_bottles,
               "delivery_address": "my_fridge_obviously"}
    reply = [{"order_status": "confirmed", "amount_ordered": num_of_bottles}]

    @pytest.fixture(scope="function")
    def mock_response_200(self):
        """Provide a substitute for web based API call."""

        mock_response = mock.Mock()
        mock_response.return_value.status_code = 200
        mock_response.return_value.json.return_value = self.reply

        return mock_response

    @pytest.fixture(scope="function")
    def mock_response_400(self):
        """Provide a substitute for web based API call."""

        mock_response = mock.Mock()
        mock_response.return_value.status_code = 400

        return mock_response

    # Test contacting external web based API with a response 200.
    def test_order_beer_response_200(self, loaded_fridge, mock_response_200, monkeypatch):
        """Test contacting web based API."""

        monkeypatch.setattr("fridge.requests.post", mock_response_200)

        loaded_fridge.order_beer(self.num_of_bottles)
        mock_response_200.assert_called_with(self.URL, data=self.payload)

        assert loaded_fridge.order_beer(self.num_of_bottles).json() == self.reply

    # Test contacting external web based API with a response 400.
    def test_order_beer_response_400(self, loaded_fridge, mock_response_400, monkeypatch):
        """Test contacting web based API."""

        monkeypatch.setattr("fridge.requests.post", mock_response_400)

        assert loaded_fridge.order_beer(self.num_of_bottles) == "incorrect_response: 400"
        mock_response_400.assert_called_with(self.URL, data=self.payload)


if __name__ == "__main__":
    pytest.main()

