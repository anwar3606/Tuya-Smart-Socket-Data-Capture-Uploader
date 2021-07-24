import os
from pprint import pprint

import tinytuya


class TuyaSmartSocket:
    DP_NAMES = {
        "18": "current",
        "19": "power",
        "20": "voltage"
    }

    def __init__(self):
        self.device = tinytuya.OutletDevice(
            os.environ['TUYA_DEVICE_ID'],
            os.environ['TUYA_DEVICE_IP'],
            os.environ['TUYA_DEVICE_LOCAK_KEY'],
        )
        self.device.set_version(3.3)

    def get_data(self):
        self.device.updatedps()
        dps = self.device.status()['dps'].items()

        return {
            self.DP_NAMES[key]: value
            for key, value in dps
            if key in self.DP_NAMES
        }


if __name__ == '__main__':
    device = TuyaSmartSocket()
    pprint(device.get_data())
