import requests

class Fridge(object):
    """Keeps the brew intact."""

    max_load = 20

    def __init__(self, inverter, load=0, temp=8, base_speed=500):
        """Start chilling with factory settings."""

        if temp < 1:
            raise ValueError("Ice cream or beer Sir?")

        self.inverter = inverter
        self.load = load
        self.temp = temp
        self.base_speed = base_speed

    # Private method.
    def _fan_speed_factor(self):
        """Calculate fan speed adjustment for the load."""

        _fan_speed_factor = (self.max_load + self.load) / self.max_load

        return _fan_speed_factor

    # Answer an incoming query (from the display PCB).
    def get_fan_speed_setting(self):
        """Provide fan speed setting to the display PCB."""

        return self.base_speed * self._fan_speed_factor()

    # Perform an incoming command - change temperature.
    def set_temp(self, new_temp):
        """Set new target temperature."""

        self.temp = new_temp

    # Outgoing command - contact the inverter.
    def set_target_speed(self, target_speed):
        """Sets new fan target speed."""

        self.inverter.set_target_speed(target_speed)

        if self.get_current_speed() != target_speed:

            raise ValueError("Unable to confirm fan speed change.")

    # Outgoing query.
    def get_current_speed(self):
        """Contact inverter to get current fan speed."""

        return self.inverter.get_current_speed()

    # Contacting web based API.
    def order_beer(self, num_of_bottles):
        """Contact web based API to order more beer."""

        payload = {"num_bot": num_of_bottles,
                   "delivery_address": "my_fridge_obviously"}
        response = requests.post("https://get_more_beer.com", data=payload)

        if response.status_code == 200:

            return response

        else:

            return "incorrect_response: {0}".format(response.status_code)

