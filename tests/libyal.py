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


class ReleaseVSProjectConfigurationTest(test_lib.BaseTestCase):
  """Release VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.ReleaseVSProjectConfiguration()

    self.assertEqual(configuration.name, 'Release')
    self.assertEqual(configuration.platform, 'Win32')
    self.assertEqual(configuration.character_set, '1')
    self.assertEqual(configuration.runtime_library, '2')
    self.assertEqual(configuration.warning_level, '4')
    self.assertEqual(configuration.compile_as, '1')
    self.assertEqual(configuration.target_machine, '1')


class ReleaseDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Release DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.ReleaseDllVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '2')
    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).dll')
    self.assertEqual(configuration.library_directories, '')
    self.assertEqual(configuration.randomized_base_address, '2')
    self.assertEqual(configuration.data_execution_prevention, '2')
    self.assertEqual(
        configuration.import_library, '$(OutDir)\\$(ProjectName).lib')
    self.assertTrue(configuration.linker_values_set)


class ReleaseDotNetDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Release .Net DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.ReleaseDotNetDllVSProjectConfiguration()

    self.assertEqual(configuration.compile_as, '2')
    self.assertEqual(configuration.managed_extensions, '1')


class ReleaseExeVSProjectConfiguration(test_lib.BaseTestCase):
  """Release EXE VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.ReleaseExeVSProjectConfiguration()

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


class ReleaseLibraryVSProjectConfiguration(test_lib.BaseTestCase):
  """Release library VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.ReleaseLibraryVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '4')
    self.assertEqual(
        configuration.librarian_output_file, '$(OutDir)\\$(ProjectName).lib')
    self.assertEqual(configuration.librarian_ignore_defaults, 'false')


class ReleasePythonDllVSProjectConfiguration(test_lib.BaseTestCase):
  """Release Python DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.ReleasePythonDllVSProjectConfiguration()

    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).pyd')
    self.assertEqual(configuration.library_directories, ['C:\\Python27\\libs'])


class VSDebugVSProjectConfigurationTest(test_lib.BaseTestCase):
  """VSDebug VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.VSDebugVSProjectConfiguration()

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


class VSDebugDllVSProjectConfiguration(test_lib.BaseTestCase):
  """VSDebug DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.VSDebugDllVSProjectConfiguration()

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


class VSDebugDotNetDllVSProjectConfiguration(test_lib.BaseTestCase):
  """VSDebug .Net DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.VSDebugDotNetDllVSProjectConfiguration()

    self.assertEqual(configuration.compile_as, '2')
    self.assertEqual(configuration.managed_extensions, '1')
    self.assertEqual(configuration.basic_runtime_checks, '')
    self.assertEqual(configuration.smaller_type_check, '')


class VSDebugExeVSProjectConfiguration(test_lib.BaseTestCase):
  """VSDebug EXE VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.VSDebugExeVSProjectConfiguration()

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


class VSDebugLibraryVSProjectConfiguration(test_lib.BaseTestCase):
  """VSDebug library VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.VSDebugLibraryVSProjectConfiguration()

    self.assertEqual(configuration.output_type, '4')
    self.assertEqual(
        configuration.librarian_output_file, '$(OutDir)\\$(ProjectName).lib')
    self.assertEqual(configuration.librarian_ignore_defaults, 'false')


class VSDebugPythonDllVSProjectConfiguration(test_lib.BaseTestCase):
  """VSDebug Python DLL VS project configuration tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    configuration = libyal.VSDebugPythonDllVSProjectConfiguration()

    self.assertEqual(
        configuration.linker_output_file, '$(OutDir)\\$(ProjectName).pyd')
    self.assertEqual(configuration.library_directories, ['C:\\Python27\\libs'])


class LibyalSourceVSSolutionTest(test_lib.BaseTestCase):
  """Libyal source Visual Studio solution generator tests."""

  # pylint: disable=protected-access

  def testConfigureAsBzip2Dll(self):
    """Tests the _ConfigureAsBzip2Dll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.ReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.VSDebugVSProjectConfiguration()

    solution._ConfigureAsBzip2Dll(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        '..\\..\\..\\bzip2', release_project_configuration.include_directories)

    self.assertTrue(
        release_project_configuration.preprocessor_definitions.endswith(
            ';BZ_DLL'))

    self.assertIn(
        '..\\..\\..\\bzip2', debug_project_configuration.include_directories)

    self.assertTrue(
        debug_project_configuration.preprocessor_definitions.endswith(
            ';BZ_DLL'))

  def testConfigureAsZlibDll(self):
    """Tests the _ConfigureAsZlibDll function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.ReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.VSDebugVSProjectConfiguration()

    solution._ConfigureAsZlibDll(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        '..\\..\\..\\zlib', release_project_configuration.include_directories)

    self.assertTrue(
        release_project_configuration.preprocessor_definitions.endswith(
            ';ZLIB_DLL'))

    self.assertIn(
        '..\\..\\..\\zlib', debug_project_configuration.include_directories)

    self.assertTrue(
        debug_project_configuration.preprocessor_definitions.endswith(
            ';ZLIB_DLL'))

  def testConfigureLibuuid(self):
    """Tests the _ConfigureLibuuid function."""
    solution = libyal.LibyalSourceVSSolution()

    project_information = resources.VSProjectInformation()
    release_project_configuration = libyal.ReleaseVSProjectConfiguration()
    debug_project_configuration = libyal.VSDebugVSProjectConfiguration()

    solution._ConfigureLibuuid(
        project_information, release_project_configuration,
        debug_project_configuration)

    self.assertIn(
        'rpcrt4.lib', release_project_configuration.additional_dependencies)

    self.assertIn(
        'rpcrt4.lib', debug_project_configuration.additional_dependencies)

  # TODO: add tests for _CreateThirdPartyDependencies
  # TODO: add tests for _ReadMakefile
  # TODO: add tests for _ReadMakefilePrograms
  # TODO: add tests for Convert


if __name__ == '__main__':
  unittest.main()
