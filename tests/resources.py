# -*- coding: utf-8 -*-
"""Tests for the project and solution classes."""

from __future__ import unicode_literals

import unittest

from vstools import resources

from tests import test_lib


class VSConfigurationTest(test_lib.BaseTestCase):
  """Visual Studio configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = resources.VSConfiguration(name='test', platform='Win32')
    self.assertIsNotNone(configuration)


class VSConfigurationsTest(test_lib.BaseTestCase):
  """Visual Studio solution and project configurations tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configurations = resources.VSConfigurations()
    self.assertIsNotNone(configurations)

  def testNumberOfConfigurations(self):
    """Tests the number_of_configurations property."""
    configurations = resources.VSConfigurations()
    self.assertEqual(configurations.number_of_configurations, 0)

  def testAppend(self):
    """Tests the Append function."""
    configurations = resources.VSConfigurations()

    configuration = resources.VSSolutionConfiguration(
        name='test', platform='Win32')
    configurations.Append(configuration)

  def testExtendWithX64(self):
    """Tests the ExtendWithX64 function."""
    configurations = resources.VSConfigurations()

    configuration = resources.VSSolutionConfiguration(
        name='test', platform='Win32')
    configurations.Append(configuration)

    configurations.ExtendWithX64('2010')

  def testGetByIdentifier(self):
    """Tests the GetByIdentifier function."""
    configurations = resources.VSConfigurations()

    configuration = resources.VSSolutionConfiguration(
        name='test', platform='Win32')
    configurations.Append(configuration)

    configuration = configurations.GetByIdentifier('test', 'Win32')
    self.assertIsNotNone(configuration)

  def testGetSorted(self):
    """Tests the GetSorted function."""
    configurations = resources.VSConfigurations()

    configuration = resources.VSSolutionConfiguration(
        name='test', platform='Win32')
    configurations.Append(configuration)

    sorted_configurations = list(configurations.GetSorted())
    self.assertEqual(len(sorted_configurations), 1)


class VSProjectConfigurationTests(test_lib.BaseTestCase):
  """Visual Studio project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    project_configuration = resources.VSProjectConfiguration()
    self.assertIsNotNone(project_configuration)

  def testBasicRuntimeChecksString(self):
    """Tests the basic_runtime_checks_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.basic_runtime_checks = ''
    self.assertEqual(project_configuration.basic_runtime_checks_string, '')

    project_configuration.basic_runtime_checks = '0'
    self.assertEqual(
        project_configuration.basic_runtime_checks_string, 'Default')

    project_configuration.basic_runtime_checks = '3'
    self.assertEqual(
        project_configuration.basic_runtime_checks_string, 'EnableFastChecks')

    project_configuration.basic_runtime_checks = '-1'
    self.assertEqual(project_configuration.basic_runtime_checks_string, '')

  def testCharacterSetString(self):
    """Tests the character_set_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.character_set = ''
    self.assertEqual(project_configuration.character_set_string, '')

    project_configuration.character_set = '1'
    self.assertEqual(
        project_configuration.character_set_string, 'Unicode')

    project_configuration.character_set = '-1'
    self.assertEqual(project_configuration.character_set_string, '')

  def testCompilerAsString(self):
    """Tests the compile_as_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.compile_as = ''
    self.assertEqual(project_configuration.compile_as_string, '')

    project_configuration.compile_as = '1'
    self.assertEqual(
        project_configuration.compile_as_string, 'CompileAsC')

    project_configuration.compile_as = '2'
    self.assertEqual(
        project_configuration.compile_as_string, 'CompileAsCpp')

    project_configuration.compile_as = '-1'
    self.assertEqual(project_configuration.compile_as_string, '')

  def testDataExecutionPreventionString(self):
    """Tests the data_execution_prevention_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.data_execution_prevention = ''
    self.assertEqual(project_configuration.data_execution_prevention_string, '')

    project_configuration.data_execution_prevention = '1'
    self.assertEqual(
        project_configuration.data_execution_prevention_string, 'false')

    project_configuration.data_execution_prevention = '2'
    self.assertEqual(
        project_configuration.data_execution_prevention_string, 'true')

    project_configuration.data_execution_prevention = '-1'
    self.assertEqual(project_configuration.data_execution_prevention_string, '')

  def testDebugInformationFormatString(self):
    """Tests the debug_information_format_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.debug_information_format = ''
    self.assertEqual(project_configuration.debug_information_format_string, '')

    project_configuration.debug_information_format = '3'
    self.assertEqual(
        project_configuration.debug_information_format_string,
        'ProgramDatabase')

    project_configuration.debug_information_format = '-1'
    self.assertEqual(project_configuration.debug_information_format_string, '')

  def testEnableComdatFoldingString(self):
    """Tests the enable_comdat_folding_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.enable_comdat_folding = ''
    self.assertEqual(project_configuration.enable_comdat_folding_string, '')

    project_configuration.enable_comdat_folding = '2'
    self.assertEqual(
        project_configuration.enable_comdat_folding_string, 'true')

    project_configuration.enable_comdat_folding = '-1'
    self.assertEqual(project_configuration.enable_comdat_folding_string, '')

  def testLinkIncrementalString(self):
    """Tests the link_incremental_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.link_incremental = ''
    self.assertEqual(project_configuration.link_incremental_string, '')

    project_configuration.link_incremental = '1'
    self.assertEqual(
        project_configuration.link_incremental_string, 'false')

    project_configuration.link_incremental = '-1'
    self.assertEqual(project_configuration.link_incremental_string, '')

  def testOptimizeReferencesString(self):
    """Tests the optimize_references_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.optimize_references = ''
    self.assertEqual(project_configuration.optimize_references_string, '')

    project_configuration.optimize_references = '2'
    self.assertEqual(
        project_configuration.optimize_references_string, 'true')

    project_configuration.optimize_references = '-1'
    self.assertEqual(project_configuration.optimize_references_string, '')

  def testOptimizationString(self):
    """Tests the optimization_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.optimization = ''
    self.assertEqual(project_configuration.optimization_string, '')

    project_configuration.optimization = '0'
    self.assertEqual(
        project_configuration.optimization_string, 'Disabled')

    project_configuration.optimization = '2'
    self.assertEqual(
        project_configuration.optimization_string, 'MaxSpeed')

    project_configuration.optimization = '-1'
    self.assertEqual(project_configuration.optimization_string, '')

  def testOutputTypeString(self):
    """Tests the output_type_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.output_type = ''
    self.assertEqual(project_configuration.output_type_string, '')

    project_configuration.output_type = '1'
    self.assertEqual(
        project_configuration.output_type_string, 'Application')

    project_configuration.output_type = '2'
    self.assertEqual(
        project_configuration.output_type_string, 'DynamicLibrary')

    project_configuration.output_type = '4'
    self.assertEqual(
        project_configuration.output_type_string, 'StaticLibrary')

    project_configuration.output_type = '-1'
    self.assertEqual(project_configuration.output_type_string, '')

  def testPrecompiledHeaderString(self):
    """Tests the precompiled_header_string property."""
    project_configuration = resources.VSProjectConfiguration()

    project_configuration.precompiled_header = ''
    self.assertEqual(project_configuration.precompiled_header_string, '')

    # TODO: do something with precompiled_header.

    project_configuration.precompiled_header = '-1'
    self.assertEqual(project_configuration.precompiled_header_string, '')

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
    solution_project = resources.VSSolutionProject('name', 'file', 'guid')
    self.assertIsNotNone(solution_project)

  # TODO: add tests for AddDependency function


if __name__ == '__main__':
  unittest.main()
