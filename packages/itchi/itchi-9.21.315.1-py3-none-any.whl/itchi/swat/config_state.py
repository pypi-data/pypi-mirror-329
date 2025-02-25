from dataclasses import dataclass
from typing import Optional
from itchi.ortilib.orti import Orti
from itchi.profilerxml.model import ProfilerXml
from itchi.config import ItchiConfig, SwatConfig
from .encoding import ObjectEncoding
from .trace_ninja import TraceNinjaConfig
from . import encoding
from . import trace_ninja


@dataclass
class SwatConfigState:
    orti: Orti
    profiler_xml: ProfilerXml
    config: ItchiConfig
    swat_config: SwatConfig
    trace_ninja: TraceNinjaConfig
    generic_encoding: ObjectEncoding
    signal_encodings: list[ObjectEncoding]
    num_cores: int = 0
    num_types: int = 0
    microsar_thread_encoding: Optional[ObjectEncoding] = None
    microsar_runnable_encoding: Optional[ObjectEncoding] = None
    _type_id_key: int = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, orti: Orti, profiler_xml: ProfilerXml, config: ItchiConfig):
        self.orti = orti
        self.profiler_xml = profiler_xml
        self.config = config
        self.num_cores = self.orti.get_number_of_cores()
        self.num_types = self.calculate_num_types()
        self.swat_config = config.swat if config.swat is not None else SwatConfig.default_factory()
        self.trace_ninja = trace_ninja.get_trace_ninja_config(self.swat_config)
        self.generic_encoding = encoding.get_generic_encoding(
            self.num_cores, self.num_types, self.swat_config.cycle_duration_ns
        )
        self.signal_encodings = list()

    def calculate_num_types(self) -> int:
        num_types = 1  # Always need one type for the status messages
        num_types += 1 if self.config.task_state_inst_microsar is not None else 0
        num_types += 1 if self.config.runnable_instrumentation is not None else 0
        num_types += len(self.config.signals.signals) if self.config.signals else 0
        return num_types

    @property
    def type_id_key(self) -> int:
        current_key = self._type_id_key
        self._type_id_key += 1
        return current_key
