import logging
import itchi.type_enum
from . import microsar
from . import render
from . import encoding
from .config_state import SwatConfigState
from itchi.config import ItchiConfig
from itchi.ortilib.orti import Orti
from itchi.profilerxml.model import ProfilerXml, SwatConfigProperties, ProfilerObject


def create_swat_default_config(state: SwatConfigState):
    """Create SWAT `ProfilerObject`, `ObjectEncoding`, and `TypeEnum` for status messages."""
    status_encoding = state.generic_encoding.model_copy().into_status(state.type_id_key)
    state.trace_ninja.decoder.objects.append(status_encoding)
    swat_var = state.swat_config.swat_target_struct

    swat_config_properties = SwatConfigProperties(
        type_mask=encoding.size_to_mask(status_encoding.type_id_size),
        time_offset=status_encoding.timestamp_offset,
        time_size=status_encoding.timestamp_size,
        buffer=f"{swat_var}.buffer",
        read_index=f"{swat_var}.rd_idx",
        write_index=f"{swat_var}.wr_tail",
        status=f"{swat_var}.status",
        cycle_duration_ns=status_encoding.time_ns_per_tick,
        time_right_shift=state.swat_config.time_right_shift,
        status_enum=itchi.type_enum.SWAT_STATUS,
    )

    swat_object = ProfilerObject(
        name="SWAT_Config",
        definition="SWAT_Config",
        description="SWAT_Config",
        level="SWAT",
        swat_config_properties=swat_config_properties,
    )

    state.profiler_xml.set_object(swat_object)
    state.profiler_xml.set_type_enum(itchi.type_enum.get_swat_status_type_enum())


def create_swat_microsar_thread_config(state: SwatConfigState):
    assert state.config.task_state_inst_microsar is not None
    thread_encoding = microsar.get_microsar_thread_encoding(state)
    state.trace_ninja.append_encoding(thread_encoding)
    state.microsar_thread_encoding = thread_encoding
    microsar.do_microsar_thread_profiler_xml_config(state)
    render.microsar_timing_hooks(state)


def create_swat_microsar_runnable_config(state: SwatConfigState):
    assert state.config.runnable_instrumentation is not None
    runnable_encoding = microsar.get_microsar_runnable_encoding(state)
    state.trace_ninja.append_encoding(runnable_encoding)
    state.microsar_runnable_encoding = runnable_encoding
    microsar.do_microsar_runnable_profiler_xml_config(state)
    render.microsar_vfb_runnable_hooks(state)


def swat(orti: Orti, profiler_xml: ProfilerXml, config: ItchiConfig):
    # ORTI file is not required for this use case.
    profiler_xml.orti = None

    state = SwatConfigState(orti, profiler_xml, config)

    if state.num_types >= 256:
        logging.critical("The maximum type size is currently 8.")
        return

    create_swat_default_config(state)

    # MICROSAR Thread config
    if state.config.task_state_inst_microsar is not None:
        create_swat_microsar_thread_config(state)

    if state.config.runnable_instrumentation is not None:
        # MICROSAR Runnable config
        if state.config.runnable_instrumentation.rte_hook_h.is_file():
            create_swat_microsar_runnable_config(state)
        else:
            logging.warning(
                "Runnable Instrumentation attribute provided but `Rte_Hook.h` does not exist. "
                "Other RTEs are currently not supported for Runnable instrumentation."
            )

    if config.signals:
        for signal in config.signals.signals:
            # TODO(felixm): Also add to Profiler XML when I know how.
            signal_encoding = state.generic_encoding.model_copy().into_signal_u32(
                state.type_id_key, signal
            )
            state.signal_encodings.append(signal_encoding)
            state.trace_ninja.append_encoding(signal_encoding)

    render.swat_config_h(state)
    if state.config.swat is not None:
        state.trace_ninja.write(state.config.swat.trace_ninja_json)
