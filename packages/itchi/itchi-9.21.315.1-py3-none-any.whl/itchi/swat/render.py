import logging
import itchi.runnable.instrumentation
from pathlib import Path
from itchi.templates.render import render_template_from_templates
from .encoding import size_to_mask
from .config_state import SwatConfigState


def swat_config_h(state: SwatConfigState):
    TEMPLATE_FILE = "swat_config.h"
    destination_file = Path("swat_config.h")

    if destination_file == Path():
        logging.error(f"Did not render '{TEMPLATE_FILE}'.")
        return

    time_right_shift = (
        state.swat_config.time_right_shift if state.swat_config.time_right_shift else 3
    )

    kwargs = {
        "filename": destination_file,
        "include_guard_str": str(destination_file).upper().replace(".", "_"),
        "generic": state.generic_encoding,
        "microsar_thread": state.microsar_thread_encoding,
        "microsar_runnable": state.microsar_runnable_encoding,
        "signals": state.signal_encodings,
        "size_to_mask": size_to_mask,
        "time_right_shift": time_right_shift,
    }

    content = render_template_from_templates(Path(TEMPLATE_FILE), kwargs)
    if not isinstance(content, str):
        logging.error(f"Could not render '{destination_file}'.")
        return

    logging.info(f"Render template '{TEMPLATE_FILE}' into '{destination_file}'.")
    with open(destination_file, "w", encoding="utf-8") as f:
        f.write(content)


def microsar_timing_hooks(state: SwatConfigState):
    assert state.config.task_state_inst_microsar is not None
    TEMPLATE_FILE = "Os_TimingHooks_swat.h"
    destination_file = state.config.task_state_inst_microsar.vector_os_timing_hooks_h

    if destination_file == Path():
        logging.error("Did not render because 'vector_os_timing_hooks_h' is empty.")
        return

    include_guard_h = str(destination_file).upper().replace(".", "_")
    kwargs: dict = {"include_guard_str": include_guard_h}

    content = render_template_from_templates(Path(TEMPLATE_FILE), kwargs)
    if not isinstance(content, str):
        logging.error(f"Could not render '{destination_file}'.")
        return

    logging.info(f"Render template '{TEMPLATE_FILE}' into '{destination_file}'.")
    with open(destination_file, "w", encoding="utf-8") as f:
        f.write(content)


def microsar_vfb_runnable_hooks(state: SwatConfigState):
    config = state.config.runnable_instrumentation
    assert config is not None
    hooks = itchi.runnable.instrumentation.get_rte_runnable_hooks_vector(
        config.rte_hook_h, config.regex
    )
    config.instrumentation_type = itchi.config.InstrumentationTypeEnum.SWAT
    itchi.runnable.instrumentation.write_rte_hook_file(hooks, config)
