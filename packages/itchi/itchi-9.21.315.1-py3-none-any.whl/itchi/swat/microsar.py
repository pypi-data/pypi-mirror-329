import logging
import itchi.type_enum
import itchi.runnable.instrumentation

from .config_state import SwatConfigState
from itchi.swat import encoding
from itchi.swat.encoding import ObjectEncoding, size_to_mask, bits_required
from itchi.config import RunnableInstrumentationConfig
from itchi.ortilib.orti import Orti
from itchi.profilerxml.model import (
    Enum,
    TypeEnum,
    ProfilerObject,
    SwatObjectProperties,
)
from itchi.taskstate import instrumentation_microsar


def get_thread_state_mapping_list() -> list[tuple[int, str, str]]:
    """Returns the MICROSAR state mapping for SWAT including the optional
    task state state info string."""
    return [
        (2, "TERMINATED_ISR", "TERMINATED"),
        (3, "WAITING_EVENT", "WAITING"),
        (4, "WAITING_SEM", "WAITING"),
        (5, "READY", "READY"),
        (6, "RUNNING", "RUNNING"),
        (7, "NEW", "ACTIVE"),
        (1, "TERMINATED_TASK", "TERMINATED"),
    ]


def get_thread_state_mapping() -> dict[int, str]:
    """Returns MICROSAR state mapping as a dictionary."""
    return {id: state for id, state, _ in get_thread_state_mapping_list()}


def get_thread_state_mapping_type_enum() -> TypeEnum:
    """Returns MICROSAR state mapping as a TypeEnum that can be added to
    the ProfilerXml object."""
    tuples = get_thread_state_mapping_list()
    return TypeEnum(
        name=itchi.type_enum.TASK_STATE_MAPPING,
        enums=[
            Enum(state, str(val), task_state_property=task_state)
            for val, state, task_state in tuples
        ],
    )


def get_thread_mapping(orti: Orti) -> dict[int, str]:
    """Returns the MICROSAR thread mapping as a dictionary."""
    thread_mapping = instrumentation_microsar.get_vector_microsar_thread_mapping(orti)
    return {int(id): name for name, id in thread_mapping}


def get_thread_mapping_type_enum(thread_encoding: ObjectEncoding) -> TypeEnum:
    """Returns the MICROSAR thread mapping as a TypeEnum that can be added
    to the ProfilerXml object."""
    thread_mapping = [(name, str(id)) for id, name in thread_encoding.object_id_mapping.items()]
    thread_type_enum = instrumentation_microsar.get_thread_mapping_type_enum(thread_mapping)
    return thread_type_enum


def get_btf_mapping_type_enum() -> TypeEnum:
    states = [state for _, state, _ in get_thread_state_mapping_list()]
    btf_thread_type_enum = itchi.type_enum.get_btf_mapping_type_enum(states)
    btf_thread_type_enum.name = itchi.type_enum.BTF_MAPPING
    return btf_thread_type_enum


def get_thread_object(thread_encoding: ObjectEncoding) -> ProfilerObject:
    """Get ProfilerObject for SWAT Thread Profiling."""
    assert thread_encoding.type_id_name == itchi.swat.encoding.OBJECT_ENCODING_THREADS_TYPE_NAME

    data_size = (
        thread_encoding.core_id_size
        + thread_encoding.state_id_size
        + thread_encoding.object_id_size
    )
    data_offset = thread_encoding.type_id_size

    # The following offsets are relative to the data offset in contrast
    # to the offsets in the ObjectEncoding which are relative to the
    # message as a whole.
    mask_core = size_to_mask(thread_encoding.core_id_size)
    state_offset = thread_encoding.core_id_size
    mask_state = size_to_mask(thread_encoding.state_id_size, state_offset)

    thread_offset = state_offset + thread_encoding.state_id_size
    mask_thread = size_to_mask(thread_encoding.object_id_size, thread_offset)

    swat_object_properties = SwatObjectProperties(
        type_value=thread_encoding.type_id_key,
        data_size=data_size,
        data_offset=data_offset,
        task_state_mask_core=mask_core,
        task_state_mask_state=mask_state,
        task_state_mask_thread_id=mask_thread,
        task_state_type_enum_name=itchi.type_enum.TASK_STATE_MAPPING,
    )

    return ProfilerObject(
        name="Threads",
        description="Threads",
        definition="Threads_Definition",
        type=itchi.type_enum.THREAD_MAPPING,
        level="Task",
        signaling="SWAT",
        swat_object_properties=swat_object_properties,
        btf_mapping_type=itchi.type_enum.BTF_MAPPING,
    )


def get_microsar_thread_encoding(state: SwatConfigState) -> ObjectEncoding:
    """Clones and transforms `ObjectEncoding` into Vector MICROSAR Threads encoding."""
    obj = state.generic_encoding.model_copy()
    obj.type_id_key = state.type_id_key
    obj.type_id_name = itchi.swat.encoding.OBJECT_ENCODING_THREADS_TYPE_NAME
    obj.core_id_mapping = None

    payload_offset = obj.get_payload_offset()

    obj.state_id_mapping = itchi.swat.microsar.get_thread_state_mapping()
    obj.state_id_offset = payload_offset
    obj.state_id_size = bits_required(len(obj.state_id_mapping))

    obj.object_id_mapping = itchi.swat.microsar.get_thread_mapping(state.orti)
    obj.object_id_offset = payload_offset + obj.state_id_size
    obj.object_id_size = bits_required(len(obj.object_id_mapping))

    payload_size = obj.state_id_size + obj.object_id_size
    max_payload_size = obj.get_max_payload_size()
    logging.debug(f"Used {payload_size} out of {max_payload_size} bits for MICROSAR threads.")
    assert payload_size <= max_payload_size, "Not enough bits to represent thread payload"

    return obj


def do_microsar_thread_profiler_xml_config(state: SwatConfigState):
    """Adds the necessary `Object` and `TypeEnums` for MICROSAR thread profiling to
    the `state.profiler_xml`."""
    assert state.microsar_thread_encoding is not None
    encoding = state.microsar_thread_encoding

    btf_thread_type_enum = get_btf_mapping_type_enum()
    state.profiler_xml.set_type_enum(btf_thread_type_enum)

    thread_mapping_type_enum = get_thread_mapping_type_enum(encoding)
    state.profiler_xml.set_type_enum(thread_mapping_type_enum)

    thread_state_mapping_type_enum = get_thread_state_mapping_type_enum()
    state.profiler_xml.set_type_enum(thread_state_mapping_type_enum)

    thread_object = get_thread_object(encoding)

    if state.num_cores == 1:
        core = state.orti.orti_core_to_soc_core.get(0, 0)
        logging.warning(
            f"Adding <SourceCore>{core}</SourceCore> to Profiler XML thread object. "
            "This is required for single core applications. Please remap the core via "
            "`running_taskisr.orti_core_to_soc_core` if your application does not run "
            f"on SoC core `{core}`."
        )
        thread_object.source_core = str(0)

    state.profiler_xml.set_object(thread_object)


def do_microsar_runnable_profiler_xml_config(state: SwatConfigState):
    """Adds the necessary `Object` and `TypeEnums` for MICROSAR Runnable profiling to
    the `state.profiler_xml`."""
    assert state.microsar_runnable_encoding is not None
    runnable_config = state.config.runnable_instrumentation
    assert runnable_config is not None
    runnable_type_enum = get_runnable_mapping_type_enum(runnable_config)
    state.profiler_xml.set_type_enum(runnable_type_enum)

    runnable_object = get_runnable_object_swat(state.microsar_runnable_encoding)

    if state.num_cores == 1:
        core = state.orti.orti_core_to_soc_core.get(0, 0)
        logging.warning(
            f"Adding <Core>{core}</Core> to Profiler XML Runnable object. "
            "This is required for single core applications. Please remap the core via "
            "`running_taskisr.orti_core_to_soc_core` if your application does not run "
            f"on SoC core `{core}`."
        )
        runnable_object.source_core = str(core)

    state.profiler_xml.set_object(runnable_object)


def get_runnable_mapping_type_enum(config: RunnableInstrumentationConfig) -> TypeEnum:
    runnable_hooks = itchi.runnable.instrumentation.get_rte_hooks(config)
    return itchi.runnable.instrumentation.get_runnable_type_enum(runnable_hooks)


def get_runnable_object_swat(runnable_encoding: ObjectEncoding) -> ProfilerObject:
    """Get ProfilerObject for SWAT Runnable Profiling."""
    assert runnable_encoding.type_id_name == itchi.swat.encoding.OBJECT_ENCODING_RUNNABLES_TYPE_NAME

    data_size = (
        runnable_encoding.core_id_size
        + runnable_encoding.state_id_size
        + runnable_encoding.object_id_size
    )
    data_offset = runnable_encoding.type_id_size

    # Offset relative to data start
    runnable_offset = runnable_encoding.core_id_size + runnable_encoding.state_id_size
    runnable_mask = itchi.swat.encoding.size_to_mask(
        runnable_encoding.object_id_size, runnable_offset
    )

    # Take runnable message data encoding and convert it to the Profiler XML SWAT format.
    swat_object_properties = SwatObjectProperties(
        type_value=runnable_encoding.type_id_key,
        data_size=data_size,
        data_offset=data_offset,
        runnable_mask_core=encoding.size_to_mask(runnable_encoding.core_id_size),
        runnable_mask_id=runnable_mask,
        runnable_exit_value="0",
    )

    return ProfilerObject(
        name="Runnables",
        description="Runnables",
        definition="Runnables_Definition",
        type=itchi.type_enum.RUNNABLE_MAPPING,
        level="Runnable",
        signaling="SWAT",
        swat_object_properties=swat_object_properties,
    )


def get_microsar_runnable_encoding(state: SwatConfigState) -> ObjectEncoding:
    """Clones and transforms `ObjectEncoding` into Vector MICROSAR Runnables encoding."""
    config = state.config.runnable_instrumentation
    assert config is not None

    obj = state.generic_encoding.model_copy()
    obj.type_id_key = state.type_id_key
    obj.type_id_name = itchi.swat.encoding.OBJECT_ENCODING_RUNNABLES_TYPE_NAME
    payload_offset = obj.get_payload_offset()

    # Runnables don't have state IDs
    obj.state_id_mapping = {0: "Runnable"}
    obj.state_id_offset = payload_offset
    obj.state_id_size = 0

    hooks = itchi.runnable.instrumentation.get_rte_runnable_hooks_vector(
        config.rte_hook_h, config.regex
    )
    obj.object_id_mapping = {int(hook.id): hook.name for hook in hooks}
    obj.object_id_mapping[0] = "NO_RUNNABLE"

    obj.object_id_offset = obj.state_id_offset + obj.state_id_size
    obj.object_id_size = bits_required(len(obj.object_id_mapping))
    payload_size = obj.state_id_size + obj.object_id_size
    max_payload_size = obj.get_max_payload_size()
    logging.debug(f"Used {payload_size} out of {max_payload_size} bits for MICROSAR Runnables.")
    assert payload_size <= max_payload_size, "Not enough bits to represent Runnables payload"
    return obj
