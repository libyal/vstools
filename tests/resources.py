# -*- coding: utf-8 -*-
"""Tests for the project and solution classes."""

import unittest

from vstools import resources

from tests import test_lib


class VSConfigurationTest(test_lib.BaseTestCase):
  """Visual Studio configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = resources.VSConfiguration()
    self.assertIsNotNone(configuration)


class VSConfigurationsTest(test_lib.BaseTestCase):
  """Visual Studio solution and project configurations tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configurations = resources.VSConfigurations()
    self.assertIsNotNone(configurations)

  # TODO: add tests for number_of_configurations property
  # TODO: add tests for Append function
  # TODO: add tests for ExtendWithX64 function
  # TODO: add tests for GetByIdentifier function
  # TODO: add tests for GetSorted function


class VSProjectConfigurationTests(test_lib.BaseTestCase):
  """Visual Studio project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    project_configuration = resources.VSProjectConfiguration()
    self.assertIsNotNone(project_configuration)

  # TODO: add tests for basic_runtime_checks_string property
  # TODO: add tests for character_set_string property
  # TODO: add tests for compile_as_string property
  # TODO: add tests for data_execution_prevention_string property
  # TODO: add tests for debug_information_format_string property
  # TODO: add tests for enable_comdat_folding_string property
  # TODO: add tests for link_incremental_string property
  # TODO: add tests for optimize_references_string property
  # TODO: add tests for optimization_string property
  # TODO: add tests for output_type_string property
  # TODO: add tests for precompiled_header_string property
  # TODO: add tests for randomized_base_address_string property
  # TODO: add tests for runtime_librarian_string property
  # TODO: add tests for sub_system_string property
  # TODO: add tests for target_machine_string property
  # TODO: add tests for warning_level_string property
  # TODO: add tests for whole_program_optimization_string property
  # TODO: add tests for CopyToX64 function
  # TODO: add tests for GetPlatformToolset function


class VSProjectInformationTests(test_lib.BaseTestCase):
  """Visual Studio project information tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    project_information = resources.VSProjectInformation()
    self.assertIsNotNone(project_information)


class VSSolutionConfigurationTests(test_lib.BaseTestCase):
  """Visual Studio solution configuration tests."""

  # TODO: add tests for CopyToX64 function


class VSSolutionProjectTest(test_lib.BaseTestCase):
  """Visual Studio solution project tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    solution_project = resources.VSSolutionProject(u'name', u'file', u'guid')
    self.assertIsNotNone(solution_project)

  # TODO: add tests for AddDependency function


if __name__ == '__main__':
  unittest.main()
