class Fridge(object):
    """Keeps the brew intact."""

    max_load = 20

    def __init__(self, inverter, load=0, temp=8, base_speed=500):
        """Start chilling with factory settings."""

        self.load = load
        self.temp = temp
        self._inverter = inverter
        self._base_speed = base_speed

    # Answer an incoming query (from the display PCB).
    def get_temp(self):
        """Provide temperature reading for the display PCB."""

        return self.temp

    # Private method.
    def _fan_speed_factor(self):
        """Calculate fan speed factor for the load."""

        _fan_speed_factor = (self.max_load + self.load) / self.max_load
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        return _fan_speed_factor

    # Answer an incoming query (from the display PCB).
    def get_fan_speed_setting(self):
        """Provide fan speed setting to the display PCB."""

        return self._base_speed * self._fan_speed_factor()

    # Perform an incoming command - change the temperature.
    def set_temp(self, new_temp):
        """Set new target temperature."""

        if new_temp < 1:
            raise ValueError("Ice cream or beer Sir?")

        self.temp = new_temp

    # Outgoing command - contact the _inverter.
    def set_target_speed(self, target_speed):
        """Sets new fan target speed."""

        self._inverter.set_target_speed(target_speed)
