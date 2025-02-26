# a model for GTC cooling status
from twisted.logger import Logger
from astropy.time import Time
import requests


class GTCCooler(object):
    extra_rpc_calls = ()
    log = Logger()
    settable_attributes = ()

    def __init__(self, emulate=True):
        self.telemetry_delay = 10
        self.emulate = emulate
        # no state machine needed
        self.machines = {}
        if self.emulate:
            self.temp_function = self.fake_temps
        else:
            self.temp_function = self.get_temps

    def get_temps(self):
        url = "http://161.72.18.76:1026/v2/entities/TemperatureSensor3"
        try:
            response = requests.get(
                url, headers={"fiware-service": "gtc", "fiware-servicePath": "/"}
            )
            response.raise_for_status()
            data = response.json()
            self.temps = [
                float(data["temperature1"]["value"]),
                float(data["temperature2"]["value"]),
                float(data["temperature3"]["value"]),
            ]
        except Exception as e:
            self.log.warn("Failed to get flow temperatures: {error}", error=e)
            self.temps = [None, None, None]
        return self.temps

    def fake_temps(self):
        return [12.3, 12.3, 5.0]

    def telemetry(self):
        ts = Time.now()
        ts.format = "iso"
        tel = dict(timestamp=ts)
        t1, t2, t3 = self.temp_function()
        tel["ccd_input"] = t3
        tel["cab_pre_filter"] = t2
        tel["cab_post_filter"] = t1
        tel["state"] = {}
        return tel
