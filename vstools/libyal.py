# -*- coding: utf-8 -*-
"""Libyal sources classes."""

from __future__ import unicode_literals

import logging
import os
import uuid

from vstools import readers
from vstools import resources
from vstools import solutions


class Bzip2VSProjectInformation(resources.VSProjectInformation):
  """Bzip2 Visual Studio project information."""

  def __init__(self):
    """Initializes bzip2 Visual Studio project information."""
    super(Bzip2VSProjectInformation, self).__init__()

    self.header_files = sorted([
        '..\\..\\..\\bzip2\\bzlib.h',
        '..\\..\\..\\bzip2\\bzlib_private.h'])

    self.source_files = sorted([
        '..\\..\\..\\bzip2\\blocksort.c',
        '..\\..\\..\\bzip2\\bzlib.c',
        '..\\..\\..\\bzip2\\compress.c',
        '..\\..\\..\\bzip2\\crctable.c',
        '..\\..\\..\\bzip2\\decompress.c',
        '..\\..\\..\\bzip2\\huffman.c',
        '..\\..\\..\\bzip2\\randtable.c'])


class ZlibVSProjectInformation(resources.VSProjectInformation):
  """Zlib Visual Studio project information."""

  def __init__(self):
    """Initializes zlib Visual Studio project information."""
    super(ZlibVSProjectInformation, self).__init__()

    self.header_files = sorted([
        '..\\..\\..\\zlib\\crc32.h',
        '..\\..\\..\\zlib\\deflate.h',
        '..\\..\\..\\zlib\\gzguts.h',
        '..\\..\\..\\zlib\\inffast.h',
        '..\\..\\..\\zlib\\inffixed.h',
        '..\\..\\..\\zlib\\inflate.h',
        '..\\..\\..\\zlib\\inftrees.h',
        '..\\..\\..\\zlib\\trees.h',
        '..\\..\\..\\zlib\\zconf.h',
        '..\\..\\..\\zlib\\zlib.h',
        '..\\..\\..\\zlib\\zutil.h'])

    self.resource_files = sorted([
        '..\\..\\..\\zlib\\win32\\zlib1.rc'])

    self.source_files = sorted([
        '..\\..\\..\\zlib\\adler32.c',
        '..\\..\\..\\zlib\\compress.c',
        '..\\..\\..\\zlib\\crc32.c',
        '..\\..\\..\\zlib\\deflate.c',
        '..\\..\\..\\zlib\\gzclose.c',
        '..\\..\\..\\zlib\\gzlib.c',
        '..\\..\\..\\zlib\\gzread.c',
        '..\\..\\..\\zlib\\gzwrite.c',
        '..\\..\\..\\zlib\\infback.c',
        '..\\..\\..\\zlib\\inffast.c',
        '..\\..\\..\\zlib\\inflate.c',
        '..\\..\\..\\zlib\\inftrees.c',
        '..\\..\\..\\zlib\\trees.c',
        '..\\..\\..\\zlib\\uncompr.c',
        '..\\..\\..\\zlib\\zutil.c'])


class ReleaseVSProjectConfiguration(resources.VSProjectConfiguration):
  """Release Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(ReleaseVSProjectConfiguration, self).__init__()

    self.name = 'Release'
    self.platform = 'Win32'
    self.character_set = '1'

    self.runtime_library = '2'
    # self.smaller_type_check = 'false'
    # self.precompiled_header = '0'
    self.warning_level = '4'
    # self.warning_as_error = 'false'
    self.compile_as = '1'

    self.target_machine = '1'


class ReleaseDllVSProjectConfiguration(ReleaseVSProjectConfiguration):
  """Release DLL Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(ReleaseDllVSProjectConfiguration, self).__init__()

    self.output_type = '2'
    self.linker_output_file = '$(OutDir)\\$(ProjectName).dll'
    self.library_directories = ''
    self.randomized_base_address = '2'
    self.data_execution_prevention = '2'
    self.import_library = '$(OutDir)\\$(ProjectName).lib'
    self.linker_values_set = True


class ReleaseDotNetDllVSProjectConfiguration(ReleaseDllVSProjectConfiguration):
  """Release .Net DLL Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(ReleaseDotNetDllVSProjectConfiguration, self).__init__()

    self.compile_as = '2'
    self.managed_extensions = '1'


class ReleaseExeVSProjectConfiguration(ReleaseVSProjectConfiguration):
  """Release EXE Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(ReleaseExeVSProjectConfiguration, self).__init__()

    self.output_type = '1'

    self.whole_program_optimization = '1'

    # self.precompiled_header = '0'

    self.link_incremental = '1'
    self.sub_system = '1'
    self.optimize_references = '2'
    self.enable_comdat_folding = '2'
    self.randomized_base_address = '2'
    self.data_execution_prevention = '2'
    self.target_machine = '1'
    self.linker_values_set = True


class ReleaseLibraryVSProjectConfiguration(ReleaseVSProjectConfiguration):
  """Release library Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(ReleaseLibraryVSProjectConfiguration, self).__init__()

    self.output_type = '4'
    self.librarian_output_file = '$(OutDir)\\$(ProjectName).lib'
    self.librarian_ignore_defaults = 'false'


class ReleasePythonDllVSProjectConfiguration(ReleaseDllVSProjectConfiguration):
  """Release Python DLL Visual Studio project configuration."""

  def __init__(self, python_path='C:\\Python27'):
    """Initializes a Visual Studio project configuration.

    Args:
      python_path (Optional[str]): path to the Python installation.
    """
    super(ReleasePythonDllVSProjectConfiguration, self).__init__()

    self.linker_output_file = '$(OutDir)\\$(ProjectName).pyd'
    self.library_directories = ['{0:s}\\libs'.format(python_path)]


class VSDebugVSProjectConfiguration(resources.VSProjectConfiguration):
  """VSDebug Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(VSDebugVSProjectConfiguration, self).__init__()

    self.name = 'VSDebug'
    self.platform = 'Win32'
    self.character_set = '1'

    self.optimization = '0'
    self.basic_runtime_checks = '3'
    self.smaller_type_check = 'true'
    self.runtime_library = '3'
    # self.precompiled_header = '0'
    self.warning_level = '4'
    # self.warning_as_error = 'false'
    self.debug_information_format = '3'
    self.compile_as = '1'

    self.target_machine = '1'


class VSDebugDllVSProjectConfiguration(VSDebugVSProjectConfiguration):
  """VSDebug DLL Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(VSDebugDllVSProjectConfiguration, self).__init__()

    self.output_type = '2'
    self.linker_output_file = '$(OutDir)\\$(ProjectName).dll'
    self.library_directories = ''
    self.generate_debug_information = 'true'
    self.randomized_base_address = '1'
    self.data_execution_prevention = '1'
    self.import_library = '$(OutDir)\\$(ProjectName).lib'
    self.linker_values_set = True


class VSDebugDotNetDllVSProjectConfiguration(VSDebugDllVSProjectConfiguration):
  """VSDebug .Net DLL Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(VSDebugDotNetDllVSProjectConfiguration, self).__init__()

    self.compile_as = '2'
    self.managed_extensions = '1'
    self.basic_runtime_checks = ''
    self.smaller_type_check = ''


class VSDebugExeVSProjectConfiguration(VSDebugVSProjectConfiguration):
  """VSDebug EXE Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(VSDebugExeVSProjectConfiguration, self).__init__()

    self.output_type = '1'

    # self.precompiled_header = '0'

    self.generate_debug_information = 'true'
    self.link_incremental = '1'
    self.sub_system = '1'
    self.optimize_references = '2'
    self.enable_comdat_folding = '2'
    self.randomized_base_address = '1'
    self.data_execution_prevention = '1'
    self.target_machine = '1'
    self.linker_values_set = True


class VSDebugLibraryVSProjectConfiguration(VSDebugVSProjectConfiguration):
  """VSDebug library Visual Studio project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(VSDebugLibraryVSProjectConfiguration, self).__init__()

    self.output_type = '4'
    self.librarian_output_file = '$(OutDir)\\$(ProjectName).lib'
    self.librarian_ignore_defaults = 'false'


class VSDebugPythonDllVSProjectConfiguration(VSDebugDllVSProjectConfiguration):
  """VSDebug Python DLL Visual Studio project configuration."""

  def __init__(self, python_path='C:\\Python27'):
    """Initializes a Visual Studio project configuration.

    Args:
      python_path (Optional[str]): path to the Python installation.
    """
    super(VSDebugPythonDllVSProjectConfiguration, self).__init__()

    self.linker_output_file = '$(OutDir)\\$(ProjectName).pyd'
    self.library_directories = ['{0:s}\\libs'.format(python_path)]


class LibyalSourceVSSolution(solutions.VSSolution):
  """Libyal source Visual Studio solution."""

  _SUPPORTED_THIRD_PARTY_DEPENDENCIES = frozenset(['bzip2', 'zlib'])

  def _ConfigureAsBzip2Dll(
      self, unused_project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as the bzip2 DLL.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (ReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (VSDebugVSProjectConfiguration):
          debug project configuration.
    """
    include_directories = sorted([
        '..\\..\\..\\bzip2'])

    preprocessor_definitions = [
        'WIN32',
        'NDEBUG',
        '_WINDOWS',
        '_USRDLL',
        '_CRT_SECURE_NO_WARNINGS',
        'BZ_DLL']

    release_project_configuration.include_directories = include_directories
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    debug_project_configuration.include_directories = include_directories
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

  def _ConfigureAsZlibDll(
      self, unused_project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as the zlib DLL.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (ReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (VSDebugVSProjectConfiguration):
          debug project configuration.
    """
    include_directories = sorted([
        '..\\..\\..\\zlib'])

    preprocessor_definitions = [
        'WIN32',
        'NDEBUG',
        '_WINDOWS',
        '_USRDLL',
        '_CRT_SECURE_NO_WARNINGS',
        'ZLIB_DLL']

    release_project_configuration.include_directories = include_directories
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    debug_project_configuration.include_directories = include_directories
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

  def _ConfigureLibcrypto(
      self, unused_project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project for the Windows libcrypto equivalent.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (ReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (VSDebugVSProjectConfiguration):
          debug project configuration.
    """
    dependency = 'advapi32.lib'

    if dependency not in release_project_configuration.additional_dependencies:
      release_project_configuration.additional_dependencies.append(dependency)

    if dependency not in debug_project_configuration.additional_dependencies:
      debug_project_configuration.additional_dependencies.append(dependency)

  def _ConfigureLibuuid(
      self, unused_project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project for the Windows libuuid equivalent.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (ReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (VSDebugVSProjectConfiguration):
          debug project configuration.
    """
    dependency = 'rpcrt4.lib'

    if dependency not in release_project_configuration.additional_dependencies:
      release_project_configuration.additional_dependencies.append(dependency)

    if dependency not in debug_project_configuration.additional_dependencies:
      debug_project_configuration.additional_dependencies.append(dependency)

  def _CreateThirdPartyDepencies(
      self, solution_projects, projects_by_guid, project_guids_by_name):
    """Creates the project files for third party dependencies.

    Args:
      solution_projects (list[VSSolutionProject]): projects.
      projects_by_guid (dict[str, VSProjectInformation]): projects per lower
          case GUID.
      project_guids_by_name (dict[str, VSProjectInformation]): lower case
          project GUID per name. This dictionary is use as a lookup table
          to preserve the existing GUIDs.
    """
    third_party_dependencies = []
    for project_information in projects_by_guid.itervalues():
      for dependency in project_information.third_party_dependencies:
        if dependency not in third_party_dependencies:
          third_party_dependencies.append(dependency)

    for project_name in third_party_dependencies:
      if project_name not in self._SUPPORTED_THIRD_PARTY_DEPENDENCIES:
        logging.info('Unsupported third party dependency: {0:s}'.format(
            project_name))
        continue

      project_filename = '{0:s}\\{0:s}'.format(project_name)

      project_guid = project_guids_by_name.get(project_name, '')
      if not project_guid:
        project_guid = project_guids_by_name.get(
            '{0:s}.dll'.format(project_name), '')
      if not project_guid:
        project_guid = str(uuid.uuid4())

      solution_project = resources.VSSolutionProject(
          project_name, project_filename, project_guid)

      solution_projects.append(solution_project)

      if project_name == 'bzip2':
        project_information = Bzip2VSProjectInformation()

      elif project_name == 'zlib':
        project_information = ZlibVSProjectInformation()

      else:
        project_information = resources.VSProjectInformation()

      project_information.name = project_name
      project_information.guid = project_guid
      project_information.root_name_space = project_name

      if project_name in ('bzip2', 'zlib'):
        release_project_configuration = ReleaseDllVSProjectConfiguration()
        debug_project_configuration = VSDebugDllVSProjectConfiguration()
      else:
        release_project_configuration = ReleaseVSProjectConfiguration()
        debug_project_configuration = VSDebugVSProjectConfiguration()

      if project_name == 'bzip2':
        self._ConfigureAsBzip2Dll(
            project_information, release_project_configuration,
            debug_project_configuration)

      elif project_name == 'zlib':
        self._ConfigureAsZlibDll(
            project_information, release_project_configuration,
            debug_project_configuration)

      project_information.configurations.Append(release_project_configuration)
      project_information.configurations.Append(debug_project_configuration)

      projects_by_guid[project_guid] = project_information

  def _ReadMakefile(
      self, makefile_am_path, solution_name, project_information,
      release_project_configuration, debug_project_configuration):
    """Reads the Makefile.am.

    Args:
      makefile_am_path (str): path of the Makefile.am file.
      solution_name (str): name of the solution.
      project_information (VSProjectInformation): project information.
      release_project_configuration (ReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (VSDebugVSProjectConfiguration):
          debug project configuration.
    """
    project_name = project_information.name

    file_object = open(makefile_am_path, 'r')

    include_directories = []
    preprocessor_definitions = []

    include_directories.append('\\'.join(['..', '..', 'include']))
    include_directories.append('\\'.join(['..', '..', 'common']))

    if (not project_name.startswith('lib') and
        not project_name.startswith('py') and
        not project_name.endswith('.net')):
      preprocessor_definitions.append('WIN32')
      preprocessor_definitions.append('NDEBUG')
      preprocessor_definitions.append('_CONSOLE')

    preprocessor_definitions.append('_CRT_SECURE_NO_DEPRECATE')

    additional_dependencies = []
    alternate_dependencies = []
    dependencies = []
    source_files = []
    header_files = []
    resource_files = []

    in_am_cppflags_section = False
    in_extra_dist_section = False
    in_la_libadd_section = False
    in_la_sources_section = False
    in_ldadd_section = False
    in_sources_section = False

    for index, line in enumerate(file_object.readlines()):
      line = line.strip()
      original_line = line

      if in_am_cppflags_section:
        if not line:
          in_am_cppflags_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          elif line.endswith('\\'):
            logging.warning((
                'Detected missing space before \\ in line: {0:d} '
                '"{1:s}" ({2:s})').format(
                    index, original_line, makefile_am_path))
            line = line[:-1]

          if line.startswith('@') and line.endswith('_CPPFLAGS@'):
            directory_name = line[1:-10].lower()
            if directory_name == 'bzip2':
              include_directories.append('..\\..\\..\\bzip2')

              preprocessor_definitions.append('BZ_DLL')

              alternate_dependencies.append('bzip2')

            elif directory_name == 'libfuse' and project_name.endswith('mount'):
              include_directories.append('..\\..\\..\\dokan\\dokan')

              preprocessor_definitions.append('HAVE_LIBDOKAN')

              additional_dependencies.append(
                  '..\\..\\..\\dokan\\msvscpp\\$(Configuration)\\dokan.lib')

            elif directory_name == 'zlib':
              include_directories.append('..\\..\\..\\zlib')

              preprocessor_definitions.append('ZLIB_DLL')

              alternate_dependencies.append('zlib')

            elif os.path.isdir(directory_name):
              include_directories.append(
                  '\\'.join(['..', '..', directory_name]))

              preprocessor_definitions.append(
                  'HAVE_LOCAL_{0:s}'.format(line[1:-10]))

              alternate_dependencies.append(directory_name)

      elif in_extra_dist_section:
        if not line:
          in_extra_dist_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          elif line.endswith('\\'):
            logging.warning((
                'Detected missing space before \\ in line: {0:d} '
                '"{1:s}" ({2:s})').format(
                    index, original_line, makefile_am_path))
            line = line[:-1]

          for filename in line.split(' '):
            if filename.endswith('.c') or filename.endswith('.cpp'):
              source_files.append('\\'.join([
                  '..', '..', project_name, filename]))

            elif filename.endswith('.h'):
              header_files.append('\\'.join([
                  '..', '..', project_name, filename]))

            elif filename.endswith('.rc'):
              resource_files.append('\\'.join([
                  '..', '..', project_name, filename]))

      elif in_la_libadd_section:
        if not line:
          in_la_libadd_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          if line in frozenset([
              'endif', '@LIBDL_LIBADD@', '@LIBINTL@', '@PTHREAD_LIBADD@']):
            dependency_name = ''
          elif line.startswith('@') and line.endswith('_LIBADD@'):
            dependency_name = line[1:-8].lower()
          elif line.endswith('.la'):
            _, _, dependency_name = line.rpartition('/')
            dependency_name = dependency_name[:-3]
          else:
            logging.warning(
                'Unuspported dependency definition: {0:s}'.format(line))
            dependency_name = ''

          if dependency_name:
            if dependency_name == 'libcrypto':
              preprocessor_definitions.append('HAVE_WINCRYPT')

              self._ConfigureLibcrypto(
                  project_information, release_project_configuration,
                  debug_project_configuration)

            elif dependency_name == 'libuuid':
              self._ConfigureLibuuid(
                  project_information, release_project_configuration,
                  debug_project_configuration)

            else:
              dependencies.append(dependency_name)

      elif in_la_sources_section:
        if not line:
          in_la_sources_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          elif line.endswith('\\'):
            logging.warning((
                'Detected missing space before \\ in line: {0:d} '
                '"{1:s}" ({2:s})').format(
                    index, original_line, makefile_am_path))
            line = line[:-1]

          for filename in line.split(' '):
            if filename.endswith('.c') or filename.endswith('.cpp'):
              source_files.append('\\'.join([
                  '..', '..', project_name, filename]))

            elif filename.endswith('.h'):
              header_files.append('\\'.join([
                  '..', '..', project_name, filename]))

      elif in_ldadd_section:
        if not line:
          in_ldadd_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          if line in frozenset([
              'endif', '@LIBDL_LIBADD@', '@LIBINTL@', '@PTHREAD_LIBADD@']):
            dependency_name = ''
          elif line.startswith('@') and line.endswith('_LIBADD@'):
            dependency_name = line[1:-8].lower()
          elif line.endswith('.la'):
            _, _, dependency_name = line.rpartition('/')
            dependency_name = dependency_name[:-3]
          else:
            logging.warning(
                'Unuspported dependency definition: {0:s}'.format(line))
            dependency_name = ''

          if dependency_name:
            if dependency_name == 'libcrypto':
              preprocessor_definitions.append('HAVE_WINCRYPT')

              self._ConfigureLibcrypto(
                  project_information, release_project_configuration,
                  debug_project_configuration)

            elif dependency_name == 'libuuid':
              self._ConfigureLibuuid(
                  project_information, release_project_configuration,
                  debug_project_configuration)

            elif dependency_name != 'libfuse':
              dependencies.append(dependency_name)

      elif in_sources_section:
        if not line:
          in_sources_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          _, _, directory_name = os.path.dirname(
              makefile_am_path).rpartition(os.path.sep)

          for filename in line.split(' '):
            if filename.endswith('.c') or filename.endswith('.cpp'):
              source_files.append('\\'.join([
                  '..', '..', directory_name, filename]))

            elif filename.endswith('.h'):
              header_files.append('\\'.join([
                  '..', '..', directory_name, filename]))

      if line.startswith('AM_CFLAGS') or line.startswith('AM_CPPFLAGS'):
        in_am_cppflags_section = True

      elif line.startswith('{0:s}_la_LIBADD'.format(project_name)):
        in_la_libadd_section = True

      elif line.startswith('{0:s}_la_SOURCES'.format(project_name)):
        in_la_sources_section = True

      elif line.startswith('{0:s}_LDADD'.format(project_name)):
        in_ldadd_section = True

      elif line.startswith('{0:s}_SOURCES'.format(project_name)):
        in_sources_section = True

      elif line.startswith('EXTRA_DIST'):
        in_extra_dist_section = True

    file_object.close()

    if project_name in ('libcaes', 'libhmac'):
      if 'HAVE_WINCRYPT' not in preprocessor_definitions:
        preprocessor_definitions.append('HAVE_WINCRYPT')

    if project_name.endswith('.net'):
      dependencies.append(solution_name)

    if dependencies:
      project_information.dependencies = dependencies
    else:
      project_information.dependencies = alternate_dependencies

    if 'bzip2' in project_information.dependencies:
      project_information.third_party_dependencies.append('bzip2')

    if 'zlib' in project_information.dependencies:
      project_information.third_party_dependencies.append('zlib')

    if project_name == solution_name:
      preprocessor_definitions.append(
          '{0:s}_DLL_EXPORT'.format(project_name.upper()))

    elif project_name.startswith('lib'):
      preprocessor_definitions.append(
          'HAVE_LOCAL_{0:s}'.format(project_name.upper()))

    else:
      preprocessor_definitions.append(
          '{0:s}_DLL_IMPORT'.format(solution_name.upper()))

    if project_name.startswith('py'):
      include_directories.append('{0:s}\\include'.format(self._python_path))

    release_project_configuration.include_directories = include_directories
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    debug_project_configuration.include_directories = include_directories
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    if project_name.endswith('.net'):
      dependency = '{0:s}.lib'.format(solution_name)
      additional_dependencies.append(dependency)

    for dependency in additional_dependencies:
      release_project_configuration.additional_dependencies.append(
          dependency)
      debug_project_configuration.additional_dependencies.append(
          dependency)

    project_information.source_files = sorted(source_files)
    project_information.header_files = sorted(header_files)
    project_information.resource_files = sorted(resource_files)

  def _ReadMakefilePrograms(self, makefile_am_path):
    """Reads the programs section in the Makefile.am.

    Args:
      makefile_am_path (str): path of the Makefile.am file.

    Returns:
      list[str]: binary program names.
    """
    file_object = open(makefile_am_path, 'r')

    bin_programs = []

    in_bin_programs_section = False

    for line in file_object.readlines():
      line = line.strip()

      if in_bin_programs_section:
        if not line:
          in_bin_programs_section = False

        else:
          if line.endswith(' \\'):
            line = line[:-2]

          bin_programs.append(line)

      elif line.endswith('_PROGRAMS = \\'):
        in_bin_programs_section = True

    file_object.close()

    return bin_programs

  # pylint: disable=arguments-differ
  def Convert(self, input_directory, output_version):
    """Converts a Visual Studio solution.

    Args:
      input_directory (str): path of the input directory.
      output_version (str): output Visual Studio version.

    Returns:
      bool: True if the conversion successful or False if not.
    """
    configure_ac_path = os.path.join(input_directory, 'configure.ac')
    if not os.path.exists(configure_ac_path):
      logging.warning('No such file: {0:s}.'.format(configure_ac_path))
      return False

    solution_name = None
    file_object = open(configure_ac_path, 'r')

    in_ac_init_section = False

    for line in file_object.readlines():
      line = line.strip()

      if in_ac_init_section:
        if line.startswith('[') and line.endswith('],'):
          solution_name = line[1:-2]
        break

      elif line.startswith('AC_INIT('):
        in_ac_init_section = True

    file_object.close()

    if not solution_name:
      logging.warning('Unable to determine solution name.')
      return False

    # Use the existing msvscpp solution file to determine the project
    # GUID so that they can be reused.
    project_guids_by_name = {}

    input_sln_path = os.path.join(
        input_directory, 'msvscpp', '{0:s}.sln'.format(solution_name))
    if os.path.exists(input_sln_path):
      solution_reader = readers.VS2008SolutionFileReader()
      solution_reader.Open(input_sln_path)

      if not solution_reader.ReadHeader():
        logging.warning('Unable to read solution file: {0:s} header.'.format(
            input_sln_path))
        return False

      solution_projects = solution_reader.ReadProjects()
      solution_reader.Close()

      for solution_project in solution_projects:
        project_guids_by_name[solution_project.name] = solution_project.guid

    solution_projects = []
    projects_by_guid = {}

    for directory_entry in os.listdir(input_directory):
      if not os.path.isdir(directory_entry):
        continue

      if (not directory_entry.startswith('lib') and
          not directory_entry.startswith('py') and
          directory_entry not in ('src', 'tests') and
          not directory_entry.endswith('.net') and
          not directory_entry.endswith('tools')):
        continue

      # Ignore the Python version specific build directories.
      if (directory_entry.startswith('py') and (
          directory_entry.endswith('2') or
          directory_entry.endswith('3') or
          not self._generate_python_dll)):
        continue

      makefile_am_path = os.path.join(
          input_directory, directory_entry, 'Makefile.am')
      if not os.path.exists(makefile_am_path):
        logging.warning('No such file: {0:s}.'.format(makefile_am_path))
        continue

      if (directory_entry in ('src', 'tests') or
          directory_entry.endswith('tools')):
        project_names = self._ReadMakefilePrograms(makefile_am_path)
      else:
        project_names = [directory_entry]

      for project_name in project_names:
        project_filename = '{0:s}\\{0:s}'.format(project_name)

        project_guid = project_guids_by_name.get(project_name, '')
        if not project_guid:
          project_guid = project_guids_by_name.get(
              '{0:s}.dll'.format(project_name), '')
        if not project_guid:
          project_guid = str(uuid.uuid4())

        solution_project = resources.VSSolutionProject(
            project_name, project_filename, project_guid)

        solution_projects.append(solution_project)

        project_information = resources.VSProjectInformation()
        project_information.name = project_name
        project_information.guid = project_guid
        project_information.root_name_space = project_name

        if project_name == solution_name:
          release_project_configuration = ReleaseDllVSProjectConfiguration()
          debug_project_configuration = VSDebugDllVSProjectConfiguration()

        elif project_name.endswith('.net'):
          release_project_configuration = (
              ReleaseDotNetDllVSProjectConfiguration())
          debug_project_configuration = VSDebugDotNetDllVSProjectConfiguration()

        elif project_name.startswith('py'):
          release_project_configuration = (
              ReleasePythonDllVSProjectConfiguration(
                  python_path=self._python_path))
          debug_project_configuration = VSDebugPythonDllVSProjectConfiguration(
              python_path=self._python_path)

        elif project_name.startswith('lib'):
          release_project_configuration = ReleaseLibraryVSProjectConfiguration()
          debug_project_configuration = VSDebugLibraryVSProjectConfiguration()

        else:
          project_information.keyword = 'Win32Proj'

          release_project_configuration = ReleaseExeVSProjectConfiguration()
          debug_project_configuration = VSDebugExeVSProjectConfiguration()

        # TODO: determine autogenerated source.

        self._ReadMakefile(
            makefile_am_path, solution_name, project_information,
            release_project_configuration, debug_project_configuration)

        # TODO: add additional Python 3 project.

        project_information.configurations.Append(release_project_configuration)
        if debug_project_configuration:
          project_information.configurations.Append(debug_project_configuration)

        projects_by_guid[project_guid] = project_information

    self._CreateThirdPartyDepencies(
        solution_projects, projects_by_guid, project_guids_by_name)

    # Set-up the solution configurations.
    solution_configurations = resources.VSConfigurations()

    solution_configuration = resources.VSSolutionConfiguration(
        name='Release', platform='Win32')
    solution_configurations.Append(solution_configuration)

    solution_configuration = resources.VSSolutionConfiguration(
        name='VSDebug', platform='Win32')
    solution_configurations.Append(solution_configuration)

    if output_version not in ['2008']:
      # Add x64 as a platform.
      solution_configurations.ExtendWithX64(output_version)

    # Create some look-up dictionaries.
    solution_project_guids_by_name = {}
    solution_projects_by_guid = {}
    for solution_project in solution_projects:
      solution_project_guids_by_name[solution_project.name] = (
          solution_project.guid)
      solution_projects_by_guid[solution_project.guid] = solution_project

    # Set-up the solution dependencies.
    for guid, project_information in projects_by_guid.items():
      solution_project = solution_projects_by_guid[guid]

      for dependency in project_information.dependencies:
        if dependency in ['pthread']:
          continue

        dependency_guid = solution_project_guids_by_name.get(dependency, '')
        if not dependency_guid:
          logging.info('Missing GUID for dependency: {0:s}'.format(dependency))

        solution_project.AddDependency(dependency_guid)

    solution_filename = '{0:s}.sln'.format(solution_name)
    self._WriteSolution(
        solution_filename, output_version, solution_projects,
        solution_configurations)

    for solution_project in solution_projects:
      project_information = projects_by_guid[solution_project.guid]
      self._WriteProject(
          output_version, solution_project, project_information,
          solution_projects_by_guid)

    # Create the corresponding Makefile.am
    solution_project_filenames = []
    for solution_project in solution_projects:
      if output_version in ['2008']:
        solution_project_extension = 'vcproj'
      else:
        solution_project_extension = 'vcxproj'

      path_segments = solution_project.filename.split('\\')
      solution_project_filenames.append('\t{0:s}.{1:s} \\'.format(
          os.path.join(*path_segments), solution_project_extension))

    makefile_am_lines = ['MSVSCPP_FILES = \\']
    for solution_project_filename in sorted(solution_project_filenames):
      makefile_am_lines.append(solution_project_filename)

    makefile_am_lines.append('\t{0:s}'.format(solution_filename))

    makefile_am_lines.extend([
        '',
        'EXTRA_DIST = \\',
        '\t$(MSVSCPP_FILES)',
        '',
        'MAINTAINERCLEANFILES = \\',
        '\tMakefile.in',
        '',
        'distclean: clean',
        '\t/bin/rm -f Makefile',
        '',
        ''])

    filename = os.path.join('vs{0:s}'.format(output_version), 'Makefile.am')
    logging.info('Writing: {0:s}'.format(filename))

    makefile_am = open(filename, 'wb')
    makefile_am.write('\n'.join(makefile_am_lines))
    makefile_am.close()

    return True
