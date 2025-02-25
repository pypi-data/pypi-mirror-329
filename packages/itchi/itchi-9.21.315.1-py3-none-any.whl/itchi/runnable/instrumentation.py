import re
import os
import logging
import sys
import datetime
import dataclasses
import shutil
import xml.etree.ElementTree as ET
from typing import List
from pathlib import Path
from itchi.templates.render import render_template, render_string
from itchi.config import ItchiConfig, RunnableInstrumentationConfig, InstrumentationTypeEnum
from itchi.profilerxml.model import ProfilerXml, ProfilerObject, TypeEnum, Enum, RunnableState
from itchi.type_enum import RUNNABLE_MAPPING


@dataclasses.dataclass
class RteHook:
    declaration: str
    name: str
    start_return: str
    id: str


def get_rte_runnable_hooks_eb(rte_xdm_file: Path) -> List[RteHook]:
    def findRteVfbTraceFunction(element):
        """<d:lst name="RteVfbTraceFunction">"""
        for elem in element:
            attr = elem.attrib
            if "name" in attr and attr["name"] == "RteVfbTraceFunction":
                return elem
            result = findRteVfbTraceFunction(elem)
            if result is not None and len(result) > 0:
                return result
        return None

    def getRteHooksVfbTraceElem(rteVfbTraceElem):
        """
        Searches the rteVfbTraceElem for RTE hook functions. Each function is
        returned as a hook. Start functions must get a unique ID while return
        functions always have the ID '0'.

        <d:var type="FUNCTION-NAME"
               value="Rte_Runnable_LOW_BRK_FLD_Sensor_SWC_RE_LOW_BRK_FLD_Sensor_SWC_Return"/>
        """
        hooks = []
        idCounter = 1
        for elem in rteVfbTraceElem:
            value = elem.attrib["value"]
            if value.endswith("_Start"):
                name = value.replace("_Start", "")
                startReturn = "Start"
                currentId = idCounter
                idCounter += 1
            elif value.endswith("_Return"):
                name = value.replace("_Return", "")
                startReturn = "Return"
                currentId = 0
            else:
                raise Exception("Unexpected {}.".format(value))
            declaration = "void {}(void)".format(value)
            hooks.append(RteHook(declaration, name, startReturn, str(currentId)))
        return hooks

    xmlRoot = ET.parse(rte_xdm_file).getroot()
    rteVfbTraceElem = findRteVfbTraceFunction(xmlRoot)
    hooks = getRteHooksVfbTraceElem(rteVfbTraceElem)
    return hooks


def get_datetime() -> str:
    # This is a terrible hack to make sure that the date strings do not cause
    # our regression tests to fail. If you go to the test definition you will see
    # that I manipulate sys.argv to set up the configuration for the respective
    # test case. While doing that I write "itchi-test.py" into the argument zero.
    # It would usually be "itchi.py" when executed from VS Code or the terminal,
    # and "itchi-bin.exe" when executed from the executable. I don't know if there
    # is a better way of doing this, but for now it shouldn't have any evil
    # consequences either so it should be okay.
    if sys.argv[0] == "itchi-test.py":
        return "Feb 05, 2020"
    return datetime.datetime.now().strftime("%b %d, %Y")


def get_rte_runnable_hooks_vector(rte_hook_h: Path, regex: str) -> List[RteHook]:
    """
    Function returns a list of RteHooks.

    A hook looks as follows. It consists of Rte_Runnable, the name of the
    SWC, and then the name of the Runnable itself. We are not really able to
    tell which part is the runnable name and which part is the SWC. So, we
    just treat the whole part from Rte_Runnable_ till _Start/Return as the
    Runnable name.

        FUNC(void, RTE_APPL_CODE) \
        Rte_Runnable_SWC_Core2_SWC_Core2_Runnable_100ms_Start(void)

    felixm(2018-08-17):

    It turns out that Runnables can have arguments different than void:
        FUNC(void, RTE_APPL_CODE) \
        Rte_Runnable_MODULE_DataServices_Data_CPU_Load_Read_ReadData_Start\
        (Var A, P2VAR(TYPE, AUTOMATIC, RTE_VAR) Data)

    We account for that by allow arbitrary arguments:
        "([^\n]+)" #  match anything that is not a newline

    felixm(2020-02-05):
        I added a configuration item runnable_instrumentation.regex
        to enable the user to change the regex. If that argument is empty
        we fall back to the previous regex.
    """

    if not regex:
        regex = (
            "("
            "FUNC\\(void, RTE_APPL_CODE\\) "
            "Rte_Runnable_"
            "(\\w+)"
            "_(Start|Return)"
            "\\([^\\n]+\\)"
            ")"
        )
    msg = f"{regex=}"
    logging.debug(msg)
    r = re.compile(regex)

    with open(rte_hook_h, "r") as f:
        matches = [m.groups() for line in f if (m := r.match(line))]

    hooks = []
    runnable_id_counter = 1
    for match in matches:
        if len(match) != 3:
            logging.error("The number of groups in the Runnable regex is not three.")
            logging.error("Use non-capturing '(?:foo)' groups to avoid this error.")
            sys.exit(-1)

        if match[2] == "Return":
            runnableId = 0
        else:
            runnableId = runnable_id_counter
            runnable_id_counter += 1
        h = RteHook(match[0], match[1], match[2], str(runnableId))
        hooks.append(h)

    if not hooks:
        msg = f"No hooks for {regex=} in {rte_hook_h=}."
        logging.error(msg)
    return hooks


def write_rte_hook_file(runnable_hooks: list[RteHook], config: RunnableInstrumentationConfig):
    template_file = get_template_file_path(config)
    vfb_hooks_c = config.isystem_vfb_hooks_c
    kwargs = {
        "filename": os.path.basename(vfb_hooks_c),
        "date": get_datetime(),
        "runnable_hooks": runnable_hooks,
    }

    if config.trace_variable_definition:
        s = render_string(config.trace_variable_definition, trace_variable=config.trace_variable)
        if s is not None:
            config.trace_variable_definition = s

    kwargs.update(config)
    content = render_template(template_file, kwargs)
    if content is None:
        logging.error(f"Could not render '{vfb_hooks_c}'.")
        return
    logging.info(f"Render '{template_file}' into '{vfb_hooks_c}'.")
    with open(vfb_hooks_c, "w") as f:
        f.write(content)


def get_runnable_type_enum(runnableHooks: List[RteHook]):
    enums = [Enum(hook.name, hook.id) for hook in runnableHooks if hook.start_return == "Start"]
    return TypeEnum(name=RUNNABLE_MAPPING, enums=enums)


def get_runnable_object(config: RunnableInstrumentationConfig) -> ProfilerObject:
    p = ProfilerObject(
        definition="Runnables_Definition",
        level="Runnable",
        name="Runnables",
        description="All Cores: Runnables",
        type=RUNNABLE_MAPPING,
        default_value="0",
    )

    p.runnable_state = RunnableState(mask_id="0xFFFFFF00", mask_core="0x000000FF", exit_value=0)

    if config.instrumentation_type == InstrumentationTypeEnum.STM_TRACE:
        # format as hex and pad to 10 characters
        p.signaling = f"STM({config.stm_channel})"
    elif config.instrumentation_type == InstrumentationTypeEnum.SOFTWARE_TRACE:
        p.runnable_state.mask_id = "0xFFFFFFFF"
        p.runnable_state.mask_core = None
        if config.sft_dbtag is True:
            p.signaling = "DBTAG"
        else:
            p.signaling = f"DBPUSH({config.sft_dbpush_register})"
        if config.software_based_coreid_gen == True:
            logging.info(
                "Attribute 'software_based_coreid_gen' does not have an effect for RH850 SFT"
            )
    elif config.instrumentation_type == InstrumentationTypeEnum.DATA_TRACE:
        p.expression = config.trace_variable
    else:
        m = f"Unexpected {config.instrumentation_type=}"
        raise ValueError(m)

    if config.software_based_coreid_gen == False:
        p.runnable_state.mask_core = None
    return p


def get_template_file_path(config: RunnableInstrumentationConfig) -> Path:
    directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../templates")
    if config.rte_hook_h.is_file():
        template_file = "Rte_Hook_isystem.template.c"
    elif config.rte_xdm.is_file():
        template_file = "Rte_Hook_isystem.template.c"
    else:
        raise Exception("Point rte_hook_h or rte_xdm to an existing file.")
    template_file_path = os.path.join(directory, template_file)

    if config.template_file != Path():
        user_template_path = os.path.join(os.getcwd(), config.template_file)
        # If user wants to provide their own config file and it does not
        # yet exist we copy our template for the user.
        os.makedirs(os.path.dirname(user_template_path), exist_ok=True)
        if not os.path.isfile(user_template_path):
            shutil.copyfile(template_file_path, user_template_path)
        template_file_path = user_template_path

    return Path(template_file_path)


def get_rte_hooks(config: RunnableInstrumentationConfig):
    if config.rte_hook_h.is_file() and config.rte_xdm.is_file():
        logging.error("Provide either rte_hook_h or rte_xdm.")
        logging.error("Remove the other attribute from the iTCHi JSON file.")
        raise Exception("Provide either rte_hook_h or rte_xdm.")

    if config.rte_hook_h.is_file():
        hooks = get_rte_runnable_hooks_vector(config.rte_hook_h, config.regex)
    elif config.rte_xdm.is_file():
        hooks = get_rte_runnable_hooks_eb(config.rte_xdm)
    else:
        raise Exception("Configure rte_hook_h or rte_xdm.")
    return hooks


def runnable_instrumentation(profiler_xml: ProfilerXml, config: ItchiConfig):
    if config.runnable_instrumentation is None:
        logging.critical("Configure runnable_instrumentation attribute.")
        sys.exit(1)
    logging.info("Running runnable_instrumentation.")
    hooks = get_rte_hooks(config.runnable_instrumentation)

    write_rte_hook_file(hooks, config.runnable_instrumentation)

    runnable_type_enum = get_runnable_type_enum(hooks)
    profiler_xml.set_type_enum(runnable_type_enum)

    runnable_object = get_runnable_object(config.runnable_instrumentation)
    profiler_xml.set_object(runnable_object)
