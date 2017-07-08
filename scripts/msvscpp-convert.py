#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to generate different versions of Visual Studio (express) files.

Currently supported input formats:
* libyal source directory (configure.ac and Makefile.am)
* 2008 (9.0)

Currently supported output formats:
* 2008 (9.0)
* 2010 (10.0)
* 2012 (11.0)
* 2013 (12.0)
* 2015 (14.0)
"""

# TODO: add automated tests.
# TODO: add vs2010 reader.
# TODO: add vs2012 reader.
# TODO: add vs2013 reader.
# TODO: add vs2015 reader.
# TODO: add vs2017 reader.
# TODO: add vs2017 writer.

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import logging
import os
import sys
import uuid

from vstools import readers
from vstools import resources
from vstools import writers


class VSSolution(object):
  """Visual Studio solution."""

  def _ConvertProject(
      self, input_version, input_directory, output_version, solution_project,
      solution_projects_by_guid):
    """Converts a Visual Studio project.

    Args:
      input_version (str): input version of the Visual Studio solution.
      input_directory (str): path of the input directory.
      output_version (str): output Visual Studio version.
      solution_project (VSSolutionProject): project.
      solution_projects_by_guid (dict[str, VSSolutionProject]): projects
          per lower case GUID.

    Returns:
      bool: True if the conversion successful or False if not.
    """
    if not solution_project:
      return False

    input_project_filename = input_directory
    for path_segment in solution_project.filename.split('\\'):
      input_project_filename = os.path.join(
          input_project_filename, path_segment)

    # TODO: move logic into the reader?
    if input_version == '2008':
      input_project_filename = '{0:s}.vcproj'.format(input_project_filename)
    elif output_version in ('2010', '2012', '2013', '2015'):
      input_project_filename = '{0:s}.vcxproj'.format(input_project_filename)

    if not os.path.exists(input_project_filename):
      return False

    if input_version == '2008':
      project_reader = readers.VS2008ProjectFileReader()
    elif input_version == '2010':
      project_reader = readers.VS2010ProjectFileReader()
    elif input_version == '2012':
      project_reader = readers.VS2012ProjectFileReader()
    elif input_version == '2013':
      project_reader = readers.VS2013ProjectFileReader()
    elif input_version == '2015':
      project_reader = readers.VS2015ProjectFileReader()

    logging.info('Reading: {0:s}'.format(input_project_filename))

    project_reader.Open(input_project_filename)

    if not project_reader.ReadHeader():
      return False

    project_information = project_reader.ReadProject()
    project_reader.Close()

    # Add x64 as a platform.
    project_information.configurations.ExtendWithX64(output_version)

    self._WriteProject(
        output_version, solution_project, project_information,
        solution_projects_by_guid)

    return True

  def _WriteProject(
      self, output_version, solution_project, project_information,
      solution_projects_by_guid):
    """Writes a Visual Studio project file.

    Args:
      output_version (str): output Visual Studio version.
      solution_project (VSSolutionProject): project.
      project_information (VSProjectInformation): project information.
      solution_projects_by_guid (dict[str, VSSolutionProject]): projects
          per lower case GUID.
    """
    output_directory = 'vs{0:s}'.format(output_version)
    output_project_filename = output_directory
    for path_segment in solution_project.filename.split('\\'):
      output_project_filename = os.path.join(
          output_project_filename, path_segment)

    # TODO: move logic into the writer?
    if output_version == '2008':
      output_project_filename = '{0:s}.vcproj'.format(output_project_filename)
    elif output_version in ('2010', '2012', '2013', '2015'):
      output_project_filename = '{0:s}.vcxproj'.format(output_project_filename)

    output_directory = os.path.dirname(output_project_filename)
    os.mkdir(output_directory)

    if output_version == '2008':
      project_writer = writers.VS2008ProjectFileWriter()
    elif output_version == '2010':
      project_writer = writers.VS2010ProjectFileWriter()
    elif output_version == '2012':
      project_writer = writers.VS2012ProjectFileWriter()
    elif output_version == '2013':
      project_writer = writers.VS2013ProjectFileWriter()
    elif output_version == '2015':
      project_writer = writers.VS2015ProjectFileWriter()

    logging.info('Writing: {0:s}'.format(output_project_filename))

    project_writer.Open(output_project_filename)
    project_writer.WriteHeader()
    project_writer.WriteProjectConfigurations(
        project_information.configurations)
    project_writer.WriteProjectInformation(project_information)
    project_writer.WriteConfigurations(project_information.configurations)
    project_writer.WriteFiles(
        project_information.source_files, project_information.header_files,
        project_information.resource_files)
    project_writer.WriteDependencies(
        solution_project.dependencies, solution_projects_by_guid)
    project_writer.WriteFooter()
    project_writer.Close()

  def _WriteSolution(
      self, solution_filename, output_version, solution_projects,
      solution_configurations):
    """Writes a Visual Studio solution file.

    Args:
      solution_filename (str): the Visual Studio solution filename.
      output_version (str): output Visual Studio version.
      solution_projects (list[VSSolutionProject]): projects.
      solution_configurations (VSConfigurations): configurations.
    """
    output_directory = 'vs{0:s}'.format(output_version)
    os.mkdir(output_directory)

    output_sln_filename = os.path.join(output_directory, solution_filename)

    logging.info('Writing: {0:s}'.format(output_sln_filename))

    if output_version == '2008':
      solution_writer = writers.VS2008SolutionFileWriter()
    elif output_version == '2010':
      solution_writer = writers.VS2010SolutionFileWriter()
    elif output_version == '2012':
      solution_writer = writers.VS2012SolutionFileWriter()
    elif output_version == '2013':
      solution_writer = writers.VS2013SolutionFileWriter()
    elif output_version == '2015':
      solution_writer = writers.VS2015SolutionFileWriter()

    solution_writer.Open(output_sln_filename)
    solution_writer.WriteHeader()
    solution_writer.WriteProjects(solution_projects)
    solution_writer.WriteConfigurations(
        solution_configurations, solution_projects)
    solution_writer.Close()

  def Convert(self, input_sln_path, output_version):
    """Converts a Visual Studio solution.

    Args:
      input_sln_path (str): path of the Visual Studio solution file.
      output_version (str): output Visual Studio version.

    Returns:
      bool: True if the conversion successful or False if not.
    """
    if not os.path.exists(input_sln_path):
      return False

    logging.info('Reading: {0:s}'.format(input_sln_path))

    # TODO: detect input version based on solution file reader?
    input_version = '2008'

    if input_version == '2008':
      solution_reader = readers.VS2008SolutionFileReader()
    elif input_version == '2010':
      solution_reader = readers.VS2010SolutionFileReader()
    elif input_version == '2012':
      solution_reader = readers.VS2012SolutionFileReader()
    elif input_version == '2013':
      solution_reader = readers.VS2013SolutionFileReader()
    elif input_version == '2015':
      solution_reader = readers.VS2015SolutionFileReader()

    solution_reader.Open(input_sln_path)

    if not solution_reader.ReadHeader():
      return False

    solution_projects = solution_reader.ReadProjects()
    solution_configurations = solution_reader.ReadConfigurations()
    solution_reader.Close()

    # Add x64 as a platform.
    solution_configurations.ExtendWithX64(output_version)

    solution_filename = os.path.basename(input_sln_path)
    self._WriteSolution(
        solution_filename, output_version, solution_projects,
        solution_configurations)

    input_directory = os.path.dirname(input_sln_path)

    solution_projects_by_guid = {}
    for solution_project in solution_projects:
      solution_projects_by_guid[solution_project.guid] = solution_project

    result = True
    for solution_project in solution_projects:
      result = self._ConvertProject(
          input_version, input_directory, output_version, solution_project,
          solution_projects_by_guid)
      if not result:
        break

    return result


class LibyalReleaseVSProjectConfiguration(resources.VSProjectConfiguration):
  """Libyal release VS project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(LibyalReleaseVSProjectConfiguration, self).__init__()

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


class LibyalDebugVSProjectConfiguration(resources.VSProjectConfiguration):
  """Libyal debug VS project configuration."""

  def __init__(self):
    """Initializes a Visual Studio project configuration."""
    super(LibyalDebugVSProjectConfiguration, self).__init__()

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


class LibyalSourceVSSolution(VSSolution):
  """Libyal source Visual Studio solution generator."""

  _SUPPORTED_THIRD_PARTY_DEPENDENCIES = frozenset([
      'bzip2', 'dokan', 'zlib'])

  def _ConfigureAsBzip2Dll(
      self, project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as the bzip2 DLL.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
          debug project configuration.
    """
    project_information.source_files = sorted([
        '..\\..\\..\\bzip2\\blocksort.c',
        '..\\..\\..\\bzip2\\bzlib.c',
        '..\\..\\..\\bzip2\\compress.c',
        '..\\..\\..\\bzip2\\crctable.c',
        '..\\..\\..\\bzip2\\decompress.c',
        '..\\..\\..\\bzip2\\huffman.c',
        '..\\..\\..\\bzip2\\randtable.c'])

    project_information.header_files = sorted([
        '..\\..\\..\\bzip2\\bzlib.h',
        '..\\..\\..\\bzip2\\bzlib_private.h'])

    include_directories = sorted([
        '..\\..\\..\\bzip2'])

    preprocessor_definitions = [
        'WIN32',
        'NDEBUG',
        '_WINDOWS',
        '_USRDLL',
        '_CRT_SECURE_NO_WARNINGS',
        'BZ_DLL']

    release_project_configuration.include_directories = ';'.join(
        include_directories)
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    debug_project_configuration.include_directories = ';'.join(
        include_directories)
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    self._ConfigureAsDll(
        project_information, release_project_configuration,
        debug_project_configuration)

  def _ConfigureAsDll(
      self, project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as a DLL.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
          debug project configuration.
    """
    if project_information.name.startswith('py'):
      dll_extension = 'pyd'
      library_directories = 'C:\\Python27\\libs'
    else:
      dll_extension = 'dll'
      library_directories = ''

    dll_filename = '$(OutDir)\\$(ProjectName).{0:s}'.format(dll_extension)
    lib_filename = '$(OutDir)\\$(ProjectName).lib'

    release_project_configuration.output_type = '2'
    release_project_configuration.linker_output_file = dll_filename
    release_project_configuration.library_directories = library_directories
    release_project_configuration.randomized_base_address = '2'
    release_project_configuration.data_execution_prevention = '2'
    release_project_configuration.import_library = lib_filename
    release_project_configuration.linker_values_set = True

    if project_information.name.endswith('.net'):
      release_project_configuration.compile_as = '2'
      release_project_configuration.managed_extensions = '1'

    debug_project_configuration.output_type = '2'
    debug_project_configuration.linker_output_file = dll_filename
    debug_project_configuration.library_directories = library_directories
    debug_project_configuration.generate_debug_information = 'true'
    debug_project_configuration.randomized_base_address = '1'
    debug_project_configuration.data_execution_prevention = '1'
    debug_project_configuration.import_library = lib_filename
    debug_project_configuration.linker_values_set = True

    if project_information.name.endswith('.net'):
      debug_project_configuration.compile_as = '2'
      debug_project_configuration.managed_extensions = '1'
      debug_project_configuration.basic_runtime_checks = ''
      debug_project_configuration.smaller_type_check = ''

  def _ConfigureAsDokanDll(
      self, project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as the dokan DLL.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
          debug project configuration.
    """
    project_information.source_files = sorted([
        '..\\..\\..\\dokan\\dokan\\access.c',
        '..\\..\\..\\dokan\\dokan\\cleanup.c',
        '..\\..\\..\\dokan\\dokan\\close.c',
        '..\\..\\..\\dokan\\dokan\\create.c',
        '..\\..\\..\\dokan\\dokan\\directory.c',
        '..\\..\\..\\dokan\\dokan\\dokan.c',
        '..\\..\\..\\dokan\\dokan\\fileinfo.c',
        '..\\..\\..\\dokan\\dokan\\flush.c',
        '..\\..\\..\\dokan\\dokan\\lock.c',
        '..\\..\\..\\dokan\\dokan\\mount.c',
        '..\\..\\..\\dokan\\dokan\\read.c',
        '..\\..\\..\\dokan\\dokan\\security.c',
        '..\\..\\..\\dokan\\dokan\\setfile.c',
        '..\\..\\..\\dokan\\dokan\\status.c',
        '..\\..\\..\\dokan\\dokan\\timeout.c',
        '..\\..\\..\\dokan\\dokan\\version.c',
        '..\\..\\..\\dokan\\dokan\\volume.c',
        '..\\..\\..\\dokan\\dokan\\write.c'])

    project_information.header_files = sorted([
        '..\\..\\..\\dokan\\dokan\\dokan.h',
        '..\\..\\..\\dokan\\dokan\\dokanc.h',
        '..\\..\\..\\dokan\\dokan\\dokani.h',
        '..\\..\\..\\dokan\\dokan\\fileinfo.h',
        '..\\..\\..\\dokan\\dokan\\list.h'])

    include_directories = sorted([
        '..\\..\\..\\dokan\\sys\\'])

    preprocessor_definitions = [
        'WIN32',
        'NDEBUG',
        '_WINDOWS',
        '_USRDLL',
        '_CRT_SECURE_NO_WARNINGS',
        'DOKAN_DLL']

    module_definition_file = '..\\..\\..\\dokan\\dokan\\dokan.def'

    release_project_configuration.include_directories = ';'.join(
        include_directories)
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)
    release_project_configuration.module_definition_file = (
        module_definition_file)

    debug_project_configuration.include_directories = ';'.join(
        include_directories)
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)
    debug_project_configuration.module_definition_file = (
        module_definition_file)

    self._ConfigureAsDll(
        project_information, release_project_configuration,
        debug_project_configuration)

  def _ConfigureAsExe(
      self, project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as an EXE.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
          debug project configuration.
    """
    project_information.keyword = 'Win32Proj'

    release_project_configuration.output_type = '1'

    release_project_configuration.whole_program_optimization = '1'

    # release_project_configuration.precompiled_header = '0'

    release_project_configuration.link_incremental = '1'
    release_project_configuration.sub_system = '1'
    release_project_configuration.optimize_references = '2'
    release_project_configuration.enable_comdat_folding = '2'
    release_project_configuration.randomized_base_address = '2'
    release_project_configuration.data_execution_prevention = '2'
    release_project_configuration.target_machine = '1'
    release_project_configuration.linker_values_set = True

    debug_project_configuration.output_type = '1'

    # debug_project_configuration.precompiled_header = '0'

    debug_project_configuration.generate_debug_information = 'true'
    debug_project_configuration.link_incremental = '1'
    debug_project_configuration.sub_system = '1'
    debug_project_configuration.optimize_references = '2'
    debug_project_configuration.enable_comdat_folding = '2'
    debug_project_configuration.randomized_base_address = '1'
    debug_project_configuration.data_execution_prevention = '1'
    debug_project_configuration.target_machine = '1'
    debug_project_configuration.linker_values_set = True

  def _ConfigureAsLibrary(
      self, unused_project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as a local library.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
          debug project configuration.
    """
    lib_filename = '$(OutDir)\\$(ProjectName).lib'

    release_project_configuration.output_type = '4'
    release_project_configuration.librarian_output_file = lib_filename
    release_project_configuration.librarian_ignore_defaults = 'false'

    debug_project_configuration.output_type = '4'
    debug_project_configuration.librarian_output_file = lib_filename
    debug_project_configuration.librarian_ignore_defaults = 'false'

  def _ConfigureAsZlibDll(
      self, project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project as the zlib DLL.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
          debug project configuration.
    """
    project_information.source_files = sorted([
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

    project_information.header_files = sorted([
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

    project_information.resource_files = sorted([
        '..\\..\\..\\zlib\\win32\\zlib1.rc'])

    include_directories = sorted([
        '..\\..\\..\\zlib'])

    preprocessor_definitions = [
        'WIN32',
        'NDEBUG',
        '_WINDOWS',
        '_USRDLL',
        '_CRT_SECURE_NO_WARNINGS',
        'ZLIB_DLL']

    release_project_configuration.include_directories = ';'.join(
        include_directories)
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    debug_project_configuration.include_directories = ';'.join(
        include_directories)
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    self._ConfigureAsDll(
        project_information, release_project_configuration,
        debug_project_configuration)

  def _ConfigureLibcrypto(
      self, unused_project_information, release_project_configuration,
      debug_project_configuration):
    """Configures the project for the Windows libcrypto equivalent.

    Args:
      project_information (VSProjectInformation): project information.
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
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
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
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

      project_information = resources.VSProjectInformation()

      project_information.name = project_name
      project_information.guid = project_guid
      project_information.root_name_space = project_name

      release_project_configuration = LibyalReleaseVSProjectConfiguration()
      debug_project_configuration = LibyalDebugVSProjectConfiguration()

      if project_name == 'bzip2':
        self._ConfigureAsBzip2Dll(
            project_information, release_project_configuration,
            debug_project_configuration)

      elif project_name == 'dokan':
        self._ConfigureAsDokanDll(
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
      release_project_configuration (LibyalReleaseVSProjectConfiguration):
          release project configuration.
      debug_project_configuration (LibyalReleaseVSProjectConfiguration):
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

              alternate_dependencies.append('dokan')

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

            elif dependency_name == 'libfuse':
              dependencies.append('dokan')

            elif dependency_name == 'libuuid':
              self._ConfigureLibuuid(
                  project_information, release_project_configuration,
                  debug_project_configuration)

            else:
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

    if 'dokan' in project_information.dependencies:
      project_information.third_party_dependencies.append('dokan')

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
      include_directories.append('C:\\Python27\\include')

    release_project_configuration.include_directories = ';'.join(
        include_directories)
    release_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    debug_project_configuration.include_directories = ';'.join(
        include_directories)
    debug_project_configuration.preprocessor_definitions = ';'.join(
        preprocessor_definitions)

    if project_name.endswith('.net'):
      dependency = '{0:s}.lib'.format(solution_name)

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
          directory_entry.endswith('3'))):
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

        release_project_configuration = LibyalReleaseVSProjectConfiguration()
        debug_project_configuration = LibyalDebugVSProjectConfiguration()

        # TODO: determine autogenerated source.

        self._ReadMakefile(
            makefile_am_path, solution_name, project_information,
            release_project_configuration, debug_project_configuration)

        # TODO: add additional Python 3 project.

        if (project_name == solution_name or project_name.startswith('py') or
            project_name.endswith('.net')):
          self._ConfigureAsDll(
              project_information, release_project_configuration,
              debug_project_configuration)

        elif project_name.startswith('lib'):
          self._ConfigureAsLibrary(
              project_information, release_project_configuration,
              debug_project_configuration)

        else:
          self._ConfigureAsExe(
              project_information, release_project_configuration,
              debug_project_configuration)

        project_information.configurations.Append(release_project_configuration)
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
    for guid, project_information in projects_by_guid.iteritems():
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


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  output_formats = frozenset(['2008', '2010', '2012', '2013', '2015'])

  argument_parser = argparse.ArgumentParser(description=(
      'Converts source directory (autoconf and automake files) into '
      'Visual Studio express solution and project files. It is also '
      'possible to convert from one version of Visual Studio to another.'))

  argument_parser.add_argument(
      'solution_file', nargs='?', action='store', metavar='FILENAME',
      default=None, help=(
          'The location of the source directory or the Visual Studio solution '
          'file (.sln).'))

  argument_parser.add_argument(
      '--to', dest='output_format', nargs='?', choices=sorted(output_formats),
      action='store', metavar='FORMAT', default='2010',
      help='The format to convert to.')

  options = argument_parser.parse_args()

  if not options.solution_file:
    print('Solution file missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  if options.output_format not in output_formats:
    print('Unsupported output format: {0:s}.'.format(options.format_to))
    print('')
    return False

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  if os.path.isdir(options.solution_file):
    input_solution = LibyalSourceVSSolution()
  else:
    input_solution = VSSolution()

  if not input_solution.Convert(options.solution_file, options.output_format):
    print('Unable to convert Visual Studio solution file.')
    return False

  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
