# -*- coding: utf-8 -*-
"""Tests for the libyal sources classes."""

from __future__ import unicode_literals

import unittest

from vstools import libyal
from vstools import resources

from tests import test_lib


class Bzip2VSProjectInformationTest(test_lib.BaseTestCase):
  """Bzip2 Visual Studio project information tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    project_information = libyal.Bzip2VSProjectInformation()

    self.assertIn(
        '..\\..\\..\\bzip2\\compress.c', project_information.source_files)

    self.assertIn(
        '..\\..\\..\\bzip2\\bzlib.h', project_information.header_files)


class DokanVSProjectInformationTest(test_lib.BaseTestCase):
  """Dokan Visual Studio project information tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    project_information = libyal.DokanVSProjectInformation()

    self.assertIn(
        '..\\..\\..\\dokan\\dokan\\dokan.c', project_information.source_files)

    self.assertIn(
        '..\\..\\..\\dokan\\dokan\\dokan.h', project_information.header_files)


class ZlibVSProjectInformationTest(test_lib.BaseTestCase):
  """Zlib Visual Studio project information tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    project_information = libyal.ZlibVSProjectInformation()

    self.assertIn(
        '..\\..\\..\\zlib\\adler32.c', project_information.source_files)

    self.assertIn(
        '..\\..\\..\\zlib\\zlib.h', project_information.header_files)

    self.assertIn(
        '..\\..\\..\\zlib\\win32\\zlib1.rc', project_information.resource_files)


class LibyalDebugVSProjectConfigurationTest(test_lib.BaseTestCase):
  """Libyal debug VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugVSProjectConfiguration()

    self.assertEqual(configuration.name, 'VSDebug')
    self.assertEqual(configuration.platform, 'Win32')
    self.assertEqual(configuration.character_set, '1')
    self.assertEqual(configuration.optimization, '0')
    self.assertEqual(configuration.basic_runtime_checks, '3')
    self.assertEqual(configuration.smaller_type_check, 'true')
    self.assertEqual(configuration.runtime_library, '3')
    self.assertEqual(configuration.warning_level, '4')
    self.assertEqual(configuration.debug_information_format, '3')
    self.assertEqual(configuration.compile_as, '1')
    self.assertEqual(configuration.target_machine, '1')


class LibyalDebugDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal debug DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugDllVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '2')
    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).dll')
    self.assertEqual(configuration.library_directories, '')
    self.assertEqual(configuration.generate_debug_information, 'true')
    self.assertEqual(configuration.randomized_base_address, '1')
    self.assertEqual(configuration.data_execution_prevention, '1')
    self.assertEqual(
        configuration.import_library, '$(OutDir)\\$(ProjectName).lib')
    self.assertTrue(configuration.linker_values_set)


class LibyalDebugDotNetDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal debug .Net DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugDotNetDllVSProjectConfiguration()

    self.assertEqual(configuration.compile_as, '2')
    self.assertEqual(configuration.managed_extensions, '1')
    self.assertEqual(configuration.basic_runtime_checks, '')
    self.assertEqual(configuration.smaller_type_check, '')


class LibyalDebugExeVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal debug EXE VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugExeVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '1')
    self.assertEqual(configuration.generate_debug_information, 'true')
    self.assertEqual(configuration.link_incremental, '1')
    self.assertEqual(configuration.sub_system, '1')
    self.assertEqual(configuration.optimize_references, '2')
    self.assertEqual(configuration.enable_comdat_folding, '2')
    self.assertEqual(configuration.randomized_base_address, '1')
    self.assertEqual(configuration.data_execution_prevention, '1')
    self.assertEqual(configuration.target_machine, '1')
    self.assertTrue(configuration.linker_values_set)


class LibyalDebugLibraryVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal debug library VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugLibraryVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '4')
    self.assertEqual(
        configuration.librarian_output_file, '$(OutDir)\\$(ProjectName).lib')
    self.assertEqual(configuration.librarian_ignore_defaults, 'false')


class LibyalDebugPythonDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal debug Python DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalDebugPythonDllVSProjectConfiguration()

    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).pyd')
    self.assertEqual(configuration.library_directories, 'C:\\Python27\\libs')


class LibyalReleaseVSProjectConfigurationTest(test_lib.BaseTestCase):
  """Libyal release VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleaseVSProjectConfiguration()

    self.assertEqual(configuration.name, 'Release')
    self.assertEqual(configuration.platform, 'Win32')
    self.assertEqual(configuration.character_set, '1')
    self.assertEqual(configuration.runtime_library, '2')
    self.assertEqual(configuration.warning_level, '4')
    self.assertEqual(configuration.compile_as, '1')
    self.assertEqual(configuration.target_machine, '1')


class LibyalReleaseDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal release DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleaseDllVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '2')
    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).dll')
    self.assertEqual(configuration.library_directories, '')
    self.assertEqual(configuration.randomized_base_address, '2')
    self.assertEqual(configuration.data_execution_prevention, '2')
    self.assertEqual(
        configuration.import_library, '$(OutDir)\\$(ProjectName).lib')
    self.assertTrue(configuration.linker_values_set)


class LibyalReleaseDotNetDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal release .Net DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleaseDotNetDllVSProjectConfiguration()

    self.assertEqual(configuration.compile_as, '2')
    self.assertEqual(configuration.managed_extensions, '1')


class LibyalReleaseExeVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal release EXE VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleaseExeVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '1')
    self.assertEqual(configuration.whole_program_optimization, '1')
    self.assertEqual(configuration.link_incremental, '1')
    self.assertEqual(configuration.sub_system, '1')
    self.assertEqual(configuration.optimize_references, '2')
    self.assertEqual(configuration.enable_comdat_folding, '2')
    self.assertEqual(configuration.randomized_base_address, '2')
    self.assertEqual(configuration.data_execution_prevention, '2')
    self.assertEqual(configuration.target_machine, '1')
    self.assertTrue(configuration.linker_values_set)


class LibyalReleaseLibraryVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal release library VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleaseLibraryVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '4')
    self.assertEqual(
        configuration.librarian_output_file, '$(OutDir)\\$(ProjectName).lib')
    self.assertEqual(configuration.librarian_ignore_defaults, 'false')


class LibyalReleasePythonDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Libyal release Python DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.LibyalReleasePythonDllVSProjectConfiguration()

    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).pyd')
    self.assertEqual(configuration.library_directories, 'C:\\Python27\\libs')


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

  def testConfigureAsDokanDll(self):
    """Tests the _ConfigureAsDokanDll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsDokanDll(
        project_information, release_project_configuration,
        debug_project_configuration)

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

  def testConfigureAsZlibDll(self):
    """Tests the _ConfigureAsZlibDll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.LibyalReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.LibyalDebugVSProjectConfiguration()

    solution._ConfigureAsZlibDll(
        project_information, release_project_configuration,
        debug_project_configuration)

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
