# -*- coding: utf-8 -*-
"""Project and solution file reader classes."""

import abc
import re

from vstools import resources


class FileReader(object):
  """File reader."""

  def __init__(self):
    """Initializes a file reader."""
    self._file = None
    self._line = None

  def Open(self, filename):
    """Opens the file.

    Args:
      filename (str): path of the file.
    """
    # For reading these files we don't care about the actual end of lines.
    self._file = open(filename, 'r')

  def Close(self):
    """Closes the file."""
    self._file.close()

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

    return line


class VSProjectFileReader(FileReader):
  """Visual Studio project file reader."""


class VS2008ProjectFileReader(VSProjectFileReader):
  """Visual Studio 2008 project file reader."""

  def _ReadConfiguration(self, line):
    """Reads a configuration.

    Args:
      line (str): line that contains the start of the configuration section.

    Returns:
      VSProjectConfiguration: configuration or None if no configuration was
          found.
    """
    if not line.startswith(u'<Configuration'):
      return None

    project_configuration = resources.VSProjectConfiguration()

    found_tool = False
    found_tool_compiler = False
    found_tool_librarian = False
    found_tool_linker = False

    while line:
      line = self._ReadLine()

      if line.startswith(u'</Configuration>'):
        break

      elif found_tool:
        if line.startswith(u'/>'):
          found_tool = False
          found_tool_compiler = False
          found_tool_librarian = False
          found_tool_linker = False

        elif found_tool_compiler:
          # Parse the compiler specific configuration.
          if line.startswith(u'Optimization='):
            values = re.findall(u'Optimization="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.optimization = values[0]

          elif line.startswith(u'EnableIntrinsicFunctions='):
            values = re.findall(
                u'EnableIntrinsicFunctions="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.enable_intrinsic_functions = values[0]

          elif line.startswith(u'AdditionalIncludeDirectories='):
            values = re.findall(
                u'AdditionalIncludeDirectories="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.include_directories = values[0]

          elif line.startswith(u'PreprocessorDefinitions='):
            values = re.findall(
                u'PreprocessorDefinitions="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.preprocessor_definitions = values[0]

          elif line.startswith(u'BasicRuntimeChecks='):
            values = re.findall(u'BasicRuntimeChecks="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.basic_runtime_checks = values[0]

          elif line.startswith(u'SmallerTypeCheck='):
            values = re.findall(u'SmallerTypeCheck="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.smaller_type_check = values[0]

          elif line.startswith(u'RuntimeLibrary='):
            values = re.findall(u'RuntimeLibrary="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.runtime_library = values[0]

          elif line.startswith(u'EnableFunctionLevelLinking='):
            values = re.findall(u'EnableFunctionLevelLinking="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.enable_function_level_linking = values[0]

          elif line.startswith(u'UsePrecompiledHeader='):
            values = re.findall(u'UsePrecompiledHeader="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.precompiled_header = values[0]

          elif line.startswith(u'WarningLevel='):
            values = re.findall(u'WarningLevel="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.warning_level = values[0]

          elif line.startswith(u'Detect64BitPortabilityProblems='):
            values = re.findall(
                u'Detect64BitPortabilityProblems="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.detect_64bit_portability_problems = (
                  values[0])

          elif line.startswith(u'WarnAsError='):
            values = re.findall(u'WarnAsError="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.warning_as_error = values[0]

          elif line.startswith(u'DebugInformationFormat='):
            values = re.findall(
                u'DebugInformationFormat="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.debug_information_format = values[0]

          elif line.startswith(u'CompileAs='):
            values = re.findall(u'CompileAs="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.compile_as = values[0]

        elif found_tool_librarian:
          # Parse the libararian specific configuration.
          if line.startswith(u'OutputFile='):
            values = re.findall(u'OutputFile="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.librarian_output_file = values[0]

          elif line.startswith(u'IgnoreAllDefaultLibraries='):
            values = re.findall(
                u'IgnoreAllDefaultLibraries="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.librarian_ignore_defaults = values[0]

        elif found_tool_linker:
          # Parse the linker specific configuration.
          if line.startswith(u'OutputDirectory='):
            project_configuration.linker_values_set = True
            values = re.findall(u'OutputDirectory="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.linker_output_directory = values[0]

          elif line.startswith(u'OutputFile='):
            project_configuration.linker_values_set = True
            values = re.findall(u'OutputFile="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.linker_output_file = values[0]

          elif line.startswith(u'AdditionalDependencies='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'AdditionalDependencies="([^"]*)"', line)
            if len(values) == 1:
              values = values[0].split(u' ')
              project_configuration.additional_dependencies = values

          elif line.startswith(u'LinkIncremental='):
            project_configuration.linker_values_set = True
            values = re.findall(u'LinkIncremental="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.link_incremental = values[0]

          elif line.startswith(u'ModuleDefinitionFile='):
            project_configuration.linker_values_set = True
            values = re.findall(u'ModuleDefinitionFile="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.module_definition_file = values[0]

          elif line.startswith(u'AdditionalLibraryDirectories='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'AdditionalLibraryDirectories="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.library_directories = values[0]

          elif line.startswith(u'GenerateDebugInformation='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'GenerateDebugInformation="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.generate_debug_information = values[0]

          elif line.startswith(u'SubSystem='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'SubSystem="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.sub_system = values[0]

          elif line.startswith(u'OptimizeReferences='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'OptimizeReferences="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.optimize_references = values[0]

          elif line.startswith(u'RandomizedBaseAddress='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'RandomizedBaseAddress="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.randomized_base_address = values[0]

          elif line.startswith(u'FixedBaseAddress='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'FixedBaseAddress="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.fixed_base_address = values[0]

          elif line.startswith(u'EnableCOMDATFolding='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'EnableCOMDATFolding="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.enable_comdat_folding = values[0]

          elif line.startswith(u'DataExecutionPrevention='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'DataExecutionPrevention="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.data_execution_prevention = values[0]

          elif line.startswith(u'ImportLibrary='):
            project_configuration.linker_values_set = True
            values = re.findall(
                u'ImportLibrary="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.import_library = values[0]

          elif line.startswith(u'TargetMachine='):
            project_configuration.linker_values_set = True
            values = re.findall(u'TargetMachine="([^"]*)"', line)
            if len(values) == 1:
              project_configuration.target_machine = values[0]

        elif line.startswith(u'Name="VCCLCompilerTool"'):
          found_tool_compiler = True

        elif line.startswith(u'Name="VCLibrarianTool"'):
          found_tool_librarian = True

        elif line.startswith(u'Name="VCLinkerTool"'):
          found_tool_linker = True

      elif line.startswith(u'<Tool'):
        found_tool = True

      elif line.startswith(u'Name='):
        # For more than 1 match findall will return a list with a tuple.
        values = re.findall(u'Name="([^|]*)[|]([^"]*)"', line)[0]
        if len(values) == 2:
          project_configuration.name = values[0]
          project_configuration.platform = values[1]

      elif line.startswith(u'ConfigurationType='):
        values = re.findall(u'ConfigurationType="([^"]*)"', line)
        if len(values) == 1:
          project_configuration.output_type = values[0]

      elif line.startswith(u'CharacterSet='):
        values = re.findall(u'CharacterSet="([^"]*)"', line)
        if len(values) == 1:
          project_configuration.character_set = values[0]

      elif line.startswith(u'ManagedExtensions='):
        values = re.findall(u'ManagedExtensions="([^"]*)"', line)
        if len(values) == 1:
          project_configuration.managed_extensions = values[0]

      elif line.startswith(u'WholeProgramOptimization='):
        values = re.findall(u'WholeProgramOptimization="([^"]*)"', line)
        if len(values) == 1:
          project_configuration.whole_program_optimization = values[0]

      # TODO: PlatformToolset.
      # TargetFrameworkVersion ?

    # Add the target machine when not defined.
    if not project_configuration.target_machine:
      if project_configuration.platform == u'Win32':
        project_configuration.target_machine = u'1'
      # TODO: assuming here that 2 is x64.
      elif project_configuration.platform == u'x64':
        project_configuration.target_machine = u'2'

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
      result = line.startswith(u'<Configurations>')
      if result:
        break
      line = self._ReadLine()

    if result:
      while line:
        line = self._ReadLine()

        if line.startswith(u'</Configurations>'):
          break

        elif line.startswith(u'<Configuration'):
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
      result = line.startswith(u'<Files>')
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

        if line.startswith(u'</Files>'):
          break

        elif found_filter:
          if line.startswith(u'</Filter>'):
            found_filter = False
            found_filter_source_files = False
            found_filter_header_files = False
            found_filter_resource_files = False

          elif found_filter_source_files:
            if line.startswith(u'RelativePath='):
              values = re.findall(u'RelativePath="([^"]*)"', line)

              if len(values) == 1:
                project_information.source_files.append(values[0])

          elif found_filter_header_files:
            if line.startswith(u'RelativePath='):
              values = re.findall(u'RelativePath="([^"]*)"', line)

              if len(values) == 1:
                project_information.header_files.append(values[0])

          elif found_filter_resource_files:
            if line.startswith(u'RelativePath='):
              values = re.findall(u'RelativePath="([^"]*)"', line)

              if len(values) == 1:
                project_information.resource_files.append(values[0])

          elif line.startswith(u'Name="Source Files"'):
            found_filter_source_files = True

          elif line.startswith(u'Name="Header Files"'):
            found_filter_header_files = True

          elif line.startswith(u'Name="Resource Files"'):

            found_filter_resource_files = True

        elif line.startswith(u'<Filter'):
          found_filter = True

  def _ReadProjectInformation(self, project_information):
    """Reads project information.

    Args:
      project_information (VSProjectInformation): project information.
    """
    line = self._ReadLine()
    while line:
      if line.startswith(u'>'):
        break

      elif line.startswith(u'Name='):
        values = re.findall(u'Name="([^"]*)"', line)
        if len(values) == 1:
          project_information.name = values[0]

      elif line.startswith(u'ProjectGUID='):
        values = re.findall(u'ProjectGUID="{([^}]*)}"', line)
        if len(values) == 1:
          project_information.guid = values[0]

      elif line.startswith(u'RootNamespace='):
        values = re.findall(u'RootNamespace="([^"]*)"', line)
        if len(values) == 1:
          project_information.root_name_space = values[0]

      elif line.startswith(u'Keyword='):
        values = re.findall(u'Keyword="([^"]*)"', line)
        if len(values) == 1:
          project_information.keyword = values[0]

      line = self._ReadLine()

  def ReadHeader(self):
    """Reads a file header.

    Returns:
      bool: True if successful or false otherwise.
    """
    line = self._ReadLine()

    if not line:
      return False

    if not line.startswith(u'<?xml version="1.0"'):
      return False

    # TODO check encoding?

    line = self._ReadLine()

    if not line:
      return False

    if not line.startswith(u'<VisualStudioProject'):
      return False

    line = self._ReadLine()

    if not line:
      return False

    if not line.startswith(u'ProjectType="Visual C++"'):
      return False

    line = self._ReadLine()

    if not line:
      return False

    if not line.startswith(u'Version="9,00"'):
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
      line (bytes): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """

  def ReadHeader(self):
    """Reads a file header.

    Returns:
      bool: True if successful or false otherwise.
    """
    line = self._ReadLine()

    if not line:
      return False

    if line != '\xef\xbb\xbf':
      return False

    line = self._ReadLine()

    if not line:
      return False

    if not line.startswith(
        'Microsoft Visual Studio Solution File, Format Version '):
      return False

    if not self._CheckFormatVersion(line):
      return False

    line = self._ReadLine(look_ahead=True)

    if line and line.startswith('# Visual C++ '):
      line = self._ReadLine()

    return True

  def ReadProject(self):
    """Reads a project.

    Returns:
      VSSolutionProject: project if successful or None otherwise.
    """
    line = self._ReadLine(look_ahead=True)

    if not line:
      return None

    # 8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942 is a Visual C++ related GUID.
    if not line.startswith(
        'Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = '):
      return None

    # For more than 1 match findall will return a list with a tuple.
    values = re.findall(
        ('Project\\("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}"\\) = "([^"]*)", '
         '"([^"]*)\\.vcproj", '
         '"{([0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*-[0-9A-F]*)}"'),
        line)

    if len(values) != 1:
      return None

    values = values[0]
    if len(values) != 3:
      return None

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

  def ReadConfigurations(self):
    """Reads the configurations.

    Returns:
      VSConfigurations: configurations.
    """
    solution_configurations = resources.VSConfigurations()

    line = self._ReadLine(look_ahead=True)

    if not line:
      return None

    if line != 'Global':
      return None

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


class VS2008SolutionFileReader(VSSolutionFileReader):
  """Visual Studio 2008 solution file reader."""

  def _CheckFormatVersion(self, line):
    """Checks the format version.

    Args:
      line (bytes): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """
    return line.endswith(' 10.00')


class VS2010SolutionFileReader(object):
  """Visual Studio 2010 solution file reader."""

  def _CheckFormatVersion(self, line):
    """Checks the format version.

    Args:
      line (bytes): line containing the Visual Studio format version.

    Returns:
      bool: True if successful or false otherwise.
    """
    return line.endswith(' 11.00')


class VS2012SolutionFileReader(object):
  """Visual Studio 2012 solution file reader."""
  # TODO: implement.


class VS2013SolutionFileReader(object):
  """Visual Studio 2013 solution file reader."""
  # TODO: implement.


class VS2015SolutionFileReader(object):
  """Visual Studio 2015 solution file reader."""
  # TODO: implement.
