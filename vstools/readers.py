# -*- coding: utf-8 -*-
"""Project and solution file reader classes."""

from __future__ import unicode_literals

import abc
import re

from vstools import py2to3
from vstools import resources


class FileReader(object):
  """File reader."""

  def __init__(self, encoding='utf-8'):
    """Initializes a file reader.

    Args:
      encoding (str): encoding.
    """
    super(FileReader, self).__init__()
    self._encoding = encoding
    self._file = None
    self._line = None

  def _ReadBinaryData(self, size):
    """Reads binary data.

    Args:
      size (int): number of bytes to read.

    Returns:
      bytes: binary data.
    """
    return self._file.read(size)

  def _ReadLine(self, look_ahead=False):
    """Reads a line.

    Args:
      look_ahead (Optional[bool]): indicated if the line should be considered
          read (False) or not (True).

    Returns:
      str: line stripped of leading and trailing white space or None if no
          input is available.
    """
    if self._line != None:
      line = self._line
      if not look_ahead:
        self._line = None

    else:
      line = self._file.readline()
      if line:
        line = line.strip()
      if look_ahead:
        self._line = line

    if isinstance(line, py2to3.BYTES_TYPE):
      line = line.decode(self._encoding)

    return line

  def Close(self):
    """Closes the file."""
    self._file.close()

  def Open(self, filename):
    """Opens the file.

    Args:
      filename (str): path of the file.
    """
    self._file = open(filename, 'rb')


class VSProjectFileReader(FileReader):
  """Visual Studio project file reader."""


class VS2008ProjectFileReader(VSProjectFileReader):
  """Visual Studio 2008 project file reader."""

  _CONFIGURATION_OPTIONS = {
      'CharacterSet': 'character_set',
      'ConfigurationType': 'output_type',
      'ManagedExtensions': 'managed_extensions',
      'WholeProgramOptimization': 'whole_program_optimization',
  }

  _TOOL_COMPILER_CONFIGURATION_OPTIONS = {
      'AdditionalIncludeDirectories': 'include_directories',
      'BasicRuntimeChecks': 'basic_runtime_checks',
      'CompileAs': 'compile_as',
      'DebugInformationFormat': 'debug_information_format',
      'Detect64BitPortabilityProblems': 'detect_64bit_portability_problems',
      'EnableFunctionLevelLinking': 'enable_function_level_linking',
      'EnableIntrinsicFunctions': 'enable_intrinsic_functions',
      'Optimization': 'optimization',
      'PreprocessorDefinitions': 'preprocessor_definitions',
      'RuntimeLibrary': 'runtime_library',
      'SmallerTypeCheck': 'smaller_type_check',
      'UsePrecompiledHeader': 'precompiled_header',
      'WarnAsError': 'warning_as_error',
      'WarningLevel': 'warning_level',
  }

  _TOOL_LIBRARIAN_CONFIGURATION_OPTIONS = {
      'IgnoreAllDefaultLibraries': 'librarian_ignore_defaults',
      'OutputFile': 'librarian_output_file',
  }

  _TOOL_LINKER_CONFIGURATION_OPTIONS = {
      'AdditionalDependencies': 'additional_dependencies',
      'AdditionalLibraryDirectories': 'library_directories',
      'DataExecutionPrevention': 'data_execution_prevention',
      'EnableCOMDATFolding': 'enable_comdat_folding',
      'FixedBaseAddress': 'fixed_base_address',
      'GenerateDebugInformation': 'generate_debug_information',
      'ImportLibrary': 'linker_values_set',
      'LinkIncremental': 'link_incremental',
      'ModuleDefinitionFile': 'module_definition_file',
      'OptimizeReferences': 'optimize_references',
      'OutputDirectory': 'linker_output_directory',
      'OutputFile': 'linker_output_file',
      'RandomizedBaseAddress': 'randomized_base_address',
      'SubSystem': 'sub_system',
      'TargetMachine': 'target_machine',
  }

  def _ParseConfigurationOption(
        self, project_configuration, definition, name, line):
    """Parses a configuration option.

    Args:
      project_information (VSProjectInformation): project information.
      definition (str): definition of the configuration value in file.
      name (str): name of the configuration value in the project information.
      line (str): line that contains the configuration value.
    """
    regex_pattern = '{0:s}="([^"]*)"'.format(definition)
    values = re.findall(regex_pattern, line)
    if len(values) == 1:
      setattr(project_configuration, name, values[0])

  def _ParseConfigurationOptions(
        self, project_configuration, configuration_options, line):
    """Parses configuration options.

    Args:
      project_information (VSProjectInformation): project information.
      configuration_options (dict[str, str]): configuration options defined
          as a name per definition.
      line (str): line that contains the configuration value.
    """
    configuration_definition, _, _ = line.partition('=')

    configuration_value = configuration_options.get(
        configuration_definition, None)

    if configuration_value:
      self._ParseConfigurationOption(
          project_configuration, configuration_definition, configuration_value,
          line)

  def _ReadConfiguration(self, line):
    """Reads a configuration.

    Args:
      line (str): line that contains the start of the configuration section.

    Returns:
      VSProjectConfiguration: configuration or None if no configuration was
          found.
    """
    if not line or not line.startswith('<Configuration'):
      return

    project_configuration = resources.VSProjectConfiguration()

    found_tool = False
    found_tool_compiler = False
    found_tool_librarian = False
    found_tool_linker = False

    while line:
      line = self._ReadLine()

      if line.startswith('</Configuration>'):
        break

      elif found_tool:
        if line.startswith('/>'):
          found_tool = False
          found_tool_compiler = False
          found_tool_librarian = False
          found_tool_linker = False

        elif found_tool_compiler:
          self._ParseConfigurationOptions(
              project_configuration, self._TOOL_COMPILER_CONFIGURATION_OPTIONS,
              line)

        elif found_tool_librarian:
          self._ParseConfigurationOptions(
              project_configuration, self._TOOL_LIBRARIAN_CONFIGURATION_OPTIONS,
              line)

        elif found_tool_linker:
          self._ParseConfigurationOptions(
              project_configuration, self._TOOL_LINKER_CONFIGURATION_OPTIONS,
              line)

        elif line.startswith('Name="VCCLCompilerTool"'):
          found_tool_compiler = True

        elif line.startswith('Name="VCLibrarianTool"'):
          found_tool_librarian = True

        elif line.startswith('Name="VCLinkerTool"'):
          found_tool_linker = True

      elif line.startswith('<Tool'):
        found_tool = True

      elif line.startswith('Name='):
        # For more than 1 match findall will return a list with a tuple.
        values = re.findall('Name="([^|]*)[|]([^"]*)"', line)[0]
        if len(values) == 2:
          project_configuration.name = values[0]
          project_configuration.platform = values[1]

      else:
        self._ParseConfigurationOptions(
            project_configuration, self._CONFIGURATION_OPTIONS, line)

      # TODO: PlatformToolset.
      # TargetFrameworkVersion ?

    # Add the target machine when not defined.
    if not project_configuration.target_machine:
      if project_configuration.platform == 'Win32':
        project_configuration.target_machine = '1'
      # TODO: assuming here that 2 is x64.
      elif project_configuration.platform == 'x64':
        project_configuration.target_machine = '2'

    return project_configuration

  def _ReadConfigurations(self, project_information):
    """Reads the configurations.

    Args:
      project_information (VSProjectInformation): project information.
    """
    # Find the start of the configurations section.
    result = False
    line = self._ReadLine()

    while line:
      result = line.startswith('<Configurations>')
      if result:
        break
      line = self._ReadLine()

    if not result:
      return

    while line:
      line = self._ReadLine()

      if line.startswith('</Configurations>'):
        break

      elif line.startswith('<Configuration'):
        project_configuration = self._ReadConfiguration(line)

        if project_configuration:
          project_information.configurations.Append(project_configuration)

  def _ReadFiles(self, project_information):
    """Reads the files.

    Args:
      project_information (VSProjectInformation): project information.
    """
    # Find the start of the files section.
    result = False
    line = self._ReadLine()

    while line:
      result = line.startswith('<Files>')
      if result:
        break
      line = self._ReadLine()

    if result:
      found_filter = False
      found_filter_source_files = False
      found_filter_header_files = False
      found_filter_resource_files = False

      while line:
        line = self._ReadLine()

        if line.startswith('</Files>'):
          break

        elif found_filter:
          if line.startswith('</Filter>'):
            found_filter = False
            found_filter_source_files = False
            found_filter_header_files = False
            found_filter_resource_files = False

          elif found_filter_source_files:
            if line.startswith('RelativePath='):
              values = re.findall('RelativePath="([^"]*)"', line)

              if len(values) == 1:
                project_information.source_files.append(values[0])

          elif found_filter_header_files:
            if line.startswith('RelativePath='):
              values = re.findall('RelativePath="([^"]*)"', line)

              if len(values) == 1:
                project_information.header_files.append(values[0])

          elif found_filter_resource_files:
            if line.startswith('RelativePath='):
              values = re.findall('RelativePath="([^"]*)"', line)

              if len(values) == 1:
                project_information.resource_files.append(values[0])

          elif line.startswith('Name="Source Files"'):
            found_filter_source_files = True

          elif line.startswith('Name="Header Files"'):
            found_filter_header_files = True

          elif line.startswith('Name="Resource Files"'):

            found_filter_resource_files = True

        elif line.startswith('<Filter'):
          found_filter = True

  def _ReadProjectInformation(self, project_information):
    """Reads project information.

    Args:
      project_information (VSProjectInformation): project information.
    """
    line = self._ReadLine()
    while line:
      if line.startswith('>'):
        break

      elif line.startswith('Name='):
        values = re.findall('Name="([^"]*)"', line)
        if len(values) == 1:
          project_information.name = values[0]

      elif line.startswith('ProjectGUID='):
        values = re.findall('ProjectGUID="{([^}]*)}"', line)
        if len(values) == 1:
          project_information.guid = values[0]

      elif line.startswith('RootNamespace='):
        values = re.findall('RootNamespace="([^"]*)"', line)
        if len(values) == 1:
          project_information.root_name_space = values[0]

      elif line.startswith('Keyword='):
        values = re.findall('Keyword="([^"]*)"', line)
        if len(values) == 1:
          project_information.keyword = values[0]

      line = self._ReadLine()

  def ReadHeader(self):
    """Reads a file header.

    Returns:
      bool: True if successful or false otherwise.
    """
    # TODO check encoding?

    line = self._ReadLine()
    if not line or not line.startswith('<?xml version="1.0"'):
      return False

    line = self._ReadLine()
    if not line or not line.startswith('<VisualStudioProject'):
      return False

    line = self._ReadLine()
    if not line or not line.startswith('ProjectType="Visual C++"'):
      return False

    line = self._ReadLine()
    if not line or not line.startswith('Version="9,00"'):
      return False

    return True

  def ReadProject(self):
    """Reads the project.

    Returns:
      VSProjectInformation: project information if successful or None otherwise.
    """
    project_information = resources.VSProjectInformation()

    self._ReadProjectInformation(project_information)
    self._ReadConfigurations(project_information)
    self._ReadFiles(project_information)

    return project_information


class VS2010ProjectFileReader(VSProjectFileReader):
  """Visual Studio 2010 project file reader."""

  # TODO: implement.


class VS2012ProjectFileReader(VSProjectFileReader):
  """Visual Studio 2012 project file reader."""

  # TODO: implement.


class VS2013ProjectFileReader(VSProjectFileReader):
  """Visual Studio 2013 project file reader."""

  # TODO: implement.


class VS2015ProjectFileReader(VSProjectFileReader):
  """Visual Studio 2015 project file reader."""

  # TODO: implement.


class VSSolutionFileReader(FileReader):
  """Visual Studio solution file reader."""

  @abc.abstractmethod
  def _CheckFormatVersion(self, line):
    """Checks the format version.

    Args:
      line (str): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """

  def ReadConfigurations(self):
    """Reads the configurations.

    Returns:
      VSConfigurations: configurations.
    """
    solution_configurations = resources.VSConfigurations()

    line = self._ReadLine(look_ahead=True)
    if not line or line != 'Global':
      return

    found_section = False

    line = self._ReadLine()

    while line and line != 'EndGlobal':
      line = self._ReadLine()

      if found_section:
        if line == 'EndGlobalSection':
          found_section = False

        else:
          # For more than 1 match findall will return a list with a tuple.
          values = re.findall('([^|]*)[|]([^ ]*) = ([^|]*)[|]([^ ]*)', line)

          if len(values) == 1:
            values = values[0]
            if (len(values) == 4 and values[0] == values[2] and
                values[1] == values[3]):
              configuration = resources.VSSolutionConfiguration()
              configuration.name = values[0]
              configuration.platform = values[1]

              solution_configurations.Append(configuration)

      elif line == ('GlobalSection(SolutionConfigurationPlatforms) = '
                    'preSolution'):
        found_section = True

    return solution_configurations

  def ReadHeader(self):
    """Reads a file header.

    Returns:
      bool: True if successful or false otherwise.
    """
    binary_data = self._ReadBinaryData(5)
    if binary_data != b'\xef\xbb\xbf\r\n':
      return False

    line = self._ReadLine()
    if not line or not line.startswith(
        'Microsoft Visual Studio Solution File, Format Version '):
      return False

    if not self._CheckFormatVersion(line):
      return False

    visual_studio_version_line = None

    line = self._ReadLine(look_ahead=True)
    while line:
      if line.startswith('# Visual C++ '):
        self._ReadLine()

      elif line.startswith('VisualStudioVersion = '):
        visual_studio_version_line = self._ReadLine()

      else:
        break

      line = self._ReadLine(look_ahead=True)

    if visual_studio_version_line:
      # TODO: add check for VisualStudioVersion
      pass

    return True

  def ReadProject(self):
    """Reads a project.

    Returns:
      VSSolutionProject: project if successful or None otherwise.
    """
    # 8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942 is a Visual C++ related GUID.

    line = self._ReadLine(look_ahead=True)
    if not line or not line.startswith(
        'Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = '):
      return

    # For more than 1 match findall will return a list with a tuple.
    values = re.findall(
        ('Project\\("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}"\\) = "([^"]*)", '
         '"([^"]*)\\.vcproj", '
         '"{([0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*)}"'),
        line)

    if len(values) != 1:
      return

    values = values[0]
    if len(values) != 3:
      return

    solution_project = resources.VSSolutionProject(
        values[0], values[1], values[2])

    found_dependencies = False

    line = self._ReadLine()

    while line and line != 'EndProject':
      line = self._ReadLine()

      if found_dependencies:
        if line == 'EndProjectSection':
          found_dependencies = False

        else:
          # The dependencies are defined as: {%GUID%} = {%GUID%}
          # For more than 1 match findall will return a list with a tuple.
          guids = re.findall(
              ('{([0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*)} = '
               '{([0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*)}'),
              line)

          if len(guids) == 1:
            guids = guids[0]

            if len(guids) == 2 and guids[0] == guids[1]:
              solution_project.AddDependency(guids[0])

      elif line == 'ProjectSection(ProjectDependencies) = postProject':
        found_dependencies = True

    return solution_project

  def ReadProjects(self):
    """Reads the projects.

    Returns:
      list[VSSolutionProject]: projects in preserved order.
    """
    solution_projects = []
    solution_project = self.ReadProject()

    while solution_project:
      solution_projects.append(solution_project)
      solution_project = self.ReadProject()

    return solution_projects


class VS2008SolutionFileReader(VSSolutionFileReader):
  """Visual Studio 2008 solution file reader."""

  def _CheckFormatVersion(self, line):
    """Checks the format version.

    Args:
      line (str): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """
    return line.endswith(' 10.00')


class VS2010SolutionFileReader(object):
  """Visual Studio 2010 solution file reader."""

  def _CheckFormatVersion(self, line):
    """Checks the format version.

    Args:
      line (str): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """
    return line.endswith(' 11.00')


class VS2012SolutionFileReader(object):
  """Visual Studio 2012 solution file reader."""

  def _CheckFormatVersion(self, line):
    """Checks the format version.

    Args:
      line (str): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """
    return line.endswith(' 12.00')


class VS2013SolutionFileReader(VS2012SolutionFileReader):
  """Visual Studio 2013 solution file reader."""

  # TODO: add check for VisualStudioVersion


class VS2015SolutionFileReader(VS2012SolutionFileReader):
  """Visual Studio 2015 solution file reader."""

  # TODO: add check for VisualStudioVersion
