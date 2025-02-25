import logging
import itchi.taskstate.single_variable
from pathlib import Path
from itchi.templates.render import render_template_from_templates, render_string
from itchi.config import (
    ItchiConfig,
    TaskStateInstMicrosarConfig,
    InstrumentationTypeEnum,
    SpinlockInstMicrosarConfig,
)
from itchi.ortilib.orti import Orti
from itchi.profilerxml.model import ProfilerXml, ProfilerObject
from itchi.profilerxml.model import Enum, StateInfo, TypeEnum, TaskState
from typing import List, Tuple
import itchi.type_enum


def task_state_instrumentation_microsar(orti: Orti, profiler_xml: ProfilerXml, config: ItchiConfig):
    """Thread state (aka task state and ISR) profiling for Vector MICROSAR Timing Hooks based profiling."""

    logging.info("Running task_state_instrumentation_vector.")
    if config.task_state_inst_microsar is None:
        logging.error("Missing task_state_inst_microsar config.")
        return

    # Get Vector MICROSAR Thread ID Mapping and add TypeEnum to Profiler XML.
    thread_mapping = get_vector_microsar_thread_mapping(orti)
    type_enum = get_thread_mapping_type_enum(thread_mapping)
    profiler_xml.set_type_enum(type_enum)

    # Get Vector MICROSAR State Mapping and add TypeEnum to Profiler XML.
    state_type_enum = get_state_mapping_vector_microsar()
    profiler_xml.set_type_enum(state_type_enum)

    # Transform Thread states into BTF event mapping and add TypeEnum to Profiler XML.
    states = [enum.name for enum in state_type_enum.enums]
    btf_type_enum = itchi.type_enum.get_btf_mapping_type_enum(states)
    btf_type_enum.name = itchi.type_enum.BTF_MAPPING
    profiler_xml.set_type_enum(btf_type_enum)

    # Add ARTI MDF4 TypeEnum to Profiler XML for MDF4 export.
    mdf4_type_enum = get_arti_mdf4_type_enum()
    profiler_xml.set_type_enum(mdf4_type_enum)

    # Write instrumentation and add main thread object to Profiler XML.
    write_instrumentation_code(config, config.task_state_inst_microsar)
    thread = get_thread_object(config.task_state_inst_microsar)
    profiler_xml.set_object(thread)


def write_instrumentation_code(config: ItchiConfig, task_config: TaskStateInstMicrosarConfig):
    """Write Vector MICROSAR timing-hooks header and source file."""

    if task_config.trace_variable_definition:
        s = render_string(
            task_config.trace_variable_definition, trace_variable=task_config.trace_variable
        )
        if s is not None:
            task_config.trace_variable_definition = s

    # If spinlock instrumentation is configured, update kwargs accordingly.
    kwargs = dict(task_config)
    if (
        config.commands
        and config.commands.spinlock_instrumentation_microsar
        and config.spinlock_inst_microsar
    ):
        replace_spinlock_trace_variable(config.spinlock_inst_microsar)
        kwargs.update(config.spinlock_inst_microsar)
        kwargs["spinlock_generate_instrumentation"] = True

    files_to_render: List[Tuple[str, Path]] = [
        ("Os_TimingHooks_isystem.c", task_config.vector_os_timing_hooks_c),
        ("Os_TimingHooks_isystem.h", task_config.vector_os_timing_hooks_h),
    ]
    for template_file, destination_file in files_to_render:
        # Do not render empty path.
        if destination_file == Path():
            continue

        content = render_template_from_templates(Path(template_file), kwargs)
        if not isinstance(content, str):
            logging.error(f"Could not render '{destination_file}'.")
            continue

        logging.info(f"Render template '{template_file}' into '{destination_file}'.")
        with open(destination_file, "w", encoding="utf-8") as f:
            f.write(content)


def get_thread_object(config: TaskStateInstMicrosarConfig) -> ProfilerObject:
    """Get ProfilerObject for Vector MICROSAR OS Thread profiling."""
    p = ProfilerObject(
        definition="Threads_Definition",
        description="All Cores: Threads",
        type=itchi.type_enum.THREAD_MAPPING,
        name="Threads",
        level="Task",
        default_value="NO_THREAD",
        arti_mdf4_mapping_type=itchi.type_enum.ARTI_MDF4,
    )

    p.task_state = get_task_state()
    if config.software_based_coreid_gen is False:
        p.task_state.mask_core = None

    if config.instrumentation_type == InstrumentationTypeEnum.STM_TRACE:
        p.signaling = f"STM({config.stm_channel})"
    elif config.instrumentation_type == InstrumentationTypeEnum.SOFTWARE_TRACE:
        p.signaling = f"DBPUSH({config.sft_dbpush_register})"
    elif config.instrumentation_type == InstrumentationTypeEnum.DATA_TRACE:
        p.expression = config.trace_variable
    else:
        m = f"Unexpected {config.instrumentation_type=}"
        raise ValueError(m)
    return p


def get_task_state() -> TaskState:
    """Get TaskState object for Vector MICROSAR OS profiling."""
    return TaskState(
        mask_id="0x0000FFFF",
        mask_state="0x00FF0000",
        mask_core="0xFF000000",
        type=itchi.type_enum.TASK_STATE_MAPPING,
        btf_mapping_type=itchi.type_enum.BTF_MAPPING,
    )


def get_state_infos() -> List[StateInfo]:
    return [
        StateInfo("RUNNING", "Run"),
        StateInfo("RUNNING_ISR", "Run"),
        StateInfo("TERMINATED_TASK", "Terminate"),
        StateInfo("TERMINATED_ISR", "Terminate"),
        StateInfo("WAITING_EVENT", "Terminate"),
        StateInfo("WAITING_SEM", "Terminate"),
    ]


def get_thread_mapping_type_enum(thread_mapping: List[Tuple[str, str]]) -> TypeEnum:
    """Transform Vector MICROSAR Thread Mapping into TypeEnum.

    Args:
        thread_mapping (List[Tuple[str, str]]): extracted from ORTI file

    Returns:
        TypeEnum: to be added to Profiler XML object
    """
    type_enum = TypeEnum(name=itchi.type_enum.THREAD_MAPPING, enums=[])
    for thread_name, thread_value in thread_mapping:
        enum = Enum(thread_name, thread_value)
        type_enum.enums.append(enum)
    return type_enum


def get_state_mapping_vector_microsar() -> TypeEnum:
    return TypeEnum(
        name=itchi.type_enum.TASK_STATE_MAPPING,
        enums=[
            Enum("NEW", "11", task_state_property="ACTIVE"),
            Enum("READY", "16", task_state_property="READY"),
            Enum("RUNNING_ISR", "31", task_state_property="RUNNING"),
            Enum("TERMINATED_ISR", "2", task_state_property="TERMINATED"),
            Enum("WAITING_EVENT", "4", task_state_property="WAITING"),
            Enum("WAITING_SEM", "8", task_state_property="WAITING"),
            Enum("RUNNING", "29", task_state_property="RUNNING"),
            Enum("TERMINATED_TASK", "1", task_state_property="TERMINATED"),
        ],
    )


def get_arti_mdf4_type_enum() -> TypeEnum:
    return TypeEnum(
        name=itchi.type_enum.ARTI_MDF4,
        enums=[
            Enum("NEW", "Ready"),
            Enum("READY", "Ready"),
            Enum("RUNNING", "Running"),
            Enum("TERMINATED_TASK", "Suspended"),
            Enum("WAITING_EVENT", "Waiting"),
            Enum("WAITING_SEM", "Waiting"),
            Enum("RUNNING_ISR", "Active"),
            Enum("TERMINATED_ISR", "Inactive"),
        ],
    )


def get_vector_microsar_thread_mapping(orti: Orti) -> List[Tuple[str, str]]:
    """
    Returns a list of tuples where the first element is the thread name and the
    second one the thread ID. This only works for the Vector MICROSAR OS and
    Vector MICROSAR Timing Hooks is currently the only instrumentation based
    thread state profiling OS we support.

    Args:
        orti (src.ortilib.Orti): ORTI file object

    Returns:
        List[Tuple[str, str]]: List of thread name, thread ID tuples.
    """
    thread_id_counter = 0
    thread_mapping = []

    # (FelixM) The following requires knowledge about how Vector DaVinci
    # Configurator assigns the thread IDs. The ORTI file contains an array of
    # tasks and an array of ISRs. The thread IDs are generated by first
    # enumerating the tasks, and then enumerating the ISRs starting from the
    # last task index. Finally, there are an INVALID_THREAD and a NO_THREAD
    # object that get their own ID (after the other Tasks and ISRs). The
    # INVALID_TASK and INVALID_ISR objects don't get an ID and have to be
    # ignored.

    # (04-Dec-2024 Felixm) This now longer works in all cases because in newer
    # (after 2021) MICROSAR versions there can be an arbitrary number of "hooks"
    # thread IDs after the last ISR in `Os_Types_lcfg.h`. There is currently
    # no solution for this except manually editing the Profiler XML if an unexpected
    # ID appears.

    for task_enum in orti.get_enum_elements_runningtask():
        task_name = task_enum.desc
        if task_name != "INVALID_TASK":
            thread_mapping.append((task_name, str(thread_id_counter)))
            thread_id_counter += 1

    for isrEnum in orti.get_enum_elements_runningisr2():
        isrName = isrEnum.desc
        if isrName != "INVALID_ISR":
            thread_mapping.append((isrName, str(thread_id_counter)))
            thread_id_counter += 1

    thread_mapping.append(("INVALID_THREAD", str(thread_id_counter)))
    thread_id_counter += 1
    thread_mapping.append(("NO_THREAD", str(thread_id_counter)))
    return thread_mapping


def replace_spinlock_trace_variable(config: SpinlockInstMicrosarConfig):
    """Replace '{{ spinlock_trace_variable }}' in trace_variable_definition."""
    if not config.spinlock_trace_variable_definition:
        return

    new_trace_variable_definition = render_string(
        config.spinlock_trace_variable_definition,
        spinlock_trace_variable=config.spinlock_trace_variable,
        trace_variable=config.spinlock_trace_variable,
    )
    if new_trace_variable_definition:
        config.spinlock_trace_variable_definition = new_trace_variable_definition
