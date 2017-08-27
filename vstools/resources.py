# -*- coding: utf-8 -*-
"""Project and solution classes."""

from __future__ import unicode_literals

import abc


class VSConfiguration(object):
  """Visual Studio configuration.

  Attributes:
    name (str): configuration name.
    platform (str): configuration platform.
  """

  def __init__(self, name='', platform=''):
    """Initializes a Visual Studio configuration.

    Args:
      name (Optional[str]): configuration name.
      platform (Optional[str]): configuration platform.
    """
    self.name = name
    self.platform = platform

  @abc.abstractmethod
  def CopyToX64(self):
    """Copies the Visual Studio solution configuration to an x64 equivalent."""


class VSConfigurations(object):
  """Visual Studio solution and project configurations.

  Attributes:
    names (list[str]): names of the configurations.
    platforms (list[str]): platforms of the configurations.
  """

  def __init__(self):
    """Initializes a Visual Studio configurations."""
    self._configurations = {}
    self.names = []
    self.platforms = []

  @property
  def number_of_configurations(self):
    """int: number of configurations."""
    return len(self._configurations.values())

  def Append(self, configuration):
    """Appends a configuration.

    Args:
      configuration (VSConfiguration): configuration.
    """
    if configuration.name not in self.names:
      self.names.append(configuration.name)

    if configuration.platform not in self.platforms:
      self.platforms.append(configuration.platform)

    identifier = '{0:s}|{1:s}'.format(
        configuration.name, configuration.platform)

    self._configurations[identifier] = configuration

  def ExtendWithX64(self, unused_output_version):
    """Extends the configurations with the x64 platform.

    Args:
      output_version (str): output Visual Studio version.
    """
    if 'x64' not in self.platforms:
      for configuration in list(self._configurations.values()):
        if configuration.platform != 'x64':
          x64_configuration = configuration.CopyToX64()

          self.Append(x64_configuration)

  def GetByIdentifier(self, name, platform):
    """Retrieves a specific configuration by identtifier.

    The identifier is formatted as: name|platform.

    Args:
      name (str): configuration name.
      platform (Optional[str]): configuration platform.

    Returns:
      VSConfiguration: configuration.
    """
    identifier = '{0:s}|{1:s}'.format(name, platform)
    return self._configurations[identifier]

  def GetSorted(self, reverse=False):
    """Retrieves configurations in sorted order.

    The sorting order is first alphabetacally by name,
    secondly alphabetacally by platform.

    Args:
      reverse (Optional[bool]): True if the name sort order should be
          reversed. The platform sort order is not affected.

    Yields:
      VSConfiguration: configuration.
    """
    for name in sorted(self.names, reverse=reverse):
      for platform in sorted(self.platforms):
        yield self.GetByIdentifier(name, platform)

  def RemoveByName(self, name):
    """Removes a configuration by name.

    Args:
      name (str): name of the configuration to remove.
    """
    if name not in self.names:
      return

    self.names.remove(name)

    for platform in self.platforms:
      identifier = '{0:s}|{1:s}'.format(name, platform)
      del self._configurations[identifier]


class VSProjectConfiguration(VSConfiguration):
  """Visual Studio project configuration.

  Attributes:
    additional_dependencies (list[str]): additional dependencies.
    basic_runtime_checks (str): basic runtime checks.
    character_set (str): character set.
    compile_as (str): compile as.
    data_execution_prevention (str): data execution prevention.
    debug_information_format (str): debug information format.
    detect_64bit_portability_problems (str): detect 64bit portability problems.
    enable_comdat_folding (str): enable comdat folding.
    enable_function_level_linking (str): enable function level linking.
    enable_intrinsic_functions (str): enable intrinsic functions.
    fixed_base_address (str): fixed base address.
    generate_debug_information (str): generate debug information.
    import_library (str): import library.
    include_directories (list[str]): include directories.
    librarian_ignore_defaults (str): librarian ignore defaults.
    librarian_output_file (str): librarian output file.
    library_directories (list[str]): library directories.
    link_incremental (str): link incremental.
    linker_output_directory (str): linker output directory.
    linker_output_file (str): linker output file.
    linker_values_set (bool): True if linker values are set.
    managed_extensions (str): managed extensions.
    module_definition_file (str): module definition file.
    name (str): project name.
    optimize_references (str): optimize references.
    optimization (str): optimization.
    output_type (str): output type.
    platform (str): platform.
    platform_toolset (str): platform toolset.
    precompiled_header (str): precompiled header.
    preprocessor_definitions (str): preprocessor definitions.
    randomized_base_address (str): randomized base address.
    runtime_library (str): runtime library.
    smaller_type_check (str): smaller type check.
    sub_system (str): sub system.
    target_machine (str): target machine.
    warning_as_error (str): warning as error.
    warning_level (str): warning level.
    whole_program_optimization (str): whole program optimization.
  """

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(VSProjectConfiguration, self).__init__()

    # Note that name and platform are inherited from VSConfiguration.
    self.additional_dependencies = []
    self.basic_runtime_checks = ''
    self.character_set = ''
    self.compile_as = ''
    self.data_execution_prevention = ''
    self.debug_information_format = ''
    self.detect_64bit_portability_problems = ''
    self.enable_comdat_folding = ''
    self.enable_function_level_linking = ''
    self.enable_intrinsic_functions = ''
    self.fixed_base_address = ''
    self.generate_debug_information = ''
    self.import_library = ''
    self.include_directories = []
    self.librarian_ignore_defaults = ''
    self.librarian_output_file = ''
    self.library_directories = []
    self.link_incremental = ''
    self.linker_output_directory = ''
    self.linker_output_file = ''
    self.linker_values_set = False
    self.managed_extensions = ''
    self.module_definition_file = ''
    self.name = ''
    self.optimize_references = ''
    self.optimization = ''
    self.output_type = ''
    self.platform = ''
    self.platform_toolset = ''
    self.precompiled_header = ''
    self.preprocessor_definitions = ''
    self.randomized_base_address = ''
    self.runtime_library = ''
    self.smaller_type_check = ''
    self.sub_system = ''
    self.target_machine = ''
    self.warning_as_error = ''
    self.warning_level = ''
    self.whole_program_optimization = ''

  @property
  def basic_runtime_checks_string(self):
    """str: basic runtime checks formatted as a string."""
    try:
      basic_runtime_checks = int(self.basic_runtime_checks, 10)
    except (TypeError, ValueError):
      return ''

    if basic_runtime_checks == 0:
      return 'Default'
    elif basic_runtime_checks == 3:
      return 'EnableFastChecks'
    return ''

  @property
  def character_set_string(self):
    """str: character set formatted as a string."""
    try:
      character_set = int(self.character_set, 10)
    except (TypeError, ValueError):
      return ''

    if character_set == 1:
      return 'Unicode'
    return ''

  @property
  def compile_as_string(self):
    """str: compile formatted as a string."""
    try:
      compile_as = int(self.compile_as, 10)
    except (TypeError, ValueError):
      return ''

    if compile_as == 1:
      return 'CompileAsC'
    elif compile_as == 2:
      return 'CompileAsCpp'
    return ''

  @property
  def data_execution_prevention_string(self):
    """str: data execution prevention formatted as a string."""
    try:
      data_execution_prevention = int(self.data_execution_prevention, 10)
    except (TypeError, ValueError):
      return ''

    if data_execution_prevention == 1:
      return 'false'
    if data_execution_prevention == 2:
      return 'true'
    return ''

  @property
  def debug_information_format_string(self):
    """str: debug information formatted as a string."""
    try:
      debug_information_format = int(self.debug_information_format, 10)
    except (TypeError, ValueError):
      return ''

    if debug_information_format == 3:
      return 'ProgramDatabase'
    return ''

  @property
  def enable_comdat_folding_string(self):
    """str: enable comdat folding formatted as a string."""
    try:
      enable_comdat_folding = int(self.enable_comdat_folding, 10)
    except (TypeError, ValueError):
      return ''

    if enable_comdat_folding == 2:
      return 'true'
    return ''

  @property
  def link_incremental_string(self):
    """str: link incremental formatted as a string."""
    try:
      link_incremental = int(self.link_incremental, 10)
    except (TypeError, ValueError):
      return ''

    if link_incremental == 1:
      return 'false'
    return ''

  @property
  def optimize_references_string(self):
    """str: optimize references formatted as a string."""
    try:
      optimize_references = int(self.optimize_references, 10)
    except (TypeError, ValueError):
      return ''

    if optimize_references == 2:
      return 'true'
    return ''

  @property
  def optimization_string(self):
    """str: optimization formatted as a string."""
    try:
      optimization = int(self.optimization, 10)
    except (TypeError, ValueError):
      return ''

    if optimization == 0:
      return 'Disabled'
    elif optimization == 2:
      return 'MaxSpeed'
    return ''

  @property
  def output_type_string(self):
    """str: output type formatted as a string."""
    try:
      output_type = int(self.output_type, 10)
    except (TypeError, ValueError):
      return ''

    if output_type == 1:
      return 'Application'
    elif output_type == 2:
      return 'DynamicLibrary'
    elif output_type == 4:
      return 'StaticLibrary'
    return ''

  @property
  def precompiled_header_string(self):
    """str: precompiled header formatted as a string."""
    try:
      _ = int(self.precompiled_header, 10)
    except (TypeError, ValueError):
      return ''

    # TODO: do something with precompiled_header.
    return ''

  @property
  def randomized_base_address_string(self):
    """str: randomized base address formatted as a string."""
    try:
      randomized_base_address = int(self.randomized_base_address, 10)
    except (TypeError, ValueError):
      return ''

    if randomized_base_address == 1:
      return 'false'
    elif randomized_base_address == 2:
      return 'true'
    return ''

  @property
  def runtime_librarian_string(self):
    """str: runtime librarian formatted as a string."""
    try:
      runtime_library = int(self.runtime_library, 10)
    except (TypeError, ValueError):
      return ''

    if runtime_library == 2:
      return 'MultiThreadedDLL'
    if runtime_library == 3:
      return 'MultiThreadedDebugDLL'
    return ''

  @property
  def sub_system_string(self):
    """str: sub system formatted as a string."""
    try:
      sub_system = int(self.sub_system, 10)
    except (TypeError, ValueError):
      return ''

    if sub_system == 0:
      return 'NotSet'
    elif sub_system == 1:
      return 'Console'
    return ''

  @property
  def target_machine_string(self):
    """str: target machine formatted as a string."""
    try:
      target_machine = int(self.target_machine, 10)
    except (TypeError, ValueError):
      return ''

    if target_machine == 1:
      return 'MachineX86'
    # TODO: assuming here that 2 is x64.
    elif target_machine == 2:
      return 'MachineX64'
    return ''

  @property
  def warning_level_string(self):
    """str: warning level formatted as a string."""
    try:
      warning_level = int(self.warning_level, 10)
    except (TypeError, ValueError):
      return ''

    if warning_level == 3:
      return 'Level3'
    elif warning_level == 4:
      return 'Level4'
    return ''

  @property
  def whole_program_optimization_string(self):
    """str: whole program optimization formatted as a string."""
    try:
      whole_program_optimization = int(self.whole_program_optimization, 10)
    except (TypeError, ValueError):
      return ''

    if whole_program_optimization == 0:
      return 'false'
    elif whole_program_optimization == 1:
      return 'true'
    return ''

  def CopyToX64(self):
    """Copies the Visual Studio project configuration to an x64 equivalent."""
    copy = VSProjectConfiguration()

    copy.additional_dependencies = list(self.additional_dependencies)
    copy.basic_runtime_checks = self.basic_runtime_checks
    copy.character_set = self.character_set
    copy.compile_as = self.compile_as
    copy.data_execution_prevention = self.data_execution_prevention
    copy.debug_information_format = self.debug_information_format
    copy.detect_64bit_portability_problems = (
        self.detect_64bit_portability_problems)
    copy.enable_comdat_folding = self.enable_comdat_folding
    copy.enable_function_level_linking = self.enable_function_level_linking
    copy.enable_intrinsic_functions = self.enable_intrinsic_functions
    copy.generate_debug_information = self.generate_debug_information
    copy.fixed_base_address = self.fixed_base_address
    copy.import_library = self.import_library
    copy.include_directories = list(self.include_directories)
    copy.librarian_ignore_defaults = self.librarian_ignore_defaults
    copy.librarian_output_file = self.librarian_output_file
    copy.library_directories = list(self.library_directories)
    copy.link_incremental = self.link_incremental
    copy.linker_output_directory = self.linker_output_directory
    copy.linker_output_file = self.linker_output_file
    copy.linker_values_set = self.linker_values_set
    copy.managed_extensions = self.managed_extensions
    copy.module_definition_file = self.module_definition_file
    copy.name = self.name
    copy.optimize_references = self.optimize_references
    copy.optimization = self.optimization
    copy.output_type = self.output_type
    copy.platform = 'x64'
    copy.platform_toolset = ''
    copy.precompiled_header = self.precompiled_header
    copy.preprocessor_definitions = self.preprocessor_definitions
    copy.randomized_base_address = self.randomized_base_address
    copy.runtime_library = self.runtime_library
    copy.smaller_type_check = self.smaller_type_check
    copy.sub_system = self.sub_system
    copy.target_machine = '2'
    copy.warning_as_error = self.warning_as_error
    copy.warning_level = self.warning_level
    copy.whole_program_optimization = self.whole_program_optimization

    return copy

  def GetPlatformToolset(self, output_version):
    """Retrieves the platform toolset.

    Args:
      output_version (str): platform toolsset version.
    """
    platform_toolset = self.platform_toolset
    if not platform_toolset:
      if output_version == 2010 and self.platform == 'x64':
        platform_toolset = 'Windows7.1SDK'
      elif output_version == 2012:
        platform_toolset = 'v110'
      # elif output_version == 2015:
      #   platform_toolset = 'v140'
    return platform_toolset


class VSProjectInformation(object):
  """Visual Studio project information.

  Attributes:
    configurations (VSConfigurations): configurations.
    dependencies (list[str]): dependencies.
    guid (str): project identifier (GUID).
    header_files (list[str]): header files.
    keyword (str): keyword.
    name (str): project name.
    resource_files (list[str]): resource files.
    root_name_space (str): root name space.
    source_files (list[str]): source files.
    third_party_dependencies (list[str]): third party dependencies.
  """

  def __init__(self):
    """Initializes Visual Studio project information."""
    self.configurations = VSConfigurations()
    self.dependencies = []
    self.guid = ''
    self.header_files = []
    self.keyword = ''
    self.name = ''
    self.resource_files = []
    self.root_name_space = ''
    self.source_files = []
    self.third_party_dependencies = []


class VSSolutionConfiguration(VSConfiguration):
  """Visual Studio solution configuration."""

  def CopyToX64(self):
    """Copies the Visual Studio solution configuration to an x64 equivalent."""
    copy = VSSolutionConfiguration()

    copy.name = self.name
    copy.platform = 'x64'

    return copy


class VSSolutionProject(object):
  """Visual Studio solution project.

  Attributes:
    name (str): project name.
    filename (str): name of the project file without extension.
    guid (str): project identifier (GUID).
  """

  def __init__(self, name, filename, guid):
    """Initializes a Visual Studio solution project.

    Args:
      name (str): project name.
      filename (str): name of the project file without extension.
      guid (str): project identifier (GUID).
    """
    self.name = name
    self.filename = filename
    self.guid = guid.lower()
    self.dependencies = []

  def AddDependency(self, dependency_guid):
    """Adds a dependency.

    Args:
      dependency_guid (str): project identifier (GUID) of the dependency.
    """
    self.dependencies.append(dependency_guid.lower())
