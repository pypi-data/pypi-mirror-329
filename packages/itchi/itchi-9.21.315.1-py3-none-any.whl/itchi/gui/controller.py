##
# @brief A middle layer between iTCHi models (configuration) and GUI
#
import os
import typing
import pathlib
import enum
import ast
import xml.etree.ElementTree
import io
import sys
from .models import ItchiConfig, ItchiHelp
from dataclasses import dataclass
from typing import Tuple, Dict, List
from pathlib import Path
from itchi import itchi_cli


@enum.unique
class EConfigSectionAttributeType(enum.IntEnum):
    ##
    # @brief Enumerator for attribute types that GUI uses when showing their values
    #
    # Enumerator         | Description                                                             |
    # -------------------|-------------------------------------------------------------------------|
    # Basic              | Basic type (str, int, ...); In GUI it will be shown as a simple string  |
    # Boolean            | Boolean type (True, False); In GUI it will be shown as a checkbox       |
    # Enum               | Enum type; In GUI it will be shown as a drop-down
    # Path               | String with an additional file picker button that opens file explorer   |
    # IterableOneColumn  | Attribute will have a drop-down item with one column editable           |
    # IterableTwoColumns | Attribute will have a drop-down item with two columns editable          |
    #
    Basic = enum.auto()
    Boolean = enum.auto()
    Enum = enum.auto()
    Path = enum.auto()
    IterableOneColumn = enum.auto()
    IterableTwoColumns = enum.auto()


@dataclass
class ConfigSectionAttribute:
    ##
    # @brief Class that acts as middlelayer between iTCHi config attribute and property editor.
    #
    name: str
    type: EConfigSectionAttributeType
    value: typing.Any


class CmdInfo:
    ##
    # @brief Holds information about specific command for GUI
    #        (name of a separator, group, list of commands that the command blocks, ...)
    #
    def __init__(self, separator: str, group: str, cmdBlockList: list = [], groupBlockList: list = [], htmlElementId: str = ""):
        ##
        # @brief Class constructor
        # @param separator     Name of the separator (expanding menu item)
        #                      where command will be placed
        # @param group         Name of the group under which the command will be sorted
        # @param cmdBlockList  A list of other commands that this command blocks when selected
        # @param htmlElementID Element id associated with the command
        #                        - used for searching help .hmtl
        #                        - used in conjuction with htmlElementID
        self.separator = separator
        self.group = group
        self.htmlElementId = htmlElementId
        self._cmdBlockList = cmdBlockList if cmdBlockList else []
        self._groupBlockList = groupBlockList if groupBlockList else []
        self._blockedCountingSemaphore = 0

    def getCmdBlockList(self) -> typing.List[str]:
        ##
        # @brief Get all the blocked commands from groupBlock and cmdBlock list
        cmdBlockList = []

        # Add all commands from groupBlockList to the list
        for group in self._groupBlockList:
            for cmd, cmdInfo in Controller.cmds.items():
                if cmdInfo.group == group:
                    cmdBlockList.append(cmd)

        # Add individually blocked commands to the list
        for cmd in self._cmdBlockList:
            cmdBlockList.append(cmd)

        return cmdBlockList

    def blockCmd(self, block: bool):
        if block:
            self._blockedCountingSemaphore += 1
        else:
            self._blockedCountingSemaphore -= 1

    def isBlocked(self) -> bool:
        return True if self._blockedCountingSemaphore > 0 else False

    def clearBlockedCountingSemaphore(self):
        self._blockedCountingSemaphore = 0


class Controller:
    log_file: str = 'itchi.log'
    cmds = {
        "running_taskisr": CmdInfo("Task Trace Technique", "Running Task", [], ["Task State"], "running-taskisr"),
        "running_taskisr_btf": CmdInfo("Task Trace Technique", "Running Task", [], ["Task State"], "running-taskisr-tracing-with-btf-export"),
        "running_taskisr_sampling": CmdInfo("Task Trace Technique", "Running Task", [], ["Task State"], "running-taskisr-sampling"),
        "task_state_single_variable": CmdInfo("Task Trace Technique", "Task State", [], ["Running Task"], "task-state-tracing-with-single-state-variables"),
        "task_state_complex_native": CmdInfo("Task Trace Technique", "Task State", [], ["Running Task"], "task-state-tracing-with-complex-state-native"),
        "task_state_instrumentation_microsar": CmdInfo("Task Trace Technique", "Task State", [], ["Running Task"], "task-state-tracing-with-instrumentation"),
        "task_state_instrumentation_autocore": CmdInfo("Task Trace Technique", "Task State", [], ["Running Task"], "task-state-tracing-with-instrumentation"),
        "runnable_instrumentation": CmdInfo("Runnable Trace Technique", "Runnable Tracing", [], [], "runnable-tracing-with-instrumentation"),
        "runnable_program_flow": CmdInfo("Runnable Trace Technique", "Runnable Tracing", [], [], "runnable-program-flow"),
        "signals": CmdInfo("Others", "Signals", [], [], "signals"),
        "spinlock_instrumentation_microsar": CmdInfo("Others", "Spinlocks", [], [], "spinlock-with-instrumentation"),
    }

    @classmethod
    def createDefaultConfigFile(cls, configFilePathStr: str):
        configFilePath = pathlib.Path(configFilePathStr)
        ItchiConfig.createDefaultConfigFile(configFilePath)

    @classmethod
    def isItchiRunFilePathValid(cls) -> typing.Tuple[bool, pathlib.Path]:
        ##
        # @deprecated
        # @brief  Check if the file path for itchi executable is valid and file exists
        # @return True if path is valid and file exists, False otherwise
        #
        isValid = ItchiConfig.isItchiRunFilePathValid()
        filePath = ItchiConfig.getItchiRunFilePath()
        return (isValid, filePath)

    @classmethod
    def isHtmlFilePathValid(cls) -> Tuple[bool, Path]:
        isValid = ItchiHelp.isHtmlFilePathValid()
        filePath = ItchiHelp.getHtmlFilePath()
        return (isValid, filePath)

    @classmethod
    def getSeparatorGroupsCmds(cls) -> Dict[str, Dict[str, List[str]]]:
        ##
        # @brief  Get separators (menu items), its groups and all of the cmds
        # @return A dict of {'separatorName': {'groupName': ListOfCmds[]}}
        #
        separatorGroupsCmds: Dict[str, Dict[str, List[str]]] = {}
        for cmd, cmdInfo in Controller.cmds.items():
            if cmdInfo.separator not in separatorGroupsCmds:
                separatorGroupsCmds[cmdInfo.separator] = {}
            if cmdInfo.group not in separatorGroupsCmds[cmdInfo.separator]:
                separatorGroupsCmds[cmdInfo.separator][cmdInfo.group] = []
            separatorGroupsCmds[cmdInfo.separator][cmdInfo.group].append(cmd)
        return separatorGroupsCmds

    def onCmdStateChange(self, cmdKey: str, bChecked: bool):
        ##
        # @brief For the selected cmd, block or unblock all cmds in its
        #        CmdBlockList based on cmds bChecked state
        # @param cmdKey   Name of the cmd
        # @param bChecked Is the command checked or unchecked
        #
        for cmdBlock in Controller.cmds[cmdKey].getCmdBlockList():
            Controller.cmds[cmdBlock].blockCmd(bChecked)

    def isCmdBlocked(self, cmdKey: str) -> bool:
        return self.cmds[cmdKey].isBlocked()

    def _clearCmdsBlockedState(self):
        for cmdInfo in Controller.cmds.values():
            cmdInfo.clearBlockedCountingSemaphore()

    def __init__(self, configFilePathStr: str):
        ##
        # @brief Class constructor
        # @param configFilePath Absolute path to the configuration file used for iTCHi configuration
        #
        self._itchiConfig = ItchiConfig(pathlib.Path("itchi.json"))

        if configFilePathStr:
            try:
                configFilePath = pathlib.Path(configFilePathStr).resolve()
                if configFilePath.is_file():
                    self._itchiConfig = ItchiConfig(configFilePath)
                    self._itchiConfig.loadConfigFileData()
                    self._itchiHelp = ItchiHelp()

                    # Change dir to config file dir -> orti, pxml can then use relative path
                    configFileDir = configFilePath.parent
                    os.chdir(configFileDir)

                    # Clear cmds counting block semaphore
                    self._clearCmdsBlockedState()
            except BaseException:
                return

    def isConfigDataValid(self) -> bool:
        ##
        # @brief  Check if the configuration data is valid
        # @return True if configuration data is valid, False otherwise
        #
        if self._itchiConfig is not None:
            return self._itchiConfig.isConfigDataValid()

        return False

    def setOrtiFilePath(self, filePathStr: str) -> bool:
        ##
        # @brief  Set ORTI file path
        # @return True if file path is valid and file exists, False otherwise
        #
        if filePathStr:
            try:
                filePath = pathlib.Path(filePathStr)
                if filePath.is_file():
                    self._itchiConfig.setOrtiFilePath(filePath)
                    return True
            except BaseException:
                return False

        return False

    def getOrtiFilePath(self) -> str:
        ortiFilePath = self._itchiConfig.getOrtiFilePath()
        return str(ortiFilePath)

    def setPxmlFilePath(self, filePathStr: str) -> bool:
        ##
        # @brief  Set Profiler XMl file path
        # @return True if file path is valid and directory exists (file will be
        #         created), False otherwise
        bFilePathValid = False

        if filePathStr:
            filePath = pathlib.Path(filePathStr)
            dirPath = filePath.resolve().parent
            if dirPath.exists():
                bFilePathValid = True
                self._itchiConfig.setPxmlFilePath(filePath)

        return bFilePathValid

    def getPxmlFilePath(self) -> str:
        pxmlFilePath = self._itchiConfig.getPxmlFilePath()
        pxmlFilePathStr = str(pxmlFilePath)
        if not pxmlFilePathStr:
            pxmlFilePathStr = "profiler.xml"
        return pxmlFilePathStr

    def getCmdConfigSections(self, cmdKey: str) -> typing.List[str]:
        ##
        # @brief  Get configuration sections that need to be configured by the
        #         user for specified command
        # @param  cmdKey Name of the command
        # @return A list of configuration sections associated with the command
        #
        return self._itchiConfig.getCmdConfigSections(cmdKey)

    def _getConfigSectionAttributeType(self, configSectionKey: str, attributeKey: str) -> EConfigSectionAttributeType:
        ##
        # @brief  Get type of an attribute
        # @param  configSectionKey Name of the configuration section
        # @param  attributeKey     Name of the attribute
        # @return Attribute type in form of EConfigSectionAttributeType
        attrType = self._itchiConfig.getAttributeType(configSectionKey, attributeKey)
        TWO_COLUMN_TYPES = [Dict[int, int], Dict[str, int], Dict[int, str], Dict[str, str]]
        ONE_COLUMN_TYPES = [List[str]]

        guiAttrType = EConfigSectionAttributeType.Basic
        if attrType == bool:
            guiAttrType = EConfigSectionAttributeType.Boolean
        elif isinstance(attrType, enum.EnumMeta):
            guiAttrType = EConfigSectionAttributeType.Enum
        elif attrType == pathlib.Path:
            guiAttrType = EConfigSectionAttributeType.Path
        elif attrType in ONE_COLUMN_TYPES:
            guiAttrType = EConfigSectionAttributeType.IterableOneColumn
        elif attrType in TWO_COLUMN_TYPES:
            guiAttrType = EConfigSectionAttributeType.IterableTwoColumns
        elif attrType in [str, int]:
            pass
        else:
            print(f"Unknown ConfigSectionAttributeType {attrType}. Default to basic.")

        return guiAttrType

    def getConfigSectionAttributes(self, configSectionKey: str) -> List[ConfigSectionAttribute]:
        ##
        # @brief  For a configuration section get a list of its attributes, their types and values
        # @param  configSectionKey Name of the configuration section
        # @return A list of dictionaries that contains and attribute, its type and value
        #         [{'name': attributeName, 'type': attributeType, 'value': attributeValue}, ...]
        #

        configSectionAttrTypeList = []
        attributes = self._itchiConfig.getConfigSectionAttributes(configSectionKey)
        for attributeName in attributes:
            attributeType = self._getConfigSectionAttributeType(configSectionKey, attributeName)
            attributeValue = self._itchiConfig.getConfigSectionAttributeValue(configSectionKey, attributeName)
            attribute = ConfigSectionAttribute(attributeName, attributeType, attributeValue)

            if isinstance(attributeValue, dict):
                attribute.value = attributeValue.items()
            elif isinstance(attributeValue, enum.Enum):
                attribute.value = attributeValue
            elif isinstance(attributeValue, pathlib.Path):
                if attributeValue == pathlib.Path(""):
                    attribute.value = ""
                else:
                    attribute.value = str(attributeValue)
            configSectionAttrTypeList.append(attribute)

        return configSectionAttrTypeList

    def setConfigSectionAttribute(self, configSectionKey: str, attributeKey: str, value: typing.Any):
        ##
        # @brief Set value to the attribute
        # @param configSectionKey Name of the configuration section
        # @param attributeKey     Name of the attribute
        # @param value            Value to be set to attribute
        #

        # Cast value back to the expected type and save it in model
        attrTypeUI = self._getConfigSectionAttributeType(configSectionKey, attributeKey)
        if attrTypeUI in (EConfigSectionAttributeType.IterableOneColumn, EConfigSectionAttributeType.IterableTwoColumns):
            attrType = self._itchiConfig.getAttributeType(configSectionKey, attributeKey)
            if value:
                valueStr = "[" + value + "]" if typing.get_origin(attrType) is list else "{" + value + "}"
                valueList: List = ast.literal_eval(valueStr)
            else:
                valueList = [] if typing.get_origin(attrType) is list else {}
            self._itchiConfig.setConfigSectionAttributeValue(configSectionKey, attributeKey, valueList)
        else:
            self._itchiConfig.setConfigSectionAttributeValue(configSectionKey, attributeKey, value)

    def isConfigSectionAlsoAttribute(self, configSectionKey: str) -> bool:
        if not configSectionKey:
            return False

        return self._itchiConfig.isConfigSectionAlsoAttribute(configSectionKey)

    def wasCmdPreviouslySelected(self, cmdKey: str) -> bool:
        commandDictList = self.getConfigSectionAttributes("commands")
        cmdIdx = next((index for (index, d) in enumerate(commandDictList) if d.name == cmdKey), None)
        if (cmdIdx is not None) and (commandDictList[cmdIdx].value is True):
            return True

        return False

    def saveSelectedCommands(self, selectedCmdKeyList: typing.List[str]):
        # Set all commands to false -> if they were previously selected
        for cmd in self.getConfigSectionAttributes("commands"):
            cmdSelected = True if cmd.name in selectedCmdKeyList else False
            self.setConfigSectionAttribute("commands", cmd.name, cmdSelected)

    def set_log_file(self, log_file: str):
        self.log_file = log_file

    def runItchi(self):
        # Consolas font has charaters with the same width so that new lines are properly aligned
        out_msg = "<html><body>"
        out_msg += "<style>.pre {font-family: Consolas;}</style>"
        out_msg += "-------------------- RUNNING ITCHI --------------------"

        msg_style = ""

        b_save_success, err_msg = self._itchiConfig.saveConfigFileData()
        if b_save_success:
            config_file_path = str(self._itchiConfig.getConfigFilePath())

            parser = itchi_cli.create_parser()
            captured_output = io.StringIO()
            sys.stdout = captured_output
            itchi_cli.main(parser.parse_args(['--config', config_file_path,
                                              '--log_file', self.log_file]))

            msg = f"<pre>{captured_output.getvalue()}</pre>"
            sys.stdout = sys.__stdout__
        else:
            msg_style = "style='color:red;'"
            msg = "There was a problem with saving configuration data\n"
            msg += err_msg

        out_msg += f"<pre {msg_style}>{msg}</pre>"
        out_msg += "</body></html>"

        return out_msg

    def getLogFileData(self):
        # Log file is located in the same folder as .json config file (current directory)
        try:
            with open(self.log_file, mode="r", encoding="utf-8") as f:
                logData = f.read()
        except Exception as ex:
            logData = f"FAILED: {ex}"

        return logData

    def getCmdHelp(self, cmdKey: str) -> str:
        def get_element_tag_priority(element: xml.etree.ElementTree.Element) -> str:
            html_element_tag_order = ["div", "p", "h4", "h3", "h2", "h1"]

            element_tag = element.tag.split("}")[-1] if '}' in element.tag else element.tag
            tag_priority = html_element_tag_order.index(element_tag) if element_tag in html_element_tag_order else -1

            return str(tag_priority)

        command_help_html = ""

        if cmdKey in self.cmds:
            command_html_element_id = self.cmds[cmdKey].htmlElementId
            if command_html_element_id:
                command_header_element = self._itchiHelp.findElementById(command_html_element_id)

                if command_header_element is not None:
                    command_help_html += xml.etree.ElementTree.tostring(command_header_element,
                                                                        method='html', encoding="unicode")

                    # Search and use all elements between headers of the same type
                    # Eg. h3 (running-taskisr) -> h3 (running-taskisr-tracing-with-btf-export) =>
                    # get all other in between and show them as help for Running Task/ISR command
                    header_element_tag_priority = get_element_tag_priority(command_header_element)
                    current_element = self._itchiHelp.findElementsNextSibling(command_header_element)
                    while current_element is not None:
                        current_element_tag_priority = get_element_tag_priority(current_element)
                        if current_element_tag_priority >= header_element_tag_priority:
                            break

                        command_help_html += xml.etree.ElementTree.tostring(current_element,
                                                                            method='html', encoding="unicode")
                        current_element = self._itchiHelp.findElementsNextSibling(current_element)

        command_group_help_html = f"<html><head>{self._itchiHelp.getStyleTags()}</head><body>"
        command_group_help_html += command_help_html
        command_group_help_html += "</body></html>"

        # Remove all "html:" prefixes before tags - Qt doesn't properly render the html otherwise
        command_group_help_html = command_group_help_html.replace("html:", "")

        return command_group_help_html

    def getAttributesHelp(self, cfgSectionsList: List[str]) -> Tuple[List[str], List[List[str]]]:
        def get_element_tag(element: xml.etree.ElementTree) -> str:
            element_tag = element.tag.split("}")[-1] if '}' in element.tag else element.tag
            return element_tag

        cfg_attr_html_tag = self._itchiHelp.findElementById("config-attributes")
        if (cfg_attr_html_tag is None) or (get_element_tag(cfg_attr_html_tag) != "h3"):
            return ([], [])

        cfg_attr_html_table = self._itchiHelp.findElementsNextSibling(cfg_attr_html_tag)
        if (cfg_attr_html_table is None) or (get_element_tag(cfg_attr_html_table) != "table"):
            return ([], [])

        # Get the names of table's columns
        header_element = cfg_attr_html_table.find('.//{*}thead').find(".//{*}tr")
        column_names = []
        for element in header_element.iter():
            if get_element_tag(element) == "th":
                column_names.append(element.text)

        # Extract data from the table
        body_element = cfg_attr_html_table.find('.//{*}tbody')
        cells_data = []
        rows = (element for element in body_element.iter() if get_element_tag(element) == "tr")
        for tr_element in rows:
            row_data: List[str] = []
            columns = (element for element in tr_element.iter() if get_element_tag(element) == "td")
            for td_element in columns:
                if len(row_data) == len(column_names):
                    break

                row_data.append(td_element.text)
            cells_data.append(row_data)

        # Filter data to only show the relevant sections
        cells_data_shown = []
        for cellData in cells_data:
            attr_cfg_section_name = cellData[0].split(" ")[0]
            if attr_cfg_section_name in cfgSectionsList:
                cells_data_shown.append(cellData)

        return (column_names, cells_data_shown)
