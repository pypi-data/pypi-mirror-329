from typing import Any

from ..models.ccd import CCDHead
from ..models.compo import Compo, CompoArms, CompoLens
from ..models.flow_sensor import FlowSensor
from ..models.gps import GPS
from ..models.gtc_cooling import GTCCooler
from ..models.meerstetter import Meerstetter
from ..models.ngc import NGC
from ..models.rack import Rack
from ..models.rackpc import RackPC
from ..models.slide import FocalPlaneSlide
from ..models.telescope import GTC
from ..models.vac_gauge import VacGauge
from ..wamp import ModelComponentMixin, WrapperComponentMixin


class RackPCComponent(ModelComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        super(RackPCComponent, self).__init__(config)
        self.traceback_app = True
        emulation_mode = config.extra.get("emulate")
        self.model = RackPC(emulate=emulation_mode)


class GTCCoolingComponent(ModelComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        super(GTCCoolingComponent, self).__init__(config)
        self.traceback_app = True
        emulation_mode = config.extra.get("emulate")
        self.model = GTCCooler(emulate=emulation_mode)


class GPSComponent(ModelComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        super(GPSComponent, self).__init__(config)
        self.traceback_app = True
        emulation_mode = config.extra.get("emulate")
        self.model = GPS(emulate=emulation_mode)


class RackComponent(ModelComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        super(RackComponent, self).__init__(config)
        self.traceback_app = True
        emulation_mode = config.extra.get("emulate")
        self.model = Rack(emulate=emulation_mode)


class GTCComponent(ModelComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        super(GTCComponent, self).__init__(config)
        self.traceback_app = True
        emulation_mode = config.extra.get("emulate")
        path = config.extra.get("path", "/data")
        self.model = GTC(emulate=emulation_mode, path=path)


class NGCComponent(ModelComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        super(NGCComponent, self).__init__(config)
        self.traceback_app = True
        emulation_mode = config.extra.get("emulate")
        self.model = NGC(emulation_mode)


class CCDComponent(WrapperComponentMixin):
    def __init__(self, config):
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        pressure_topic = config.extra.get("pressure_topic")
        flow_topic = "hipercam.flow"
        peltier_topic = config.extra.get("peltier_topic")
        pen_number = config.extra.get("pen_number")
        peltier_channel = config.extra.get("peltier_channel")

        super(CCDComponent, self).__init__(config)
        self.traceback_app = True
        self.model = CCDHead(
            pressure_topic, flow_topic, peltier_topic, pen_number, peltier_channel
        )


class PressureComponent(ModelComponentMixin):
    def __init__(self, config):
        super(PressureComponent, self).__init__(config)
        self.traceback_app = True
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        host = config.extra.get("host", None)
        port = config.extra.get("port", None)
        emulation_mode = config.extra.get("emulate")
        self.model = VacGauge(host, port, emulate=emulation_mode)


class FocalPlaneSlideComponent(ModelComponentMixin):
    def __init__(self, config):
        super(FocalPlaneSlideComponent, self).__init__(config)
        self.traceback_app = True
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        host = config.extra.get("host", None)
        port = config.extra.get("port", None)
        emulation_mode = config.extra.get("emulate")
        self.model = FocalPlaneSlide(host, port, emulate=emulation_mode)


class FlowSensorComponent(ModelComponentMixin):
    def __init__(self, config):
        super(FlowSensorComponent, self).__init__(config)
        self.traceback_app = True
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        host = config.extra.get("host", None)
        port = config.extra.get("port", None)
        emulation_mode = config.extra.get("emulate")
        self.model = FlowSensor(host, port, emulate=emulation_mode)


class CompoArmComponent(ModelComponentMixin):
    def __init__(self, config):
        super(CompoArmComponent, self).__init__(config)
        self.traceback_app = True
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        port = config.extra.get("port", None)
        emulation_mode = config.extra.get("emulate")
        self.model = CompoArms(port, emulate=emulation_mode)


class CompoLensComponent(ModelComponentMixin):
    def __init__(self, config):
        super(CompoLensComponent, self).__init__(config)
        self.traceback_app = True
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        host = config.extra.get("host", None)
        port = config.extra.get("port", None)
        emulation_mode = config.extra.get("emulate")
        self.model = CompoLens(host, port, emulate=emulation_mode)


class CompoComponent(WrapperComponentMixin):
    def __init__(self, config):
        # get name from config, or class name if missing
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        arm_topic = config.extra.get("arm_topic")
        lens_topic = config.extra.get("lens_topic")

        super(CompoComponent, self).__init__(config)
        self.traceback_app = True
        self.model = Compo(arm_topic, lens_topic)


class MeerstetterComponent(ModelComponentMixin):
    def __init__(self, config):
        super(MeerstetterComponent, self).__init__(config)
        self.traceback_app = True
        self._component_name = config.extra.get(
            "name", str(self.__class__).replace("Component", "")
        ).lower()
        host = config.extra.get("host", None)
        port = config.extra.get("port", None)
        emulation_mode = config.extra.get("emulate")
        self.model = Meerstetter(host, port, emulate=emulation_mode)
