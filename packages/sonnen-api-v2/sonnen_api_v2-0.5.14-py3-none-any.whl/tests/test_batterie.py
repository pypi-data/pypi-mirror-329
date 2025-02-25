"""pytest tests/test_batterie.py -s -v -x
3. Sync update called from sync method
"""
import logging
import pytest
from freezegun import freeze_time
import responses
from sonnen_api_v2 import Batterie

from .battery_charging_sync import fixture_battery_charging

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@responses.activate
@pytest.mark.usefixtures("battery_charging")
@freeze_time("20-11-2023 17:00:00")
def test_sync_methods(battery_charging: Batterie) -> None:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen utility methods test suite.')

    assert battery_charging.charging > 0
    assert battery_charging.discharging == 0

    led_state =  battery_charging.led_xlate_state(
                {
                    "Blinking Red":False,
                    "Brightness":'100',
                    "Pulsing Green":False,
                    "Pulsing Orange":True,
                    "Pulsing White":False,
                    "Solid Red":'false'
                }
            )
    assert led_state == "Pulsing Orange 100%"
    assert battery_charging.led_state == "Pulsing White 100%"

    led_state_text =  battery_charging.led_xlate_state_text(
                {
                    "Blinking Red":False,
                    "Brightness":'100',
                    "Pulsing Green":True,
                    "Pulsing Orange":False,
                    "Pulsing White":False,
                    "Solid Red":'false'
                }
            )
    assert led_state_text == "Off Grid."
    assert battery_charging.led_state_text == "Normal Operation."
