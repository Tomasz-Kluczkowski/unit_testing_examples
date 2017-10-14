# import pytest
#
# from unittest import mock
# from fridge import Fridge
#
#
# # Scope argument in fixture allows running it once per event.
# # function, module, class, session as argument are allowed.
# # autouse=True runs the fixture after launching tests automatically without
# # having to "use it up" in a test.
# @pytest.fixture(scope="module")
# def loaded_fridge():
#     """Create Fridge object for testing."""
#
#     _fridge = Fridge(load=10, temp=10, base_speed=1000, inverter="Inverter")
#
#     return _fridge
#
#
# @pytest.fixture(scope="module")
# def loaded_fridge_param(request):
#     """Create Fridge object for testing, able to add inverter parameter."""
#
#     load, temp, base_speed, inverter = request.param
#
#     _fridge = Fridge(load=load, temp=temp, base_speed=base_speed,
#                      inverter=inverter)
#
#     return _fridge
#
#
# # (load, temp, base_speed, inverter_type, fan_speed_setting)
# fridge_parameters = [((0, 5, 500, "INV2401PH"), 500),
#                      ((5, 0, 100, "INV2403PH"), 125),
#                      ((15, 15, 700, "INV4401PH"), 1225),
#                      ((3, 9, 300, "INV4403PH"), 345)]
#
#
# # Experiment with indirect
# @pytest.mark.parametrize("loaded_fridge_param, expected", fridge_parameters,
#                          indirect=["loaded_fridge_param"])
# def test_instantiation_multiple(loaded_fridge_param, expected):
#     """Test initialization of the Fridge class."""
#
#     assert loaded_fridge_param.get_fan_speed_setting() == expected
#
# if __name__ == "__main__":
#     pytest.main()
#
