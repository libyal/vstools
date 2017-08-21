# -*- coding: utf-8 -*-
"""Tests for the libyal sources classes."""

from __future__ import unicode_literals

import unittest

from vstools import libyal
from vstools import resources

from tests import test_lib


class LibyalReleaseVSProjectConfigurationTest(test_lib.BaseTestCase):
  """Libyal release VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleaseVSProjectConfiguration()
    self.assertIsNotNone(configuration)


class LibyalDebugVSProjectConfigurationTest(test_lib.BaseTestCase):
  """Libyal debug VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugVSProjectConfiguration()
    self.assertIsNotNone(configuration)


class LibyalSourceVSSolutionTest(test_lib.BaseTestCase):
  """Libyal source Visual Studio solution generator tests."""

  # pylint: disable=protected-access

  def testConfigureAsBzip2Dll(self):
    """Tests the _ConfigureAsBzip2Dll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsBzip2Dll(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        '..\\..\\..\\bzip2\\compress.c', project_information.source_files)

    self.assertIn(
        '..\\..\\..\\bzip2\\bzlib.h', project_information.header_files)

    self.assertTrue(
        release_project_configuration.include_directories.endswith(
            '..\\..\\..\\bzip2'))

    self.assertTrue(
        release_project_configuration.preprocessor_definitions.endswith(
            ';BZ_DLL'))

    self.assertTrue(
        debug_project_configuration.include_directories.endswith(
            '..\\..\\..\\bzip2'))

    self.assertTrue(
        debug_project_configuration.preprocessor_definitions.endswith(
            ';BZ_DLL'))

  def testConfigureAsDll(self):
    """Tests the _ConfigureAsDll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsDll(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertEqual(release_project_configuration.output_type, '2')
    self.assertEqual(
        release_project_configuration.linker_output_file,
        '$(OutDir)\\$(ProjectName).dll')
    self.assertEqual(release_project_configuration.library_directories, '')
    self.assertEqual(release_project_configuration.randomized_base_address, '2')
    self.assertEqual(
        release_project_configuration.data_execution_prevention, '2')
    self.assertEqual(
        release_project_configuration.import_library,
        '$(OutDir)\\$(ProjectName).lib')
    self.assertTrue(release_project_configuration.linker_values_set)

    self.assertEqual(debug_project_configuration.output_type, '2')
    self.assertEqual(
        debug_project_configuration.linker_output_file,
        '$(OutDir)\\$(ProjectName).dll')
    self.assertEqual(debug_project_configuration.library_directories, '')
    self.assertEqual(
        debug_project_configuration.generate_debug_information, 'true')
    self.assertEqual(debug_project_configuration.randomized_base_address, '1')
    self.assertEqual(debug_project_configuration.data_execution_prevention, '1')
    self.assertEqual(
        debug_project_configuration.import_library,
        '$(OutDir)\\$(ProjectName).lib')
    self.assertTrue(debug_project_configuration.linker_values_set)

  def testConfigureAsDllWithDotNet(self):
    """Tests the _ConfigureAsDll function with a .net project."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsDll(
        project_information, release_project_configuration,
        debug_project_configuration)

    # TODO: complete tests.

  def testConfigureAsDllWithPython(self):
    """Tests the _ConfigureAsDll function with a Python project."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsDll(
        project_information, release_project_configuration,
        debug_project_configuration)

    # TODO: complete tests.

  def testConfigureAsDokanDll(self):
    """Tests the _ConfigureAsDokanDll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsDokanDll(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        '..\\..\\..\\dokan\\dokan\\dokan.c', project_information.source_files)

    self.assertIn(
        '..\\..\\..\\dokan\\dokan\\dokan.h', project_information.header_files)

    self.assertTrue(
        release_project_configuration.include_directories.endswith(
            '..\\..\\..\\dokan\\sys\\'))

    self.assertTrue(
        release_project_configuration.preprocessor_definitions.endswith(
            ';DOKAN_DLL'))

    self.assertEqual(
        release_project_configuration.module_definition_file,
        '..\\..\\..\\dokan\\dokan\\dokan.def')

    self.assertTrue(
        debug_project_configuration.include_directories.endswith(
            '..\\..\\..\\dokan\\sys\\'))

    self.assertTrue(
        debug_project_configuration.preprocessor_definitions.endswith(
            ';DOKAN_DLL'))

    self.assertEqual(
        debug_project_configuration.module_definition_file,
        '..\\..\\..\\dokan\\dokan\\dokan.def')

  def testConfigureAsExe(self):
    """Tests the _ConfigureAsExe function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsExe(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertEqual(project_information.keyword, 'Win32Proj')

    self.assertEqual(release_project_configuration.output_type, '1')
    self.assertEqual(
        release_project_configuration.whole_program_optimization, '1')
    self.assertEqual(release_project_configuration.link_incremental, '1')
    self.assertEqual(release_project_configuration.sub_system, '1')
    self.assertEqual(release_project_configuration.optimize_references, '2')
    self.assertEqual(release_project_configuration.enable_comdat_folding, '2')
    self.assertEqual(release_project_configuration.randomized_base_address, '2')
    self.assertEqual(
        release_project_configuration.data_execution_prevention, '2')
    self.assertEqual(release_project_configuration.target_machine, '1')
    self.assertTrue(release_project_configuration.linker_values_set)

    self.assertEqual(debug_project_configuration.output_type, '1')
    self.assertEqual(
        debug_project_configuration.generate_debug_information, 'true')
    self.assertEqual(debug_project_configuration.link_incremental, '1')
    self.assertEqual(debug_project_configuration.sub_system, '1')
    self.assertEqual(debug_project_configuration.optimize_references, '2')
    self.assertEqual(debug_project_configuration.enable_comdat_folding, '2')
    self.assertEqual(debug_project_configuration.randomized_base_address, '1')
    self.assertEqual(debug_project_configuration.data_execution_prevention, '1')
    self.assertEqual(debug_project_configuration.target_machine, '1')
    self.assertTrue(debug_project_configuration.linker_values_set)

  def testConfigureAsLibrary(self):
    """Tests the _ConfigureAsLibrary function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsLibrary(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertEqual(release_project_configuration.output_type, '4')
    self.assertEqual(
        release_project_configuration.librarian_output_file,
        '$(OutDir)\\$(ProjectName).lib')
    self.assertEqual(
        release_project_configuration.librarian_ignore_defaults, 'false')

    self.assertEqual(debug_project_configuration.output_type, '4')
    self.assertEqual(
        debug_project_configuration.librarian_output_file,
        '$(OutDir)\\$(ProjectName).lib')
    self.assertEqual(
        debug_project_configuration.librarian_ignore_defaults, 'false')

  def testConfigureAsZlibDll(self):
    """Tests the _ConfigureAsZlibDll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsZlibDll(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        '..\\..\\..\\zlib\\adler32.c', project_information.source_files)

    self.assertIn(
        '..\\..\\..\\zlib\\zlib.h', project_information.header_files)

    self.assertIn(
        '..\\..\\..\\zlib\\win32\\zlib1.rc', project_information.resource_files)

    self.assertTrue(
        release_project_configuration.include_directories.endswith(
            '..\\..\\..\\zlib'))

    self.assertTrue(
        release_project_configuration.preprocessor_definitions.endswith(
            ';ZLIB_DLL'))

    self.assertTrue(
        debug_project_configuration.include_directories.endswith(
            '..\\..\\..\\zlib'))

    self.assertTrue(
        debug_project_configuration.preprocessor_definitions.endswith(
            ';ZLIB_DLL'))

  def testConfigureLibcrypto(self):
    """Tests the _ConfigureLibcrypto function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureLibcrypto(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        'advapi32.lib', release_project_configuration.additional_dependencies)

    self.assertIn(
        'advapi32.lib', debug_project_configuration.additional_dependencies)

  def testConfigureLibuuid(self):
    """Tests the _ConfigureLibuuid function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureLibuuid(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        'rpcrt4.lib', release_project_configuration.additional_dependencies)

    self.assertIn(
        'rpcrt4.lib', debug_project_configuration.additional_dependencies)

  # TODO: add tests for _CreateThirdPartyDepencies
  # TODO: add tests for _ReadMakefile
  # TODO: add tests for _ReadMakefilePrograms
  # TODO: add tests for Convert


if __name__ == '__main__':
  unittest.main()
