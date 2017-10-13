class Fridge(object):
    """Keeps the brew intact."""

    max_load = 20

    def __init__(self, load=0, temp=8, base_speed=500, inverter=None):
        """Start chilling with factory settings."""

        if not inverter:

            raise ValueError("Inverter parameter must be set.")

        self.load = load
        self.temp = temp
        self.base_speed = base_speed
        self.inverter = inverter

    # Private method.
    def _fan_speed_factor(self):
        """Calculate fan speed adjustment for the load."""

        _fan_speed_factor = (self.max_load + self.load)/self.max_load

        return _fan_speed_factor

    # Answer an incoming query (from the display PCB).
    def get_fan_speed_setting(self):
        """Provide fan speed setting to the display PCB."""

        return self.base_speed*self._fan_speed_factor()

    # Perform an incoming command - change temperature.
    def set_temp(self, new_temp):
        """Set new target temperature."""

        self.temp = new_temp



