import os
import itchi.config as config
import typing
import xml.etree.ElementTree
import pathlib


class ItchiConfig:
    ##
    # @brief A list of supported commands and their configuration sections bindings
    #        (which sections have to be configured if the command is used)
    #
    itchiRunFilePath = pathlib.Path()

    _cmdConfigSectionsBinding = {
        "running_taskisr": ["running_taskisr"],
        "running_taskisr_btf": ["running_taskisr"],
        "running_taskisr_sampling": ["running_taskisr"],
        "task_state_single_variable": ["running_taskisr", "task_state"],
        "task_state_complex_expression": ["running_taskisr", "task_state", "task_state_inspectors"],
        "task_state_complex_native": ["running_taskisr", "task_state_complex"],
        "task_state_instrumentation_microsar": ["task_state_inst_microsar"],
        "task_state_instrumentation_autocore": ["task_state_inst_autocore"],
        "runnable_instrumentation": ["runnable_instrumentation"],
        "runnable_program_flow": ["runnable_program_flow"],
        "signals": ["signals"],
        "spinlock_instrumentation_microsar": ["spinlock_inst_microsar"],
    }

    def __init__(self, configFilePath: pathlib.Path):
        ##
        # @brief Class constructor
        # @param configFilePath path to the configuration (.json) file
        #
        self._oldConfig = config.ItchiConfig.default_factory()
        self._newConfig = config.ItchiConfig.default_factory()
        self._defaultConfig = config.ItchiConfig.default_factory()
        self._configDataValid = True
        self._configFilePath = pathlib.Path(configFilePath)

    @classmethod
    def isItchiRunFilePathValid(cls) -> bool:
        """
        @deprecated itchi should be installed as a mython package and run as a module
        """
        itchiRunFilePathValid = False

        # Check for iTCHi executable - assuming exe is located in the same folder as this document
        itchiExeFilePath = pathlib.Path(__file__).resolve().parents[1].joinpath("itchi-bin.exe")
        if itchiExeFilePath.exists():
            cls.itchiRunFilePath = itchiExeFilePath
            itchiRunFilePathValid = True
        else:
            # Check if itchi.py exists (used under debug)
            itchiPyFilePath = pathlib.Path(__file__).resolve().parents[1].joinpath("itchi_cli.py")
            if itchiPyFilePath.exists():
                cls.itchiRunFilePath = itchiPyFilePath
                itchiRunFilePathValid = True

        return itchiRunFilePathValid

    @classmethod
    def getItchiRunFilePath(cls) -> pathlib.Path:
        """
        @deprecated itchi should be called as module
        """
        return cls.itchiRunFilePath

    def getConfigFilePath(self) -> pathlib.Path:
        return self._configFilePath

    @classmethod
    def createDefaultConfigFile(cls, configFilePath: pathlib.Path):
        config.write_default_config(configFilePath)

    def loadConfigFileData(self) -> bool:
        ##
        # @brief  Load configuration data from file specified at object instantiation
        # @return True if configuration data was successfully loaded and is valid else False
        #
        try:
            self._oldConfig = config.load_config(self._configFilePath)
            self._configDataValid = True
        except BaseException:
            self._configDataValid = False

        return self._configDataValid

    def saveConfigFileData(self) -> typing.Tuple[bool, str]:
        ##
        # @brief  Save configuration data in file whose path was specified at object instantiation
        # @return A tuple of (True, "") if data was successfully saved else (False, exceptionString)
        #
        bFileSavedSuccess = False
        errMsg = ""

        if self._configDataValid:
            try:
                configData = config.ItchiConfig(**self._newConfig.model_dump())
                with open(self._configFilePath, mode="w", encoding="utf-8") as f:
                    f.write(configData.model_dump_json(indent=4))

                bFileSavedSuccess = True
            except Exception as ex:
                errMsg = str(ex)

        return (bFileSavedSuccess, errMsg)

    def isConfigDataValid(self) -> bool:
        ##
        # @brief  Check if the configured data is valid
        # @return True if configured data is valid else False
        #
        return self._configDataValid

    def getCmds(self) -> typing.List[str]:
        ##
        # @brief  Get a list of cmds that iTCHi currently supports
        # @return A list of supported commands
        #
        return list(ItchiConfig._cmdConfigSectionsBinding.keys())

    def getOrtiFilePath(self) -> pathlib.Path:
        return self._oldConfig.orti_file

    def setOrtiFilePath(self, filePath: pathlib.Path):
        self._newConfig.orti_file = filePath

    def getPxmlFilePath(self) -> pathlib.Path:
        return self._oldConfig.profiler_xml_file

    def setPxmlFilePath(self, filePath: pathlib.Path):
        self._newConfig.profiler_xml_file = filePath

    def isConfigSectionAlsoAttribute(self, configSectionKey: str):
        if hasattr(self._defaultConfig, configSectionKey) and type(getattr(self._defaultConfig, configSectionKey)) in (str, list):
            return True

        return False

    def getCmdConfigSections(self, cmdKey: str) -> typing.List[str]:
        ##
        # @brief  Get configuration sections that need to be configured by the user for specified command
        # @param  cmdKey Name of the command
        # @return A list of configuration sections associated with the command
        #
        return ItchiConfig._cmdConfigSectionsBinding[cmdKey]

    def getConfigSectionAttributes(self, configSectionKey: str) -> typing.List[str]:
        ##
        # @brief  Get attributes of the specified configuration section
        # @param  configSectionKey Name of the configuration section
        # @return A list of attributes in configuration section
        #
        attributesList = []
        if self.isConfigSectionAlsoAttribute(configSectionKey):
            attributesList = [configSectionKey]
        else:
            configSectionObj = getattr(self._defaultConfig, configSectionKey)
            if configSectionObj:
                attributesList = configSectionObj.dict().keys()

        return attributesList

    def getConfigSectionAttributeValue(self, configSectionKey: str, attributeKey: str) -> typing.Any:
        ##
        # @brief  Get value of the attribute in configuration section
        # @param  configSectionKey Name of the configuration section
        # @param  attributeKey     Name of the attribute
        # @return Value of the attribute
        #

        # Get attribute value from the old configuration file (if available) or
        # from the default configuration
        if self.isConfigSectionAlsoAttribute(configSectionKey):
            config = self._oldConfig if hasattr(self._oldConfig, configSectionKey) else self._defaultConfig
            attributeValue = getattr(config, attributeKey)
        else:
            config = self._defaultConfig
            if hasattr(self._oldConfig, configSectionKey):
                if hasattr(getattr(self._oldConfig, configSectionKey), attributeKey):
                    config = self._oldConfig
            configSectionObj = getattr(config, configSectionKey)
            attributeValue = getattr(configSectionObj, attributeKey)
        return attributeValue

    def setConfigSectionAttributeValue(self, configSectionKey: str, attributeKey: str, value: typing.Any):
        ##
        # @brief Set value of the attribute in configuration section
        # @param configSectionKey Name of the configuration section
        # @param attributeKey     Name of the attribute
        # @param value            Value to be set
        #
        if self.isConfigSectionAlsoAttribute(configSectionKey):
            setattr(self._newConfig, configSectionKey, value)
        else:
            configSectionObj = getattr(self._newConfig, configSectionKey)
            setattr(configSectionObj, attributeKey, value)

    def getAttributeType(self, configSectionKey: str, attributeKey: str) -> typing.Any:
        ##
        # @brief  Get type hint of an attribute
        # @param  configSectionKey Name of the configuration section
        # @param  attributeKey     Name of the attribute
        # @return Attribute type by using get_type_hints()
        #
        if self.isConfigSectionAlsoAttribute(configSectionKey):
            attributeType = typing.get_type_hints(self._defaultConfig)[attributeKey]
        else:
            configSectionObj = getattr(self._defaultConfig, configSectionKey)
            attributeType = typing.get_type_hints(configSectionObj)[attributeKey]

        return attributeType


class ItchiHelp:
    _html_file_path  = os.path.normpath(os.path.join(os.path.dirname(__file__), 'readme.html'))

    @classmethod
    def isHtmlFilePathValid(cls) -> bool:
        return os.path.exists(cls._html_file_path)

    @classmethod
    def getHtmlFilePath(cls) -> str:
        return cls._html_file_path

    def __init__(self) -> None:
        ##
        # @brief Class constructor
        #
        if not ItchiHelp.isHtmlFilePathValid():
            return

        self._root = xml.etree.ElementTree.parse(str(ItchiHelp.getHtmlFilePath()))

        # Get style tags from html header to be applied later for nicer formatting
        self._styleTags = ""
        if self._root is not None:
            header = self._root.find('.//{http://www.w3.org/1999/xhtml}head')

            if header is not None:
                style_tag = header.find('.//{http://www.w3.org/1999/xhtml}style')
                self._styleTags = xml.etree.ElementTree.tostring(style_tag, encoding='unicode')

    def findElementById(self, elementId: str):
        element = None

        if ItchiHelp.isHtmlFilePathValid():
            try:
                element = self._root.find(f".//*[@id=\"{elementId}\"]")
            except BaseException:
                element = None

        return element

    def findElementsNextSibling(self, element):
        next_element = None

        if ItchiHelp.isHtmlFilePathValid() and element is not None:
            # Find the current element, get its iterator and return the next one
            iterator = self._root.iter()
            for elem in iterator:
                if elem == element:
                    # Get the next 'same-level' element. Skips all subelements of this tag as they are already included
                    # when using the .tostring method
                    try:
                        num_subelements = len(list(elem.iter()))
                        for _ in range(num_subelements):
                            next_element = next(iterator)
                    except StopIteration:
                        break
                    break

        return next_element

    def getStyleTags(self) -> str:
        return self._styleTags if ItchiHelp.isHtmlFilePathValid() else ""
