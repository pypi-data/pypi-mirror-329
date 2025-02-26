import collections
import time

import numpy as np
import psutil
from astropy import units as u
from astropy.time import Time
from twisted.logger import Logger


class RackPC(object):
    extra_rpc_calls = ()
    log = Logger()
    settable_attributes = ()
    extra_looping_calls = {"poll_stats": 10, "poll_net_usage": 20}
    telemetry_delay = 60

    def __init__(self, emulate=True):
        # no state machine needed
        self.machines = {}
        self.cpu_buffer = collections.deque(maxlen=10)
        self.mem_buffer = collections.deque(maxlen=10)
        self.net_buffer = collections.deque(maxlen=6)

    def poll_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        self.cpu_buffer.append(cpu)
        self.mem_buffer.append(mem)

    def poll_net_usage(self, intf="eth0"):
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[intf]
        net_in = net_stat.bytes_recv
        net_out = net_stat.bytes_sent
        self.net_buffer.append((time.time(), net_in, net_out))

    def telemetry(self):
        """
        Return telemetry data.
        """
        try:
            ts = Time.now()
            ts.format = "iso"
            tel_dict = dict(timestamp=ts)
            tel_dict["cpu"] = np.mean(self.cpu_buffer)
            tel_dict["mem"] = np.mean(self.mem_buffer)
            timestamps, net_in_values, net_out_values = list(zip(*self.net_buffer))
            bytes_in = np.diff(np.array(net_in_values)).mean() * u.byte
            bytes_out = np.diff(np.array(net_out_values)).mean() * u.byte
            mean_timestep = np.diff(np.array(timestamps)).mean() * u.second
            tel_dict["net_in"] = (bytes_in / mean_timestep).to_value(u.MB / u.s)
            tel_dict["net_out"] = (bytes_out / mean_timestep).to_value(u.MB / u.s)
        except Exception as e:
            self.log.warn("Failed to get RACK PC stats: {error}", error=e)
            tel_dict["cpu"] = None
            tel_dict["mem"] = None
            tel_dict["net_in"] = None
            tel_dict["net_out"] = None

        return tel_dict
