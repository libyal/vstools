# -*- coding: utf-8 -*-
"""Solution classes."""

from __future__ import unicode_literals

import logging
import os

from vstools import readers
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
