# COMPO components
import pickle
import astropy.units as u
from astropy.time import Time
import traceback
from twisted.logger import Logger

from ..devices.properties import microstep
from ..devices.newport import NewportESP301
from .slide import LinearStage
from ..machines import create_machine


MIN_MS = 0
MAX_MS = 1049869  # 25 mm travel
MM_PER_MS = 2.38125e-05
MIN_MM = MM_PER_MS * MIN_MS
MAX_MM = MM_PER_MS * MAX_MS


def mm_to_ms(value):
    return MIN_MS + int((MAX_MS - MIN_MS) * (value - MIN_MM) / (MAX_MM - MIN_MM) + 0.5)


def ms_to_mm(value):
    return MIN_MM + (MAX_MM - MIN_MM) * (value - MIN_MS) / (MAX_MS - MIN_MS)


equivalencies = [
    # from, to, forward, backward (assume 1-1 for now)
    (u.rad, microstep, lambda x: x, lambda x: x),
    (u.mm, microstep, mm_to_ms, ms_to_mm),
]

# match order in NewportESP301
esp_axes = {1: "pickoff", 2: "injection"}


class Compo(object):
    """
    Model for COMPO.

    COMPO contains a linear stage and two rotational arms. Each of
    these have their own hardware model. This is a convenience model
    that listens to, and forwards, telemetry from these bits of kit.

    The correct topics to subscribe to are passed as parameters.
    """

    log = Logger()

    def __init__(self, arm_channel, lens_channel):
        # we subscribe to telemetry on these channels
        self.subscribed_channels = {"lens": lens_channel, "arms": arm_channel}
        # pass through topics merely pass any published messages
        # on to a different topic
        self.pass_through_topics = {
            "target_injection_angle": f"{arm_channel}.target_injection_angle",
            "target_pickoff_angle": f"{arm_channel}.target_pickoff_angle",
            "target_lens_position": f"{lens_channel}.target_position",
        }

        self._telemetry_timestamps = {"lens": Time.now(), "arms": Time.now()}

        # this is the basic package we publish as telemetry
        self._telemetry_pkg = {
            "state": {"arms_state": "", "lens_state": ""},
            "pickoff_angle": {"target": 0, "current": 0},
            "injection_angle": {"target": 0, "current": 0},
            "lens_position": {"target": 0, "current": 0},
        }

    def on_received_telemetry(self, data):
        """
        Handle telemetry data. Could come from any
        subscribed topics
        """
        telemetry = pickle.loads(data)
        telemetry_time = telemetry["timestamp"]
        device_status = telemetry["state"]["connection"]

        if "pickoff_angle" in telemetry:
            source = "arms"
        elif "position":
            source = "lens"
        else:
            raise ValueError("unexpected telemetry pkg: ", telemetry)
        self._telemetry_timestamps[source] = telemetry_time

        if source == "arms":
            # set telemetry package for arms
            self._telemetry_pkg["state"]["arms_state"] = telemetry["state"]
            self._telemetry_pkg["pickoff_angle"] = telemetry["pickoff_angle"]
            self._telemetry_pkg["injection_angle"] = telemetry["injection_angle"]
        else:
            self._telemetry_pkg["state"]["lens_state"] = telemetry["state"]
            self._telemetry_pkg["lens_position"] = telemetry["position"]

    def telemetry(self):
        # use stalest timestamp we have as the data timestamp
        oldest_ts = min(self._telemetry_timestamps, key=self._telemetry_timestamps.get)
        tel = dict(timestamp=self._telemetry_timestamps[oldest_ts])
        tel.update(self._telemetry_pkg)
        return tel


class CompoLens(LinearStage):
    """
    COMPO contins a Zaber linear stage which controls the lens.
    """

    def __init__(self, ip_address, port, emulate=True):
        super().__init__(ip_address, port, equivalencies, emulate)
        self.natural_units = u.mm

        # override the maximum position to avoid querying it, which is unreliable
        self.dev.max_position = 1049869


class CompoArms(object):
    """
    Model for COMPO rotational arms.

    COMPO is controlled by a Newport ESP301 controller, which has 3 axes.
    The first 2 axes are the angles of the pickoff arm and injection arm.
    """

    log = Logger()

    # can be set by publishing to a device level topic of same name
    settable_attributes = ("target_injection_angle", "target_pickoff_angle")

    # all state change triggers are automatically addded as RPC calls
    # add any extra methods you want exposed here
    extra_rpc_calls = ("power_on_axis", "power_off_axis")

    def __init__(self, esp_port, emulate=False):
        self.esp = NewportESP301(
            esp_port, emulate=emulate, unit_equivalencies=equivalencies
        )

        # state machines to track state. Controller for connections
        self._controller = create_machine(
            "connections", initial_context={"device": self, "name": "compo"}
        )
        self.machines = dict(connection=self._controller)

        # newport axes!
        # ORDER HERE MUST MATCH ORDER IN Newport!
        for ax in esp_axes:
            name = esp_axes[ax]
            ctx = {
                "device": self.esp.axis[ax - 1],
                "current": 0 * u.mm if name == "lens" else 0 * u.deg,
                "target": 0 * u.mm if name == "lens" else 0 * u.deg,
                "poll_time": 2,
            }
            axis = create_machine("motors", initial_context=ctx)
            self.machines[name] = axis
            # bind axes to receive connect disconnect from controller
            self._controller.bind(axis)

    @property
    def current_injection_angle(self):
        return self.machines["injection"].context["current"]

    @property
    def target_injection_angle(self):
        return self.machines["injection"].context["target"]

    @target_injection_angle.setter
    def target_injection_angle(self, value):
        print("setting injection angle")
        if not isinstance(value, u.Quantity):
            value = value * u.deg
        self.machines["injection"].queue("positionSet", position=value)

    @property
    def current_pickoff_angle(self):
        return self.machines["pickoff"].context["current"]

    @property
    def target_pickoff_angle(self):
        return self.machines["pickoff"].context["target"]

    @target_pickoff_angle.setter
    def target_pickoff_angle(self, value):
        if not isinstance(value, u.Quantity):
            value = value * u.deg
        self.machines["pickoff"].queue("positionSet", position=value)

    def telemetry(self):
        """
        Called periodically to provide a telemetry package for the device
        """
        ts = Time.now()
        tel = dict(timestamp=ts)
        state = {key: self.machines[key].configuration for key in self.machines}
        tel["state"] = state
        tel["pickoff_angle"] = dict(
            current=self.current_pickoff_angle, target=self.target_pickoff_angle
        )
        tel["injection_angle"] = dict(
            current=self.current_injection_angle, target=self.target_injection_angle
        )
        return tel

    # Methods REQUIRED for controller state machine
    def try_connect(self):
        try:
            # connect to newport
            self.esp.connect()
            # update device in state machines for arms
            for ax in esp_axes:
                name = esp_axes[ax]
                machine = self.machines[name]
                axis = self.esp.axis[ax - 1]
                axis.power_on()
                machine.context["device"] = axis
        except Exception as err:
            print(traceback.format_exc())
            return False
        return True

    def disconnect(self):
        self.esp.disconnect()

    # additional RPC calls
    def power_on_axis(self, axis):
        self.esp.axis[axis].power_on()

    def power_off_axis(self, axis):
        self.esp.axis[axis].power_off()
