# model for GPS status
from __future__ import print_function, division, unicode_literals

try:
    from subprocess import getoutput
except:
    from commands import getoutput
import os
import getpass
import warnings
import re
from twisted.logger import Logger

from astropy.time import Time

path_to_examples = "/home/{}/hipercam-gps/tsync/examples".format(getpass.getuser())


def convert(val, to_type):
    return to_type(val.split(":")[1].strip())


class GPSCall(object):
    def __init__(self, function):
        """
        Class to call a GPS function.

        Parameters
        ----------
        function: string
            Name of function to call (must be one of the example programs
            in the TSYNC library). Should include arguments
        """
        self.function = os.path.join(path_to_examples, function)

    def _check(self, response):
        """
        Implement this function to parse results of running function.

        response: string
            response from function call
        """
        if "Could not open" in response:
            raise IOError("could not open GPS device")
        if "Error" in response:
            raise IOError("error in function call:\n" + str(response))
        if "error closing" in response:
            warnings.warn("could not properly close device")

    def __call__(self):
        response = getoutput(self.function)
        self._check(response)
        return self._parse(response)


class GetNumSats(GPSCall):
    def __init__(self):
        super(GetNumSats, self).__init__("GetSatInfo 0")

    def _parse(self, response):
        response = response.strip()
        pattern = "Number of satellites tracked:\s+(\d*)"
        match = re.search(pattern, response)
        if match is None:
            raise IOError("could not parse GPS response: " + response)
        nsats = int(match.group(1))
        return nsats


class GetValidity(GPSCall):
    """
    Validity of GPS signal on time and PPS output
    """

    def __init__(self):
        super(GetValidity, self).__init__("GR_GetValidity 0 0")

    def _parse(self, response):
        time_valid, pps_valid = (
            bool(convert(val, int)) for val in response.splitlines()[2:4]
        )
        return time_valid, pps_valid


class HWTime(GPSCall):
    def __init__(self):
        super(HWTime, self).__init__("HW_GetTime 0")

    def _parse(self, response):
        year, doy, hr, mins, sec, nsec = (
            convert(val, int) for val in response.splitlines()[2:8]
        )
        time_string = "{}:{}:{}:{}:{:.6f}".format(year, doy, hr, mins, sec + nsec / 1e9)
        timestamp = Time(time_string, format="yday")
        synced = response.splitlines()[-1].split(":")[1].strip()
        # Convert to boolean
        synced = True if synced.upper() == "TRUE" else False
        return timestamp, synced


class GPSDevice(object):
    def __init__(self):
        self.get_num_sats = GetNumSats()
        self.get_validity = GetValidity()
        self.get_hw_time = HWTime()

    def telemetry(self):
        tel = dict()
        tel["num_sats"] = self.get_num_sats()
        tel["time_valid"], tel["pps_valid"] = self.get_validity()
        ts, synced = self.get_hw_time()
        ts.format = "iso"
        tel["timestamp"] = ts
        tel["synced"] = synced
        tel["state"] = {}
        return tel


class FakeGPSDevice(object):
    def telemetry(self):
        ts = Time.now()
        ts.format = "iso"
        return dict(
            num_sats=10,
            time_valid=True,
            pps_valid=True,
            timestamp=ts,
            state={},
            synced=True,
        )


class GPS(object):
    extra_rpc_calls = ()
    log = Logger()
    settable_attributes = ()

    def __init__(self, emulate=True):
        self.telemetry_delay = 10
        self.emulate = emulate
        # no state machine needed
        self.machines = {}
        if self.emulate:
            self.device = FakeGPSDevice()
        else:
            self.device = GPSDevice()

    def telemetry(self):
        return self.device.telemetry()
