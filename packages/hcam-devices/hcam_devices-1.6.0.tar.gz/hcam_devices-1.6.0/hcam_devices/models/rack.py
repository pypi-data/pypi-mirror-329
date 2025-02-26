# model for one thing only - temperature from Rack heat exchanger
import math

from astropy.time import Time
from twisted.logger import Logger

try:
    from ..gtc.corba import TelescopeServer
    from ..gtc.headers import create_header_from_telpars
except Exception:
    TelescopeServer = None


class FakeServer(object):
    def getCabinetTemperature1(self):
        return 20.0

    def getCabinetTemperature2(self):
        return 21.0

    def getCabinetTemperature3(self):
        return 22.0


class Rack(object):
    # add any extra methods you want exposed here
    extra_rpc_calls = ()
    log = Logger()
    settable_attributes = ()

    def __init__(self, emulate=True):
        print("emulation mode: ", emulate)
        self.emulate = emulate
        self.try_connect()

        # no state machine needed
        self.machines = {}

    def try_connect(self):
        try:
            if self.emulate:
                self._server = FakeServer()
            else:
                self._server = TelescopeServer()
        except:
            self._server = None
            return False
        return True

    def disconnect(self):
        self._server = None

    def get_dewpoint(self):
        """
        Get dewpoint from telescope parameters.
        """
        # relative humidity
        try:
            humidity = self._server.getHumidity()
            # use telescope tube temp as proxy for internal temp
            telpars = self._server.getTelescopeParams()
            hdr = create_header_from_telpars(telpars)
            temperature = float(hdr["T_TUBE"])
            # calculate dewpoint using Magnus-Tetens formula
            a = 17.625
            b = 243.04
            alpha = math.log(humidity / 100) + (a * temperature) / (b + temperature)
            val = (b * alpha) / (a - alpha)
        except:
            val = None
        return val

    def telemetry(self):
        """
        Called periodically to provide a telemetry package
        """
        ts = Time.now()
        ts.format = "iso"
        try:
            temp_top = self._server.getCabinetTemperature1()
            temp_middle = self._server.getCabinetTemperature2()
            temp_bottom = self._server.getCabinetTemperature3()
            dewpoint = self.get_dewpoint()
        except Exception as e:
            temp_bottom = None
            temp_middle = None
            temp_top = None
            dewpoint = None
            self.log.warn("Failed to get rack temperatures: {error}", error=e)
            self.try_connect()

        return dict(
            timestamp=ts,
            rack_temp_bottom=temp_bottom,
            rack_temp_middle=temp_middle,
            rack_temp_top=temp_top,
            dewpoint=dewpoint,
            state={},
        )
