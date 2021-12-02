# -*- coding: utf-8 -*-
"""Project and solution file writer classes."""

import abc
import re

from vstools import definitions


class FileWriter(object):
  """File writer."""

  def __init__(self, encoding='utf-8', end_of_line='\r\n'):
    """Initializes a file writer.

    Args:
      encoding (str): encoding.
      end_of_line (str): end of line.
    """
    super(FileWriter, self).__init__()
    self._encoding = encoding
    self._end_of_line = end_of_line
    self._file = None

  def Close(self):
    """Closes the project file."""
    self._file.close()

  def Open(self, filename):
    """Opens the project file.

    Args:
      filename (str): path of the file.
    """
    # Using binary mode to make sure to write Windows/DOS end of lines.
    self._file = open(filename, 'wb')  # pylint: disable=consider-using-with

  def WriteBinaryData(self, data):
    """Writes binary data.

    Args:
      data (bytes): binary data.
    """
    self._file.write(data)

  def WriteLine(self, line):
    """Writes a line."""
    line = ''.join([line, self._end_of_line])
    line = line.encode(self._encoding)
    self.WriteBinaryData(line)

  def WriteLines(self, lines):
    """Writes lines."""
    for line in lines:
      self.WriteLine(line)


class VSProjectFileWriter(FileWriter):
  """Visual Studio project file writer."""

  def __init__(self, encoding='utf-8', end_of_line='\r\n'):
    """Initializes a Visual Studio project file writer.

    Args:
      encoding (str): encoding.
      end_of_line (str): end of line.
    """
    super(VSProjectFileWriter, self).__init__(
        encoding=encoding, end_of_line=end_of_line)

  @abc.abstractmethod
  def WriteFooter(self):
    """Writes a file footer."""

  @abc.abstractmethod
  def WriteHeader(self):
    """Writes a file header."""


class VS2008ProjectFileWriter(VSProjectFileWriter):
  """Visual Studio 2008 project file writer."""

  _CONFIGURATION_OPTIONS = [
      ('ConfigurationType', 'output_type', False),
      ('CharacterSet', 'character_set', False),
      ('ManagedExtensions', 'managed_extensions', True),
      ('WholeProgramOptimization', 'whole_program_optimization', True),
  ]

  _TOOL_COMPILER_CONFIGURATION_OPTIONS = [
      ('Optimization', 'optimization', True),
      ('AdditionalIncludeDirectories', 'include_directories', False),
      ('PreprocessorDefinitions', 'preprocessor_definitions', False),
      ('BasicRuntimeChecks', 'basic_runtime_checks', True),
      ('SmallerTypeCheck', 'smaller_type_check', True),
      ('RuntimeLibrary', 'runtime_library', False),
      ('UsePrecompiledHeader', 'precompiled_header', True),
      ('WarningLevel', 'warning_level', False),
      ('WarnAsError', 'warning_as_error', True),
      ('Detect64BitPortabilityProblems',
       'detect_64bit_portability_problems', True),
      ('DebugInformationFormat', 'debug_information_format', True),
      ('CompileAs', 'compile_as', False),
  ]

  _TOOL_LIBRARIAN_CONFIGURATION_OPTIONS = [
      ('OutputFile', 'librarian_output_file', False),
      ('ModuleDefinitionFile', 'librarian_module_definition_file', False),
      ('IgnoreAllDefaultLibraries', 'librarian_ignore_defaults', False),
  ]

  _TOOL_LINKER_CONFIGURATION_OPTIONS1 = [
      # ('AdditionalDependencies', 'additional_dependencies', True),
      ('OutputFile', 'linker_output_file', True),
      ('LinkIncremental', 'link_incremental', True),
  ]

  _TOOL_LINKER_CONFIGURATION_OPTIONS2 = [
      # ('AdditionalLibraryDirectories', 'library_directories', False),
      ('GenerateDebugInformation', 'generate_debug_information', True),
      ('SubSystem', 'sub_system', True),
      ('OptimizeReferences', 'optimize_references', True),
      ('EnableCOMDATFolding', 'enable_comdat_folding', True),
      ('RandomizedBaseAddress', 'randomized_base_address', True),
      ('DataExecutionPrevention', 'data_execution_prevention', True),
      ('TargetMachine', 'target_machine', True),
      ('ImportLibrary', 'import_library', True),
  ]

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2008ProjectFileWriter, self).__init__()
    self._version = 2008

  def _WriteConfiguration(self, project_configuration):
    """Writes the project configuration.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self.WriteLine('\t\t<Configuration')

    self.WriteLine('\t\t\tName="{0:s}|{1:s}"'.format(
        project_configuration.name, project_configuration.platform))

    self.WriteLines([
        '\t\t\tOutputDirectory="$(SolutionDir)$(ConfigurationName)"',
        '\t\t\tIntermediateDirectory="$(ConfigurationName)"'])

    for definition, name, is_optional in self._CONFIGURATION_OPTIONS:
      self._WriteConfigurationOption(
          project_configuration, definition, name, is_optional, 3)

    self.WriteLine('\t\t\t>')

    tools = [
        ('VCPreBuildEventTool', []),
        ('VCCustomBuildTool', []),
        ('VCXMLDataGeneratorTool', []),
        ('VCWebServiceProxyGeneratorTool', []),
        ('VCMIDLTool', []),
        ('VCCLCompilerTool', self._TOOL_COMPILER_CONFIGURATION_OPTIONS),
        ('VCManagedResourceCompilerTool', []),
        ('VCResourceCompilerTool', []),
        ('VCPreLinkEventTool', []),
    ]
    # TODO: add "librarian values set" to project configuration?
    if project_configuration.librarian_output_file:
      tool = ('VCLibrarianTool', self._TOOL_LIBRARIAN_CONFIGURATION_OPTIONS)
      tools.append(tool)

    for name, configuration_options in tools:
      self._WriteConfigurationTool(
          project_configuration, name, configuration_options)

    if project_configuration.linker_values_set:
      self._WriteConfigurationLinkerTool(project_configuration)

    tools = [('VCALinkTool', [])]

    if project_configuration.linker_values_set:
      tools.append(('VCManifestTool', []))

    tools.extend([
        ('VCXDCMakeTool', []),
        ('VCBscMakeTool', []),
        ('VCFxCopTool', [])
    ])

    if project_configuration.linker_values_set:
      tools.append(('VCAppVerifierTool', []))

    tools.append(('VCPostBuildEventTool', []))

    for name, configuration_options in tools:
      self._WriteConfigurationTool(
          project_configuration, name, configuration_options)

    self.WriteLine('\t\t</Configuration>')

  def _WriteConfigurationLinkerTool(self, project_configuration):
    """Writes the project configuration linker tool.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self._WriteConfigurationToolHeader('VCLinkerTool')

    if project_configuration.additional_dependencies:
      self.WriteLine('\t\t\t\tAdditionalDependencies="{0:s}"'.format(
          ' '.join(sorted(project_configuration.additional_dependencies))))

    for definition, name, is_optional in (
        self._TOOL_LINKER_CONFIGURATION_OPTIONS1):
      self._WriteConfigurationOption(
          project_configuration, definition, name, is_optional, 4)

    library_directories = ['&quot;$(OutDir)&quot;']
    library_directories.extend(project_configuration.library_directories)
    library_directories = ';'.join(library_directories)

    self.WriteLine('\t\t\t\tAdditionalLibraryDirectories="{0:s}"'.format(
        library_directories))

    for definition, name, is_optional in (
        self._TOOL_LINKER_CONFIGURATION_OPTIONS2):
      self._WriteConfigurationOption(
          project_configuration, definition, name, is_optional, 4)

    self._WriteConfigurationToolFooter()

  def _WriteConfigurationOption(
      self, project_configuration, definition, name, is_optional,
      indentation_level):
    """Parses a configuration option.

    An optional configuration option will not be written when its configuration
    value is not set.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
      definition (str): definition of the configuration value in file.
      name (str): name of the configuration value in the project information.
      is_optional (bool): True if the configuration option is optional.
      indentation_level (int): indentation level.
    """
    configuration_value = getattr(project_configuration, name, '')
    if name == 'include_directories':
      configuration_value = ';'.join(configuration_value)

    if not is_optional or configuration_value:
      indentation = '\t' * indentation_level
      line = '{0:s}{1:s}="{2:s}"'.format(
          indentation, definition, configuration_value)
      self.WriteLine(line)

  def _WriteConfigurationTool(
      self, project_configuration, name, configuration_options):
    """Writes a project configuration tool.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
      name (str): name of the tool.
      configuration_options (list[tuple[str, str, bool]]): configuration
          options defined as a tuple of definition, name and is optional.
    """
    self._WriteConfigurationToolHeader(name)

    # pylint: disable=redefined-argument-from-local
    for definition, name, is_optional in configuration_options:
      self._WriteConfigurationOption(
          project_configuration, definition, name, is_optional, 4)

    self._WriteConfigurationToolFooter()

  def _WriteConfigurationToolFooter(self):
    """Writes the project configuration tool footer."""
    self.WriteLine('\t\t\t/>')

  def _WriteConfigurationToolHeader(self, name):
    """Writes the project configuration tool header.

    Args:
      name (str): name of the tool.
    """
    self.WriteLines([
        '\t\t\t<Tool',
        '\t\t\t\tName="{0:s}"'.format(name)])

  def _WriteHeaderFiles(self, header_files):
    """Writes the header files.

    Args:
      header_files (list[str]): header filenames.
    """
    self.WriteLines([
        '\t\t<Filter',
        '\t\t\tName="Header Files"',
        '\t\t\tFilter="h;hpp;hxx;hm;inl;inc;xsd"',
        '\t\t\tUniqueIdentifier="{93995380-89BD-4b04-88EB-625FBE52EBFB}"',
        '\t\t\t>'])

    for filename in header_files:
      self.WriteLine('\t\t\t<File')

      self.WriteLine('\t\t\t\tRelativePath="{0:s}"'.format(filename))

      self.WriteLines([
          '\t\t\t\t>',
          '\t\t\t</File>'])

    self.WriteLine('\t\t</Filter>')

  def _WriteResourceFiles(self, resource_files):
    """Writes the resource files.

    Args:
      resource_files (list[str]): resource filenames.
    """
    self.WriteLines([
        '\t\t<Filter',
        '\t\t\tName="Resource Files"',
        ('\t\t\tFilter="rc;ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe;'
         'resx;tiff;tif;png;wav"'),
        '\t\t\tUniqueIdentifier="{67DA6AB6-F800-4c08-8B7A-83BB121AAD01}"',
        '\t\t\t>'])

    for filename in resource_files:
      self.WriteLine('\t\t\t<File')

      self.WriteLine('\t\t\t\tRelativePath="{0:s}"'.format(filename))

      self.WriteLines([
          '\t\t\t\t>',
          '\t\t\t</File>'])

    self.WriteLine('\t\t</Filter>')

  def _WriteSourceFiles(self, source_files):
    """Writes the source files.

    Args:
      source_files (list[str]): source filenames.
    """
    self.WriteLines([
        '\t\t<Filter',
        '\t\t\tName="Source Files"',
        '\t\t\tFilter="cpp;c;cc;cxx;def;odl;idl;hpj;bat;asm;asmx"',
        '\t\t\tUniqueIdentifier="{4FC737F1-C7A5-4376-A066-2A32D752A2FF}"',
        '\t\t\t>'])

    for filename in source_files:
      self.WriteLine('\t\t\t<File')

      self.WriteLine('\t\t\t\tRelativePath="{0:s}"'.format(filename))

      self.WriteLines([
          '\t\t\t\t>',
          '\t\t\t</File>'])

    self.WriteLine('\t\t</Filter>')

  def WriteConfigurations(self, project_configurations):
    """Writes the configurations.

    Args:
      project_configurations (VSConfigurations): configurations.
    """
    self.WriteLine('\t<Configurations>')

    for project_configuration in project_configurations.GetSorted():
      self._WriteConfiguration(project_configuration)

    self.WriteLine('\t</Configurations>')

    self.WriteLines([
        '\t<References>',
        '\t</References>'])

  # pylint: disable=unused-argument
  def WriteDependencies(self, dependencies, solution_projects_by_guid):
    """Writes the dependencies.

    Args:
      dependencies (list[str]): GUIDs of the dependencies.
      solution_projects_by_guid (dict[str, VSSolutionProject]): projects
          per lower case GUID.
    """
    return

  def WriteFiles(self, source_files, header_files, resource_files):
    """Writes the files.

    Args:
      source_files (list[str]): source filenames.
      header_files (list[str]): header filenames.
      resource_files (list[str]): resource filenames.
    """
    self.WriteLine('\t<Files>')

    self._WriteSourceFiles(source_files)
    self._WriteHeaderFiles(header_files)
    self._WriteResourceFiles(resource_files)

    self.WriteLine('\t</Files>')

    self.WriteLines([
        '\t<Globals>',
        '\t</Globals>'])

  def WriteFooter(self):
    """Writes a file footer."""
    self.WriteLine('</VisualStudioProject>')

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteLine('<?xml version="1.0" encoding="Windows-1252"?>')

  # pylint: disable=unused-argument
  def WriteProjectConfigurations(self, project_configurations):
    """Writes the project configurations.

    Args:
      project_configurations (VSConfigurations): configurations.
    """
    return

  def WriteProjectInformation(self, project_information):
    """Writes the project information.

    Args:
      project_information (VSProjectInformation): project information.
    """
    self.WriteLines([
        '<VisualStudioProject',
        '\tProjectType="Visual C++"',
        '\tVersion="9,00"'])

    self.WriteLine('\tName="{0:s}"'.format(project_information.name))

    self.WriteLine('\tProjectGUID="{{{0:s}}}"'.format(
        project_information.guid.upper()))

    self.WriteLine(
        '\tRootNamespace="{0:s}"'.format(project_information.root_name_space))

    if project_information.keyword:
      self.WriteLine(
          '\tKeyword="{0:s}"'.format(project_information.keyword))

    # Also seen 196613.
    self.WriteLines([
        '\tTargetFrameworkVersion="131072"',
        '\t>'])

    # TODO: handle platforms.
    self.WriteLines([
        '\t<Platforms>',
        '\t\t<Platform',
        '\t\t\tName="Win32"',
        '\t\t/>',
        '\t</Platforms>'])

    self.WriteLines([
        '\t<ToolFiles>',
        '\t</ToolFiles>'])


class VS2010ProjectFileWriter(VSProjectFileWriter):
  """Visual Studio 2010 project file writer."""

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2010ProjectFileWriter, self).__init__()
    self._project_file_version = '10.0.40219.1'
    self._tools_version = '4.0'
    self._version = 2010

  def _WriteClCompileSection(self, project_configuration):
    """Writes the CLCompile section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    include_directories = ';'.join(project_configuration.include_directories)

    include_directories = re.sub(r'&quot;', r'', include_directories)

    if include_directories and include_directories[-1] != ';':
      include_directories = '{0:s};'.format(
          include_directories)

    include_directories = '{0:s}%(AdditionalIncludeDirectories)'.format(
        include_directories)

    preprocessor_definitions = project_configuration.preprocessor_definitions

    if preprocessor_definitions and preprocessor_definitions[-1] != ';':
      preprocessor_definitions = '{0:s};'.format(preprocessor_definitions)

    preprocessor_definitions = '{0:s}%(PreprocessorDefinitions)'.format(
        preprocessor_definitions)

    self.WriteLine('    <ClCompile>')

    if project_configuration.optimization != '':
      self.WriteLine('      <Optimization>{0:s}</Optimization>'.format(
          project_configuration.optimization_string))

    if project_configuration.enable_intrinsic_functions != '':
      self.WriteLine((
          '      <IntrinsicFunctions>{0:s}</IntrinsicFunctions>').format(
              project_configuration.enable_intrinsic_functions))

    if project_configuration.whole_program_optimization:
      self.WriteLine((
          '      <WholeProgramOptimization>{0:s}'
          '</WholeProgramOptimization>').format(
              project_configuration.whole_program_optimization_string))

    self.WriteLine((
        '      <AdditionalIncludeDirectories>{0:s}'
        '</AdditionalIncludeDirectories>').format(include_directories))

    self.WriteLine((
        '      <PreprocessorDefinitions>{0:s}'
        '</PreprocessorDefinitions>').format(preprocessor_definitions))

    if project_configuration.basic_runtime_checks != '':
      self.WriteLine((
          '      <BasicRuntimeChecks>{0:s}'
          '</BasicRuntimeChecks>').format(
              project_configuration.basic_runtime_checks_string))

    if project_configuration.smaller_type_check != '':
      self.WriteLine((
          '      <SmallerTypeCheck>{0:s}</SmallerTypeCheck>').format(
              project_configuration.smaller_type_check))

    self.WriteLine((
        '      <RuntimeLibrary>{0:s}</RuntimeLibrary>').format(
            project_configuration.runtime_librarian_string))

    if project_configuration.enable_function_level_linking != '':
      self.WriteLine((
          '      <FunctionLevelLinking>{0:s}</FunctionLevelLinking>').format(
              project_configuration.enable_function_level_linking))

    if project_configuration.precompiled_header != '':
      # A value of 0 is represented by a new line.
      if project_configuration.precompiled_header == '0':
        self.WriteLines([
            '      <PrecompiledHeader>',
            '      </PrecompiledHeader>'])
      else:
        self.WriteLine((
            '      <PrecompiledHeader>{0:s}</PrecompiledHeader>').format(
                project_configuration.precompiled_header_string))

    self.WriteLine('      <WarningLevel>{0:s}</WarningLevel>'.format(
        project_configuration.warning_level_string))

    if project_configuration.warning_as_error:
      self.WriteLine((
          '      <TreatWarningAsError>{0:s}'
          '</TreatWarningAsError>').format(
              project_configuration.warning_as_error))

    if project_configuration.debug_information_format != '':
      # A value of 0 is represented by a new line.
      if project_configuration.debug_information_format == '0':
        self.WriteLines([
            '      <DebugInformationFormat>',
            '      </DebugInformationFormat>'])
      else:
        self.WriteLine((
            '      <DebugInformationFormat>{0:s}'
            '</DebugInformationFormat>').format(
                project_configuration.debug_information_format_string))

    if project_configuration.compile_as:
      self.WriteLine('      <CompileAs>{0:s}</CompileAs>'.format(
          project_configuration.compile_as_string))

    self.WriteLine('    </ClCompile>')

  def _WriteConfigurationPropertyGroup(self, project_configuration):
    """Writes the configuration property group.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self._WriteConfigurationPropertyGroupHeader(project_configuration)

    self.WriteLine('    <ConfigurationType>{0:s}</ConfigurationType>'.format(
        project_configuration.output_type_string))

    if project_configuration.character_set:
      self.WriteLine('    <CharacterSet>{0:s}</CharacterSet>'.format(
          project_configuration.character_set_string))

    if project_configuration.managed_extensions == '1':
      self.WriteLine('    <CLRSupport>true</CLRSupport>')

    if project_configuration.whole_program_optimization:
      self.WriteLine((
          '    <WholeProgramOptimization>{0:s}'
          '</WholeProgramOptimization>').format(
              project_configuration.whole_program_optimization_string))

    platform_toolset = project_configuration.GetPlatformToolset(self._version)
    if platform_toolset:
      self.WriteLine('    <PlatformToolset>{0:s}</PlatformToolset>'.format(
          platform_toolset))

    self._WriteConfigurationPropertyGroupFooter()

  def _WriteConfigurationPropertyGroupFooter(self):
    """Writes the configuration property group footer."""
    self.WriteLine('  </PropertyGroup>')

  def _WriteConfigurationPropertyGroupHeader(self, project_configuration):
    """Writes the configuration property group header.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self.WriteLine((
        '  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
        '\'{0:s}|{1:s}\'" Label="Configuration">').format(
            project_configuration.name, project_configuration.platform))

  def _WriteHeaderFiles(self, header_files):
    """Writes the header files.

    Args:
      header_files (list[str]): header filenames.
    """
    if header_files:
      self.WriteLine('  <ItemGroup>')

      for filename in header_files:
        self.WriteLine('    <ClInclude Include="{0:s}" />'.format(filename))

      self.WriteLine('  </ItemGroup>')

  def _WriteItemDefinitionGroup(self, project_configuration):
    """Writes the item definition group.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self._WriteItemDefinitionGroupHeader(project_configuration)

    # Write the compiler specific section.
    self._WriteClCompileSection(project_configuration)

    # Write the librarian specific section.
    if project_configuration.librarian_output_file:
      self._WriteLibrarianSection(project_configuration)

    # Write the linker specific section.
    if (project_configuration.linker_values_set or
        project_configuration.output_type == (
            definitions.OUTPUT_TYPE_APPLICATION)):
      self._WriteLinkerSection(project_configuration)

    self._WriteItemDefinitionGroupFooter()

  def _WriteItemDefinitionGroupFooter(self):
    """Writes the item definition group header."""
    self.WriteLine('  </ItemDefinitionGroup>')

  def _WriteItemDefinitionGroupHeader(self, project_configuration):
    """Writes the item definition group header.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self.WriteLine((
        '  <ItemDefinitionGroup Condition="\'$(Configuration)|'
        '$(Platform)\'==\'{0:s}|{1:s}\'">').format(
            project_configuration.name, project_configuration.platform))

  def _WriteLibrarianSection(self, project_configuration):
    """Writes the librarian section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    librarian_output_file = re.sub(
        r'[$][(]OutDir[)]\\', r'$(OutDir)',
        project_configuration.librarian_output_file)

    self.WriteLines([
        '    <Lib>',
        '      <OutputFile>{0:s}</OutputFile>'.format(librarian_output_file)])

    if project_configuration.module_definition_file != '':
      self.WriteLine((
          '      <ModuleDefinitionFile>{0:s}'
          '</ModuleDefinitionFile>').format(
              project_configuration.module_definition_file))
    else:
      self.WriteLines([
          '      <ModuleDefinitionFile>',
          '      </ModuleDefinitionFile>'])

    if project_configuration.librarian_ignore_defaults != '':
      self.WriteLine((
          '      <IgnoreAllDefaultLibraries>{0:s}'
          '</IgnoreAllDefaultLibraries>').format(
              project_configuration.librarian_ignore_defaults))

    self.WriteLine('    </Lib>')

  def _WriteLinkerSection(self, project_configuration):
    """Writes the linker section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self.WriteLine('    <Link>')

    # Visual Studio will convert an empty additional dependencies value.
    if project_configuration.additional_dependencies:
      additional_dependencies = ';'.join(
          sorted(project_configuration.additional_dependencies))

      additional_dependencies = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)', additional_dependencies)

      if additional_dependencies and additional_dependencies[-1] != ';':
        additional_dependencies = '{0:s};'.format(additional_dependencies)

      additional_dependencies = '{0:s}%(AdditionalDependencies)'.format(
          additional_dependencies)

      self.WriteLine((
          '      <AdditionalDependencies>{0:s}'
          '</AdditionalDependencies>').format(
              additional_dependencies))

    if project_configuration.linker_output_file:
      linker_output_file = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)',
          project_configuration.linker_output_file)

      self.WriteLine('      <OutputFile>{0:s}</OutputFile>'.format(
          linker_output_file))

      if project_configuration.module_definition_file != '':
        self.WriteLine((
            '      <ModuleDefinitionFile>{0:s}'
            '</ModuleDefinitionFile>').format(
                project_configuration.module_definition_file))

    if project_configuration.library_directories:
      library_directories = ';'.join(project_configuration.library_directories)
      library_directories = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)', library_directories)
      library_directories = re.sub(r'&quot;', r'', library_directories)

      if library_directories and library_directories[-1] != ';':
        library_directories = '{0:s};'.format(library_directories)

      library_directories = '{0:s}%(AdditionalLibraryDirectories)'.format(
          library_directories)

      self.WriteLine((
          '      <AdditionalLibraryDirectories>{0:s}'
          '</AdditionalLibraryDirectories>').format(
              library_directories))

    if project_configuration.generate_debug_information != '':
      self.WriteLine((
          '      <GenerateDebugInformation>{0:s}'
          '</GenerateDebugInformation>').format(
              project_configuration.generate_debug_information))

    if project_configuration.sub_system != '':
      self.WriteLine('      <SubSystem>{0:s}</SubSystem>'.format(
          project_configuration.sub_system_string))

    if project_configuration.optimize_references == '0':
      self.WriteLines([
          '      <OptimizeReferences>',
          '      </OptimizeReferences>'])

    elif project_configuration.optimize_references != '':
      self.WriteLine((
          '      <OptimizeReferences>{0:s}</OptimizeReferences>').format(
              project_configuration.optimize_references_string))

    if project_configuration.enable_comdat_folding == '0':
      self.WriteLines([
          '      <EnableCOMDATFolding>',
          '      </EnableCOMDATFolding>'])

    elif project_configuration.enable_comdat_folding != '':
      self.WriteLine((
          '      <EnableCOMDATFolding>{0:s}</EnableCOMDATFolding>').format(
              project_configuration.enable_comdat_folding_string))

    if project_configuration.randomized_base_address != '':
      self.WriteLine((
          '      <RandomizedBaseAddress>{0:s}'
          '</RandomizedBaseAddress>').format(
              project_configuration.randomized_base_address_string))

    if project_configuration.fixed_base_address == '0':
      self.WriteLines([
          '      <FixedBaseAddress>',
          '      </FixedBaseAddress>'])

    if project_configuration.data_execution_prevention != '':
      # A value of 0 is represented by a new line.
      if project_configuration.data_execution_prevention == '0':
        self.WriteLines([
            '      <DataExecutionPrevention>',
            '      </DataExecutionPrevention>'])
      else:
        self.WriteLine((
            '      <DataExecutionPrevention>{0:s}'
            '</DataExecutionPrevention>').format(
                project_configuration.data_execution_prevention_string))

    if project_configuration.import_library:
      import_library = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)',
          project_configuration.import_library)

      self.WriteLine('      <ImportLibrary>{0:s}</ImportLibrary>'.format(
          import_library))

    if project_configuration.target_machine != '':
      self.WriteLine('      <TargetMachine>{0:s}</TargetMachine>'.format(
          project_configuration.target_machine_string))

    self.WriteLine('    </Link>')

  def _WriteOutIntDirConditions(
      self, configuration_name, project_configurations):
    """Writes the OutDir and IntDir conditions.

    Args:
      configuration_name (str): name of the configuration.
      project_configurations (VSConfigurations): configurations.
    """
    for configuration_platform in sorted(project_configurations.platforms):
      project_configuration = project_configurations.GetByIdentifier(
          configuration_name, configuration_platform)

      if len(project_configurations.platforms) == 1:
        self.WriteLine((
            '    <OutDir Condition="\'$(Configuration)|$(Platform)\'=='
            '\'{0:s}|{1:s}\'">$(SolutionDir)$(Configuration)\\'
            '</OutDir>').format(
                project_configuration.name, project_configuration.platform))
      else:
        self.WriteLine((
            '    <OutDir Condition="\'$(Configuration)|$(Platform)\'=='
            '\'{0:s}|{1:s}\'">$(SolutionDir)$(Configuration)\\$(Platform)\\'
            '</OutDir>').format(
                project_configuration.name, project_configuration.platform))

    for configuration_platform in sorted(project_configurations.platforms):
      project_configuration = project_configurations.GetByIdentifier(
          configuration_name, configuration_platform)

      if len(project_configurations.platforms) == 1:
        self.WriteLine((
            '    <IntDir Condition="\'$(Configuration)|$(Platform)\'=='
            '\'{0:s}|{1:s}\'">$(Configuration)\\</IntDir>').format(
                project_configuration.name, project_configuration.platform))
      else:
        self.WriteLine((
            '    <IntDir Condition="\'$(Configuration)|$(Platform)\'=='
            '\'{0:s}|{1:s}\'">$(Configuration)\\$(Platform)\\</IntDir>').format(
                project_configuration.name, project_configuration.platform))

  def _WriteOutIntDirPropertyGroups(self, project_configurations):
    """Writes the OutDir and IntDir property groups.

    Args:
      project_configurations (VSConfigurations): configurations.
    """
    self.WriteLines([
        '  <PropertyGroup>',
        '    <_ProjectFileVersion>{0:s}</_ProjectFileVersion>'.format(
            self._project_file_version)])

    # Mimic Visual Studio behavior and output the configurations
    # in platforms by name.
    for configuration_name in sorted(project_configurations.names):
      self._WriteOutIntDirConditions(configuration_name, project_configurations)

      for configuration_platform in sorted(project_configurations.platforms):
        project_configuration = project_configurations.GetByIdentifier(
            configuration_name, configuration_platform)

        if project_configuration.link_incremental != '':
          self.WriteLine((
              '    <LinkIncremental Condition="\'$(Configuration)|'
              '$(Platform)\'==\'{0:s}|{1:s}\'">{2:s}</LinkIncremental>').format(
                  project_configuration.name, project_configuration.platform,
                  project_configuration.link_incremental_string))

    self.WriteLine('  </PropertyGroup>')

  def _WriteResourceFiles(self, resource_files):
    """Writes the resource files.

    Args:
      resource_files (list[str]): resource filenames.
    """
    if resource_files:
      self.WriteLine('  <ItemGroup>')

      for filename in resource_files:
        self.WriteLine('    <ResourceCompile Include="{0:s}" />'.format(
            filename))

      self.WriteLine('  </ItemGroup>')

  def _WriteSourceFiles(self, source_files):
    """Writes the source files.

    Args:
      source_files (list[str]): source filenames.
    """
    if source_files:
      self.WriteLine('  <ItemGroup>')

      for filename in source_files:
        self.WriteLine('    <ClCompile Include="{0:s}" />'.format(filename))

      self.WriteLine('  </ItemGroup>')

  def WriteConfigurations(self, project_configurations):
    """Writes the configurations.

    Args:
      project_configurations (VSConfigurations): configurations.
    """
    self.WriteLine(
        '  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.Default.props" />')

    # Mimic Visual Studio behavior and output the configurations
    # in reverse order of name.
    for project_configuration in project_configurations.GetSorted(reverse=True):
      self._WriteConfigurationPropertyGroup(project_configuration)

    self.WriteLines([
        '  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.props" />',
        '  <ImportGroup Label="ExtensionSettings">',
        '  </ImportGroup>'])

    # Mimic Visual Studio behavior and output the configurations
    # in reverse of name.
    for project_configuration in project_configurations.GetSorted(reverse=True):
      self.WriteLines([
          ('  <ImportGroup Condition="\'$(Configuration)|$(Platform)\'=='
           '\'{0:s}|{1:s}\'" Label="PropertySheets">'.format(
               project_configuration.name, project_configuration.platform)),
          ('    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform)'
           '.user.props" Condition="exists(\'$(UserRootDir)\\Microsoft.Cpp'
           '.$(Platform).user.props\')" Label="LocalAppDataPlatform" />'),
          '  </ImportGroup>'])

    self.WriteLine('  <PropertyGroup Label="UserMacros" />')

    self._WriteOutIntDirPropertyGroups(project_configurations)

    for project_configuration in project_configurations.GetSorted():
      self._WriteItemDefinitionGroup(project_configuration)

  def WriteDependencies(self, dependencies, solution_projects_by_guid):
    """Writes the dependencies.

    Args:
      dependencies (list[str]): GUIDs of the dependencies.
      solution_projects_by_guid (dict[str, VSSolutionProject]): projects
          per lower case GUID.
    """
    if dependencies:
      self.WriteLine('  <ItemGroup>')

      dependencies_by_name = {}

      # Mimic Visual Studio behavior and output the dependencies in order
      # of name (perhaps filename?).
      for dependency_guid in dependencies:
        dependency_project = solution_projects_by_guid[dependency_guid]

        dependencies_by_name[dependency_project.name] = dependency_project

      for dependency_name in sorted(dependencies_by_name):
        dependency_project = dependencies_by_name[dependency_name]

        dependency_filename = '..\\{0:s}.vcxproj'.format(
            dependency_project.filename)

        dependency_guid = dependency_project.guid.lower()

        self.WriteLines([
            ('    <ProjectReference Include="{0:s}">').format(
                dependency_filename),
            '      <Project>{{{0:s}}}</Project>'.format(dependency_guid),
            '      <ReferenceOutputAssembly>false</ReferenceOutputAssembly>',
            '    </ProjectReference>'])

      self.WriteLine('  </ItemGroup>')

  def WriteFiles(self, source_files, header_files, resource_files):
    """Writes the files.

    Args:
      source_files (list[str]): source filenames.
      header_files (list[str]): header filenames.
      resource_files (list[str]): resource filenames.
    """
    self._WriteSourceFiles(source_files)
    self._WriteHeaderFiles(header_files)
    self._WriteResourceFiles(resource_files)

  def WriteFooter(self):
    """Writes a file footer."""
    self.WriteLines([
        '  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.targets" />',
        '  <ImportGroup Label="ExtensionTargets">',
        '  </ImportGroup>'])

    # The last line has no \r\n.
    self._file.write(b'</Project>')

  def WriteHeader(self):
    """Writes a file header."""
    self._file.write(b'\xef\xbb\xbf')

    self.WriteLines([
        '<?xml version="1.0" encoding="utf-8"?>',
        ('<Project DefaultTargets="Build" ToolsVersion="{0:s}" '
         'xmlns="http://schemas.microsoft.com/developer/msbuild/2003">').format(
             self._tools_version)])

  def WriteProjectConfigurations(self, project_configurations):
    """Writes the project configurations.

    Args:
      project_configurations (VSConfigurations): configurations.
    """
    self.WriteLine('  <ItemGroup Label="ProjectConfigurations">')

    for project_configuration in project_configurations.GetSorted():
      self.WriteLine('    <ProjectConfiguration Include="{0:s}|{1:s}">'.format(
          project_configuration.name, project_configuration.platform))

      self.WriteLine('      <Configuration>{0:s}</Configuration>'.format(
          project_configuration.name))

      self.WriteLine('      <Platform>{0:s}</Platform>'.format(
          project_configuration.platform))

      self.WriteLine('    </ProjectConfiguration>')

    self.WriteLine('  </ItemGroup>')

  def WriteProjectInformation(self, project_information):
    """Writes the project information.

    Args:
      project_information (VSProjectInformation): project information.
    """
    self.WriteLine('  <PropertyGroup Label="Globals">')

    self.WriteLine('    <ProjectGuid>{{{0:s}}}</ProjectGuid>'.format(
        project_information.guid))

    self.WriteLine('    <RootNamespace>{0:s}</RootNamespace>'.format(
        project_information.root_name_space))

    if project_information.keyword:
      self.WriteLine('    <Keyword>{0:s}</Keyword>'.format(
          project_information.keyword))

    self.WriteLine('  </PropertyGroup>')


class VS2012ProjectFileWriter(VS2010ProjectFileWriter):
  """Visual Studio 2012 project file writer."""

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2012ProjectFileWriter, self).__init__()
    self._project_file_version = '11.0.61030.0'
    self._tools_version = '4.0'
    self._version = 2012

  def _WriteClCompileSection(self, project_configuration):
    """Writes the CLCompile section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    include_directories = ';'.join(project_configuration.include_directories)

    include_directories = re.sub(r'&quot;', r'', include_directories)

    if include_directories and include_directories[-1] != ';':
      include_directories = '{0:s};'.format(
          include_directories)

    include_directories = '{0:s}%(AdditionalIncludeDirectories)'.format(
        include_directories)

    preprocessor_definitions = project_configuration.preprocessor_definitions

    if preprocessor_definitions and preprocessor_definitions[-1] != ';':
      preprocessor_definitions = '{0:s};'.format(preprocessor_definitions)

    preprocessor_definitions = '{0:s}%(PreprocessorDefinitions)'.format(
        preprocessor_definitions)

    self.WriteLine('    <ClCompile>')

    if project_configuration.optimization != '':
      self.WriteLine('      <Optimization>{0:s}</Optimization>'.format(
          project_configuration.optimization_string))

    if project_configuration.enable_intrinsic_functions != '':
      self.WriteLine((
          '      <IntrinsicFunctions>{0:s}</IntrinsicFunctions>').format(
              project_configuration.enable_intrinsic_functions))

    self.WriteLine((
        '      <AdditionalIncludeDirectories>{0:s}'
        '</AdditionalIncludeDirectories>').format(include_directories))

    self.WriteLine((
        '      <PreprocessorDefinitions>{0:s}'
        '</PreprocessorDefinitions>').format(preprocessor_definitions))

    if project_configuration.basic_runtime_checks != '':
      self.WriteLine((
          '      <BasicRuntimeChecks>{0:s}'
          '</BasicRuntimeChecks>').format(
              project_configuration.basic_runtime_checks_string))

    if project_configuration.smaller_type_check != '':
      self.WriteLine((
          '      <SmallerTypeCheck>{0:s}</SmallerTypeCheck>').format(
              project_configuration.smaller_type_check))

    self.WriteLine((
        '      <RuntimeLibrary>{0:s}</RuntimeLibrary>').format(
            project_configuration.runtime_librarian_string))

    if project_configuration.enable_function_level_linking != '':
      self.WriteLine((
          '      <FunctionLevelLinking>{0:s}</FunctionLevelLinking>').format(
              project_configuration.enable_function_level_linking))

    if project_configuration.precompiled_header != '':
      # A value of 0 is represented by an empty XML tag.
      if project_configuration.precompiled_header == '0':
        self.WriteLine('      <PrecompiledHeader />')
      else:
        self.WriteLine((
            '      <PrecompiledHeader>{0:s}</PrecompiledHeader>').format(
                project_configuration.precompiled_header_string))

    self.WriteLine('      <WarningLevel>{0:s}</WarningLevel>'.format(
        project_configuration.warning_level_string))

    if project_configuration.warning_as_error:
      self.WriteLine((
          '      <TreatWarningAsError>{0:s}'
          '</TreatWarningAsError>').format(
              project_configuration.warning_as_error))

    if project_configuration.debug_information_format != '':
      # A value of 0 is represented by an empty XML tag.
      if project_configuration.debug_information_format == '0':
        self.WriteLine('      <DebugInformationFormat />')
      else:
        self.WriteLine((
            '      <DebugInformationFormat>{0:s}'
            '</DebugInformationFormat>').format(
                project_configuration.debug_information_format_string))

    if project_configuration.compile_as:
      self.WriteLine('      <CompileAs>{0:s}</CompileAs>'.format(
          project_configuration.compile_as_string))

    self.WriteLine('    </ClCompile>')

  def _WriteConfigurationPropertyGroup(self, project_configuration):
    """Writes the configuration property group.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self._WriteConfigurationPropertyGroupHeader(project_configuration)

    self.WriteLine('    <ConfigurationType>{0:s}</ConfigurationType>'.format(
        project_configuration.output_type_string))

    platform_toolset = project_configuration.GetPlatformToolset(self._version)
    if platform_toolset:
      self.WriteLine('    <PlatformToolset>{0:s}</PlatformToolset>'.format(
          platform_toolset))

    if project_configuration.character_set:
      self.WriteLine('    <CharacterSet>{0:s}</CharacterSet>'.format(
          project_configuration.character_set_string))

    if project_configuration.managed_extensions == '1':
      self.WriteLine('    <CLRSupport>true</CLRSupport>')

    if project_configuration.whole_program_optimization:
      self.WriteLine((
          '    <WholeProgramOptimization>{0:s}'
          '</WholeProgramOptimization>').format(
              project_configuration.whole_program_optimization_string))

    self._WriteConfigurationPropertyGroupFooter()

  def _WriteItemDefinitionGroup(self, project_configuration):
    """Writes the item definition group.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self._WriteItemDefinitionGroupHeader(project_configuration)

    # Write the compiler specific section.
    self._WriteClCompileSection(project_configuration)

    # Write the librarian specific section.
    if project_configuration.librarian_output_file:
      self._WriteLibrarianSection(project_configuration)

    # Write the linker specific section.
    if (project_configuration.linker_values_set or
        project_configuration.output_type == (
            definitions.OUTPUT_TYPE_APPLICATION)):
      self._WriteLinkerSection(project_configuration)

    self._WriteItemDefinitionGroupFooter()

  def _WriteLibrarianSection(self, project_configuration):
    """Writes the librarian section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    librarian_output_file = re.sub(
        r'[$][(]OutDir[)]\\', r'$(OutDir)',
        project_configuration.librarian_output_file)

    self.WriteLines([
        '    <Lib>',
        '      <OutputFile>{0:s}</OutputFile>'.format(librarian_output_file)])

    if project_configuration.module_definition_file != '':
      self.WriteLine((
          '      <ModuleDefinitionFile>{0:s}'
          '</ModuleDefinitionFile>').format(
              project_configuration.module_definition_file))
    else:
      self.WriteLine('      <ModuleDefinitionFile />')

    if project_configuration.librarian_ignore_defaults != '':
      self.WriteLine((
          '      <IgnoreAllDefaultLibraries>{0:s}'
          '</IgnoreAllDefaultLibraries>').format(
              project_configuration.librarian_ignore_defaults))

    self.WriteLine('    </Lib>')

  def _WriteLinkerSection(self, project_configuration):
    """Writes the linker section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self.WriteLine('    <Link>')

    # Visual Studio will convert an empty additional dependencies value.
    if project_configuration.additional_dependencies:
      additional_dependencies = ';'.join(
          sorted(project_configuration.additional_dependencies))

      additional_dependencies = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)', additional_dependencies)

      if additional_dependencies and additional_dependencies[-1] != ';':
        additional_dependencies = '{0:s};'.format(additional_dependencies)

      additional_dependencies = (
          '{0:s}%(AdditionalDependencies)').format(
              additional_dependencies)

      self.WriteLine((
          '      <AdditionalDependencies>{0:s}'
          '</AdditionalDependencies>').format(
              additional_dependencies))

    if project_configuration.linker_output_file:
      linker_output_file = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)',
          project_configuration.linker_output_file)

      self.WriteLine('      <OutputFile>{0:s}</OutputFile>'.format(
          linker_output_file))

      if project_configuration.module_definition_file != '':
        self.WriteLine((
            '      <ModuleDefinitionFile>{0:s}'
            '</ModuleDefinitionFile>').format(
                project_configuration.module_definition_file))

    if project_configuration.library_directories:
      library_directories = ';'.join(project_configuration.library_directories)
      library_directories = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)', library_directories)
      library_directories = re.sub(r'&quot;', r'', library_directories)

      if library_directories and library_directories[-1] != ';':
        library_directories = '{0:s};'.format(library_directories)

      library_directories = (
          '{0:s}%(AdditionalLibraryDirectories)').format(
              library_directories)

      self.WriteLine((
          '      <AdditionalLibraryDirectories>{0:s}'
          '</AdditionalLibraryDirectories>').format(
              library_directories))

    if project_configuration.generate_debug_information != '':
      self.WriteLine((
          '      <GenerateDebugInformation>{0:s}'
          '</GenerateDebugInformation>').format(
              project_configuration.generate_debug_information))

    if project_configuration.sub_system != '':
      self.WriteLine('      <SubSystem>{0:s}</SubSystem>'.format(
          project_configuration.sub_system_string))

    if project_configuration.optimize_references == '0':
      self.WriteLine('      <OptimizeReferences />')

    elif project_configuration.optimize_references != '':
      self.WriteLine((
          '      <OptimizeReferences>{0:s}</OptimizeReferences>').format(
              project_configuration.optimize_references_string))

    if project_configuration.enable_comdat_folding == '0':
      self.WriteLine('      <EnableCOMDATFolding />')

    elif project_configuration.enable_comdat_folding != '':
      self.WriteLine((
          '      <EnableCOMDATFolding>{0:s}</EnableCOMDATFolding>').format(
              project_configuration.enable_comdat_folding_string))

    if project_configuration.randomized_base_address != '':
      self.WriteLine((
          '      <RandomizedBaseAddress>{0:s}'
          '</RandomizedBaseAddress>').format(
              project_configuration.randomized_base_address_string))

    if project_configuration.fixed_base_address == '0':
      # A value of 0 is represented by an empty XML tag.
      self.WriteLine('      <FixedBaseAddress />')

    if project_configuration.data_execution_prevention != '':
      # A value of 0 is represented by an empty XML tag.
      if project_configuration.data_execution_prevention == '0':
        self.WriteLine('      <DataExecutionPrevention />')
      else:
        self.WriteLine((
            '      <DataExecutionPrevention>{0:s}'
            '</DataExecutionPrevention>').format(
                project_configuration.data_execution_prevention_string))

    if (project_configuration.target_machine != '' and
        project_configuration.linker_values_set):
      self.WriteLine('      <TargetMachine>{0:s}</TargetMachine>'.format(
          project_configuration.target_machine_string))

    if project_configuration.import_library:
      import_library = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)',
          project_configuration.import_library)

      self.WriteLine('      <ImportLibrary>{0:s}</ImportLibrary>'.format(
          import_library))

    self.WriteLine('    </Link>')

  def _WriteOutIntDirConditions(
      self, configuration_name, project_configurations):
    """Writes the OutDir and IntDir conditions.

    Args:
      configuration_name (str): name of the configuration.
      project_configurations (VSConfigurations): configurations.
    """
    for configuration_platform in sorted(project_configurations.platforms):
      project_configuration = project_configurations.GetByIdentifier(
          configuration_name, configuration_platform)

      if len(project_configurations.platforms) == 1:
        self.WriteLines([
            ('  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
             '\'{0:s}|{1:s}\'">').format(
                 project_configuration.name, project_configuration.platform),
            '    <OutDir>$(SolutionDir)$(Configuration)\\</OutDir>',
            '    <IntDir>$(Configuration)\\</IntDir>'])
      else:
        self.WriteLines([
            ('  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
             '\'{0:s}|{1:s}\'">').format(
                 project_configuration.name, project_configuration.platform),
            ('    <OutDir>$(SolutionDir)$(Configuration)\\$(Platform)\\'
             '</OutDir>'),
            '    <IntDir>$(Configuration)\\$(Platform)\\</IntDir>'])

      if project_configuration.linker_values_set:
        self.WriteLine('    <LinkIncremental>false</LinkIncremental>')

      self.WriteLine('  </PropertyGroup>')

  def _WriteOutIntDirPropertyGroups(self, project_configurations):
    """Writes the OutDir and IntDir property groups.

    Args:
      project_configurations (VSConfigurations): configurations.
    """
    self.WriteLines([
        '  <PropertyGroup>',
        '    <_ProjectFileVersion>{0:s}</_ProjectFileVersion>'.format(
            self._project_file_version),
        '  </PropertyGroup>'])

    # Mimic Visual Studio behavior and output the configurations
    # in platforms by name.
    for configuration_name in sorted(project_configurations.names):
      self._WriteOutIntDirConditions(configuration_name, project_configurations)

      # for configuration_platform in sorted(project_configurations.platforms):
      #   project_configuration = project_configurations.GetByIdentifier(
      #       configuration_name, configuration_platform)

      #   if project_configuration.link_incremental != '':
      #     self.WriteLine((
      #         '    <LinkIncremental Condition="\'$(Configuration)|'
      #         '$(Platform)\'==\'{0:s}|{1:s}\'">{2:s}'
      #         '</LinkIncremental>').format(
      #             project_configuration.name, project_configuration.platform,
      #             project_configuration.link_incremental_string))


class VS2013ProjectFileWriter(VS2010ProjectFileWriter):
  """Visual Studio 2013 project file writer."""

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2013ProjectFileWriter, self).__init__()
    self._project_file_version = '12.0.21005.1'
    self._tools_version = '12.0'
    self._version = 2013


class VS2015ProjectFileWriter(VS2012ProjectFileWriter):
  """Visual Studio 2015 project file writer."""

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2015ProjectFileWriter, self).__init__()
    self._project_file_version = '14.0.25431.1'
    self._tools_version = '14.0'
    self._version = 2015

  def _WriteOutIntDirConditions(
      self, configuration_name, project_configurations):
    """Writes the OutDir and IntDir conditions.

    Args:
      configuration_name (str): name of the configuration.
      project_configurations (VSConfigurations): configurations.
    """
    for configuration_platform in sorted(project_configurations.platforms):
      project_configuration = project_configurations.GetByIdentifier(
          configuration_name, configuration_platform)

      if len(project_configurations.platforms) == 1:
        self.WriteLines([
            ('  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
             '\'{0:s}|{1:s}\'">').format(
                 project_configuration.name, project_configuration.platform),
            '    <OutDir>$(SolutionDir)$(Configuration)\\</OutDir>',
            '    <IntDir>$(Configuration)\\</IntDir>'])
      else:
        self.WriteLines([
            ('  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
             '\'{0:s}|{1:s}\'">').format(
                 project_configuration.name, project_configuration.platform),
            ('    <OutDir>$(SolutionDir)$(Configuration)\\$(Platform)\\'
             '</OutDir>'),
            '    <IntDir>$(Configuration)\\$(Platform)\\</IntDir>'])

      self.WriteLine('  </PropertyGroup>')


class VS2017ProjectFileWriter(VS2012ProjectFileWriter):
  """Visual Studio 2017 project file writer."""

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2017ProjectFileWriter, self).__init__()
    self._project_file_version = '15.0.26730.3'
    self._tools_version = '15.0'
    self._version = 2017

  def _WriteItemDefinitionGroup(self, project_configuration):
    """Writes the item definition group.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self._WriteItemDefinitionGroupHeader(project_configuration)

    # Write the compiler specific section.
    self._WriteClCompileSection(project_configuration)

    # Write the librarian specific section.
    if project_configuration.librarian_output_file:
      self._WriteLibrarianSection(project_configuration)

    # Write the linker specific section.
    if (project_configuration.linker_values_set or
        project_configuration.output_type == (
            definitions.OUTPUT_TYPE_APPLICATION)):
      self._WriteLinkerSection(project_configuration)

    self._WriteItemDefinitionGroupFooter()

  def _WriteLinkerSection(self, project_configuration):
    """Writes the linker section.

    Args:
      project_configuration (VSProjectConfiguration): project configuration.
    """
    self.WriteLine('    <Link>')

    # Visual Studio will convert an empty additional dependencies value.
    if project_configuration.additional_dependencies:
      additional_dependencies = ';'.join(
          sorted(project_configuration.additional_dependencies))

      additional_dependencies = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)', additional_dependencies)

      if additional_dependencies and additional_dependencies[-1] != ';':
        additional_dependencies = '{0:s};'.format(additional_dependencies)

      additional_dependencies = '{0:s}%(AdditionalDependencies)'.format(
          additional_dependencies)

      self.WriteLine((
          '      <AdditionalDependencies>{0:s}'
          '</AdditionalDependencies>').format(
              additional_dependencies))

    if project_configuration.linker_output_file:
      linker_output_file = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)',
          project_configuration.linker_output_file)

      self.WriteLine('      <OutputFile>{0:s}</OutputFile>'.format(
          linker_output_file))

      if project_configuration.module_definition_file != '':
        self.WriteLine((
            '      <ModuleDefinitionFile>{0:s}'
            '</ModuleDefinitionFile>').format(
                project_configuration.module_definition_file))

    if project_configuration.library_directories:
      library_directories = ';'.join(project_configuration.library_directories)
      library_directories = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)', library_directories)
      library_directories = re.sub(r'&quot;', r'', library_directories)

      if library_directories and library_directories[-1] != ';':
        library_directories = '{0:s};'.format(library_directories)

      library_directories = '{0:s}%(AdditionalLibraryDirectories)'.format(
          library_directories)

      self.WriteLine((
          '      <AdditionalLibraryDirectories>{0:s}'
          '</AdditionalLibraryDirectories>').format(
              library_directories))

    if project_configuration.generate_debug_information != '':
      self.WriteLine((
          '      <GenerateDebugInformation>{0:s}'
          '</GenerateDebugInformation>').format(
              project_configuration.generate_debug_information))

    if project_configuration.sub_system != '':
      self.WriteLine('      <SubSystem>{0:s}</SubSystem>'.format(
          project_configuration.sub_system_string))

    if project_configuration.optimize_references == '0':
      self.WriteLines([
          '      <OptimizeReferences>',
          '      </OptimizeReferences>'])

    elif project_configuration.optimize_references != '':
      self.WriteLine((
          '      <OptimizeReferences>{0:s}</OptimizeReferences>').format(
              project_configuration.optimize_references_string))

    if project_configuration.enable_comdat_folding == '0':
      self.WriteLines([
          '      <EnableCOMDATFolding>',
          '      </EnableCOMDATFolding>'])

    elif project_configuration.enable_comdat_folding != '':
      self.WriteLine((
          '      <EnableCOMDATFolding>{0:s}</EnableCOMDATFolding>').format(
              project_configuration.enable_comdat_folding_string))

    if project_configuration.randomized_base_address != '':
      self.WriteLine((
          '      <RandomizedBaseAddress>{0:s}'
          '</RandomizedBaseAddress>').format(
              project_configuration.randomized_base_address_string))

    if project_configuration.fixed_base_address == '0':
      self.WriteLines([
          '      <FixedBaseAddress>',
          '      </FixedBaseAddress>'])

    if project_configuration.data_execution_prevention != '':
      # A value of 0 is represented by a new line.
      if project_configuration.data_execution_prevention == '0':
        self.WriteLines([
            '      <DataExecutionPrevention>',
            '      </DataExecutionPrevention>'])
      else:
        self.WriteLine((
            '      <DataExecutionPrevention>{0:s}'
            '</DataExecutionPrevention>').format(
                project_configuration.data_execution_prevention_string))

    if project_configuration.import_library:
      import_library = re.sub(
          r'[$][(]OutDir[)]\\', r'$(OutDir)',
          project_configuration.import_library)

      self.WriteLine('      <ImportLibrary>{0:s}</ImportLibrary>'.format(
          import_library))

    if project_configuration.target_machine != '':
      self.WriteLine('      <TargetMachine>{0:s}</TargetMachine>'.format(
          project_configuration.target_machine_string))

    if project_configuration.output_type != definitions.OUTPUT_TYPE_APPLICATION:
      self.WriteLine(
          '      <ImportLibrary>$(OutDir)$(ProjectName).lib</ImportLibrary>')

    self.WriteLine('    </Link>')

  def _WriteOutIntDirConditions(
      self, configuration_name, project_configurations):
    """Writes the OutDir and IntDir conditions.

    Args:
      configuration_name (str): name of the configuration.
      project_configurations (VSConfigurations): configurations.
    """
    for configuration_platform in sorted(project_configurations.platforms):
      project_configuration = project_configurations.GetByIdentifier(
          configuration_name, configuration_platform)

      if len(project_configurations.platforms) == 1:
        self.WriteLines([
            ('  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
             '\'{0:s}|{1:s}\'">').format(
                 project_configuration.name, project_configuration.platform),
            '    <OutDir>$(SolutionDir)$(Configuration)\\</OutDir>',
            '    <IntDir>$(Configuration)\\</IntDir>'])
      else:
        self.WriteLines([
            ('  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'=='
             '\'{0:s}|{1:s}\'">').format(
                 project_configuration.name, project_configuration.platform),
            ('    <OutDir>$(SolutionDir)$(Configuration)\\$(Platform)\\'
             '</OutDir>'),
            '    <IntDir>$(Configuration)\\$(Platform)\\</IntDir>'])

      if project_configuration.output_type == (
          definitions.OUTPUT_TYPE_APPLICATION):
        self.WriteLine('    <LinkIncremental>false</LinkIncremental>')

      self.WriteLine('  </PropertyGroup>')

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteLines([
        '<?xml version="1.0" encoding="utf-8"?>',
        ('<Project DefaultTargets="Build" ToolsVersion="{0:s}" '
         'xmlns="http://schemas.microsoft.com/developer/msbuild/2003">').format(
             self._tools_version)])


class VS2019ProjectFileWriter(VS2017ProjectFileWriter):
  """Visual Studio 2019 project file writer."""

  def __init__(self):
    """Initializes a Visual Studio project file writer."""
    super(VS2019ProjectFileWriter, self).__init__()
    self._project_file_version = '15.0.26730.3'
    self._tools_version = '15.0'
    self._version = 2019


class VSSolutionFileWriter(FileWriter):
  """Visual Studio solution file writer."""

  def _WriteProjectConfigurationPlatforms(
      self, solution_configurations, solution_projects):
    """Writes the project configuration platforms.

    Args:
      solution_configurations (VSConfigurations): configurations.
      solution_projects (list[VSSolutionProject]): projects.
    """
    if solution_configurations.number_of_configurations > 0:
      self.WriteLine(
          '\tGlobalSection(ProjectConfigurationPlatforms) = postSolution')

      for configuration_platform in sorted(solution_configurations.platforms):
        for solution_project in solution_projects:
          for configuration_name in sorted(solution_configurations.names):
            configuration = solution_configurations.GetByIdentifier(
                configuration_name, configuration_platform)

            self.WriteLine((
                '\t\t{{{0:s}}}.{1:s}|{2:s}.ActiveCfg = {1:s}|{2:s}').format(
                    solution_project.guid.upper(), configuration.name,
                    configuration.platform))
            self.WriteLine((
                '\t\t{{{0:s}}}.{1:s}|{2:s}.Build.0 = {1:s}|{2:s}').format(
                    solution_project.guid.upper(), configuration.name,
                    configuration.platform))

      self.WriteLine('\tEndGlobalSection')

  # pylint: disable=unused-argument
  def _WriteSolutionConfigurationPlatforms(
      self, solution_configurations, solution_projects):
    """Writes the solution configuration platforms.

    Args:
      solution_configurations (VSConfigurations): configurations.
      solution_projects (list[VSSolutionProject]): projects.
    """
    if solution_configurations.number_of_configurations > 0:
      self.WriteLine(
          '\tGlobalSection(SolutionConfigurationPlatforms) = preSolution')

      for configuration_platform in sorted(solution_configurations.platforms):
        for configuration_name in sorted(solution_configurations.names):
          configuration = solution_configurations.GetByIdentifier(
              configuration_name, configuration_platform)

          self.WriteLine('\t\t{0:s}|{1:s} = {0:s}|{1:s}'.format(
              configuration.name, configuration.platform))

      self.WriteLine('\tEndGlobalSection')

  def _WriteSolutionProperties(self):
    """Writes the solution properties."""
    self.WriteLines([
        '\tGlobalSection(SolutionProperties) = preSolution',
        '\t\tHideSolutionNode = FALSE',
        '\tEndGlobalSection'])

  @abc.abstractmethod
  def WriteHeader(self):
    """Writes a file header."""

  @abc.abstractmethod
  def WriteProject(self, solution_project):
    """Writes a project section.

    Args:
      solution_project (VSSolutionProject): project.
    """

  def WriteProjects(self, solution_projects):
    """Writes the projects.

    Args:
      solution_projects (list[VSSolutionProject]): projects.
    """
    for solution_project in solution_projects:
      self.WriteProject(solution_project)


class VS2008SolutionFileWriter(VSSolutionFileWriter):
  """Visual Studio 2008 solution file writer."""

  def WriteConfigurations(self, solution_configurations, solution_projects):
    """Writes the configurations.

    Args:
      solution_configurations (VSConfigurations): configurations.
      solution_projects (list[VSSolutionProject]): projects.
    """
    self.WriteLine('Global')

    self._WriteSolutionConfigurationPlatforms(
        solution_configurations, solution_projects)

    self._WriteProjectConfigurationPlatforms(
        solution_configurations, solution_projects)

    self._WriteSolutionProperties()

    self.WriteLine('EndGlobal')

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteBinaryData(b'\xef\xbb\xbf\r\n')
    self.WriteLines([
        'Microsoft Visual Studio Solution File, Format Version 10.00',
        '# Visual C++ Express 2008'])

  def WriteProject(self, solution_project):
    """Writes a project section.

    Args:
      solution_project (VSSolutionProject): project.
    """
    solution_project_filename = '{0:s}.vcproj'.format(
        solution_project.filename)

    self.WriteLine((
        'Project("{{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}}") = "{0:s}", '
        '"{1:s}", "{{{2:s}}}"').format(
            solution_project.name, solution_project_filename,
            solution_project.guid.upper()))

    if solution_project.dependencies:
      self.WriteLine(
          '\tProjectSection(ProjectDependencies) = postProject')

      for dependency_guid in solution_project.dependencies:
        self.WriteLine('\t\t{{{0:s}}} = {{{0:s}}}'.format(
            dependency_guid.upper()))

      self.WriteLine('\tEndProjectSection')

    self.WriteLine('EndProject')


class VS2010SolutionFileWriter(VSSolutionFileWriter):
  """Visual Studio 2010 solution file writer."""

  def WriteConfigurations(self, solution_configurations, solution_projects):
    """Writes the configurations.

    Args:
      solution_configurations (VSConfigurations): configurations.
      solution_projects (list[VSSolutionProject]): projects.
    """
    self.WriteLine('Global')

    self._WriteSolutionConfigurationPlatforms(
        solution_configurations, solution_projects)

    self._WriteProjectConfigurationPlatforms(
        solution_configurations, solution_projects)

    self._WriteSolutionProperties()

    self.WriteLine('EndGlobal')

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteBinaryData(b'\xef\xbb\xbf\r\n')
    self.WriteLines([
        'Microsoft Visual Studio Solution File, Format Version 11.00',
        '# Visual C++ Express 2010'])

  def WriteProject(self, solution_project):
    """Writes a project section.

    Args:
      solution_project (VSSolutionProject): project.
    """
    solution_project_filename = '{0:s}.vcxproj'.format(
        solution_project.filename)

    self.WriteLine((
        'Project("{{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}}") = "{0:s}", '
        '"{1:s}", "{{{2:s}}}"').format(
            solution_project.name, solution_project_filename,
            solution_project.guid.upper()))

    self.WriteLine('EndProject')


class VS2012SolutionFileWriter(VS2010SolutionFileWriter):
  """Visual Studio 2012 solution file writer."""

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteBinaryData(b'\xef\xbb\xbf\r\n')
    self.WriteLines([
        'Microsoft Visual Studio Solution File, Format Version 12.00',
        '# Visual Studio Express 2012 for Windows Desktop'])

  def WriteProject(self, solution_project):
    """Writes a project section.

    Args:
      solution_project (VSSolutionProject): project.
    """
    solution_project_filename = '{0:s}.vcxproj'.format(
        solution_project.filename)

    self.WriteLine((
        'Project("{{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}}") = "{0:s}", '
        '"{1:s}", "{{{2:s}}}"').format(
            solution_project.name, solution_project_filename,
            solution_project.guid.upper()))

    # TODO: what about:
    # '\tProjectSection(ProjectDependencies) = postProject'
    # '\t\t{%GUID%} = {%GUID}'
    # '\tEndProjectSection'

    self.WriteLine('EndProject')


class VS2013SolutionFileWriter(VS2010SolutionFileWriter):
  """Visual Studio 2013 solution file writer."""

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteBinaryData(b'\xef\xbb\xbf\r\n')
    self.WriteLines([
        'Microsoft Visual Studio Solution File, Format Version 12.00',
        '# Visual Studio Express 2013 for Windows Desktop',
        'VisualStudioVersion = 12.0.21005.1',
        'MinimumVisualStudioVersion = 10.0.40219.1'])


class VS2015SolutionFileWriter(VS2010SolutionFileWriter):
  """Visual Studio 2015 solution file writer."""

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteBinaryData(b'\xef\xbb\xbf\r\n')
    self.WriteLines([
        'Microsoft Visual Studio Solution File, Format Version 12.00',
        '# Visual Studio 14',
        'VisualStudioVersion = 14.0.25420.1',
        'MinimumVisualStudioVersion = 10.0.40219.1'])


class VS2017SolutionFileWriter(VS2010SolutionFileWriter):
  """Visual Studio 2017 solution file writer."""

  def _WriteExtensibilityGlobals(self):
    """Writes the extensibility globals."""
    # TODO: determine if GUID is unique.
    self.WriteLines([
        '\tGlobalSection(ExtensibilityGlobals) = postSolution',
        '\t\tSolutionGuid = {E41FC29C-7FE6-4F98-85AD-1ED968E86446}',
        '\tEndGlobalSection'])

  def WriteConfigurations(self, solution_configurations, solution_projects):
    """Writes the configurations.

    Args:
      solution_configurations (VSConfigurations): configurations.
      solution_projects (list[VSSolutionProject]): projects.
    """
    self.WriteLine('Global')

    self._WriteSolutionConfigurationPlatforms(
        solution_configurations, solution_projects)

    self._WriteProjectConfigurationPlatforms(
        solution_configurations, solution_projects)

    self._WriteSolutionProperties()
    # self._WriteExtensibilityGlobals()

    self.WriteLine('EndGlobal')

  def WriteHeader(self):
    """Writes a file header."""
    self.WriteBinaryData(b'\xef\xbb\xbf\r\n')
    self.WriteLines([
        'Microsoft Visual Studio Solution File, Format Version 12.00',
        '# Visual Studio 15',
        'VisualStudioVersion = 15.0.26730.10',
        'MinimumVisualStudioVersion = 10.0.40219.1'])


class VS2019SolutionFileWriter(VS2017SolutionFileWriter):
  """Visual Studio 2019 solution file writer."""
