# -*- coding: utf-8 -*-
"""Solution classes."""

from __future__ import unicode_literals

import logging
import os

from vstools import readers
from vstools import writers


class VSSolution(object):
  """Visual Studio solution."""

  def __init__(
      self, extend_with_x64=True, generate_python_dll=True,
      python_path='C:\\Python27'):
    """Initializes a Visual Studio solution.

    Args:
      extend_with_x64 (Optional[bool]): True if the solution should be
          extended with configuration for the x64 platform.
      generate_python_dll (Optional[bool]): True if a Python module DLL
          should be generated.
      python_path (Optional[str]): path to the Python installation.
    """
    super(VSSolution, self).__init__()
    self._extend_with_x64 = extend_with_x64
    self._generate_python_dll = generate_python_dll
    self._python_path = python_path

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
    input_project_filename = self._GetProjectFilename(
        input_version, input_project_filename)

    if not os.path.exists(input_project_filename):
      return False

    project_reader = self._GetProjectFileReader(input_version)

    logging.info('Reading: {0:s}'.format(input_project_filename))

    project_reader.Open(input_project_filename)

    if not project_reader.ReadHeader():
      return False

    project_information = project_reader.ReadProject()
    project_reader.Close()

    if solution_project.name.startswith('py'):
      for project_configuration in (
          project_information.configurations.GetSorted()):
        if 'C:\\Python27\\include' in project_configuration.include_directories:
          project_configuration.include_directories.remove(
              'C:\\Python27\\include')
          project_configuration.include_directories.append(
              '{0:s}\\include'.format(self._python_path))

        if 'C:\\Python27\\libs' in project_configuration.library_directories:
          project_configuration.library_directories.remove('C:\\Python27\\libs')
          project_configuration.library_directories.append(
              '{0:s}\\libs'.format(self._python_path))

    if self._extend_with_x64:
      # Add x64 as a platform.
      project_information.configurations.ExtendWithX64(output_version)

    self._WriteProject(
        output_version, solution_project, project_information,
        solution_projects_by_guid)

    return True

  def _GetProjectFilename(self, version, project_filename):
    """Retrieves a Visual Studio version specific project filename.

    Args:
      version (str): version of the Visual Studio solution.
      project_filename (str): project filename without extension.

    Returns:
      str: project filename with extension or None if version is not supported.
    """
    if version == '2008':
      return '{0:s}.vcproj'.format(project_filename)
    elif version in ('2010', '2012', '2013', '2015', '2017'):
      return '{0:s}.vcxproj'.format(project_filename)

  def _GetProjectFileReader(self, input_version):
    """Retrieves a Visual Studio project file reader.

    Args:
      input_version (str): input version of the Visual Studio solution.

    Returns:
      VSProjectFileReader: Visual Studio project file reader or None if version
          is not supported.
    """
    if input_version == '2008':
      return readers.VS2008ProjectFileReader()
    elif input_version == '2010':
      return readers.VS2010ProjectFileReader()
    elif input_version == '2012':
      return readers.VS2012ProjectFileReader()
    elif input_version == '2013':
      return readers.VS2013ProjectFileReader()
    elif input_version == '2015':
      return readers.VS2015ProjectFileReader()
    elif input_version == '2017':
      return readers.VS2017ProjectFileReader()

  def _GetProjectFileWriter(self, output_version):
    """Retrieves a Visual Studio project file writer.

    Args:
      output_version (str): output version of the Visual Studio solution.

    Returns:
      VSProjectFileWriter: Visual Studio project file writer or None if version
          is not supported.
    """
    if output_version == '2008':
      return writers.VS2008ProjectFileWriter()
    elif output_version == '2010':
      return writers.VS2010ProjectFileWriter()
    elif output_version == '2012':
      return writers.VS2012ProjectFileWriter()
    elif output_version == '2013':
      return writers.VS2013ProjectFileWriter()
    elif output_version == '2015':
      return writers.VS2015ProjectFileWriter()
    elif output_version == '2017':
      return writers.VS2017ProjectFileWriter()

  def _GetSolutionFileReader(self, input_version):
    """Retrieves a Visual Studio solution file reader.

    Args:
      input_version (str): input version of the Visual Studio solution.

    Returns:
      VSSolutionFileReader: Visual Studio solution file reader or None if
          version is not supported.
    """
    if input_version == '2008':
      return readers.VS2008SolutionFileReader()
    elif input_version == '2010':
      return readers.VS2010SolutionFileReader()
    elif input_version == '2012':
      return readers.VS2012SolutionFileReader()
    elif input_version == '2013':
      return readers.VS2013SolutionFileReader()
    elif input_version == '2015':
      return readers.VS2015SolutionFileReader()
    elif input_version == '2017':
      return readers.VS2017SolutionFileReader()

  def _GetSolutionFileWriter(self, output_version):
    """Retrieves a Visual Studio solution file writer.

    Args:
      output_version (str): output version of the Visual Studio solution.

    Returns:
      VSSolutionFileWriter: Visual Studio solution file writer or None if
          version is not supported.
    """
    if output_version == '2008':
      return writers.VS2008SolutionFileWriter()
    elif output_version == '2010':
      return writers.VS2010SolutionFileWriter()
    elif output_version == '2012':
      return writers.VS2012SolutionFileWriter()
    elif output_version == '2013':
      return writers.VS2013SolutionFileWriter()
    elif output_version == '2015':
      return writers.VS2015SolutionFileWriter()
    elif output_version == '2017':
      return writers.VS2017SolutionFileWriter()

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
    output_project_filename = self._GetProjectFilename(
        output_version, output_project_filename)

    output_directory = os.path.dirname(output_project_filename)
    os.mkdir(output_directory)

    project_writer = self._GetProjectFileWriter(output_version)

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

    solution_writer = self._GetSolutionFileWriter(output_version)

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

    solution_reader = self._GetSolutionFileReader(input_version)

    solution_reader.Open(input_sln_path)

    if not solution_reader.ReadHeader():
      return False

    solution_projects = solution_reader.ReadProjects()
    solution_configurations = solution_reader.ReadConfigurations()
    solution_reader.Close()

    if not self._generate_python_dll:
      python_module_project = None
      for solution_project in solution_projects:
        if solution_project.name.startswith('py'):
          python_module_project = solution_project

      if python_module_project:
        solution_projects.remove(python_module_project)

    if self._extend_with_x64:
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
