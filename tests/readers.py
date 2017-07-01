# -*- coding: utf-8 -*-
"""Tests for the project and solution file reader classes."""

import io
import unittest

from vstools import readers
from vstools import resources

from tests import test_lib


class FileReaderTest(test_lib.BaseTestCase):
  """File reader tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    file_reader = readers.FileReader()
    self.assertIsNotNone(file_reader)

  @test_lib.skipUnlessHasTestFile(['2008.vcproj'])
  def testReadLine(self):
    """Tests the _ReadLine function."""
    file_reader = readers.FileReader()

    path = self._GetTestFilePath(['2008.vcproj'])
    file_reader.Open(path)

    line = file_reader._ReadLine()

    line = file_reader._ReadLine(look_ahead=True)
    line = file_reader._ReadLine()

    file_reader.Close()

  @test_lib.skipUnlessHasTestFile(['2008.vcproj'])
  def testOpenClose(self):
    """Tests the Open and Close functions."""
    file_reader = readers.FileReader()

    path = self._GetTestFilePath(['2008.vcproj'])
    file_reader.Open(path)

    file_reader.Close()


class VS2008ProjectFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2008 project file reader tests."""

  def testParseToolCompilerConfiguration(self):
    """Tests the _ParseToolCompilerConfiguration function."""
    project_configuration = resources.VSProjectConfiguration()

    file_reader = readers.VS2008ProjectFileReader()

    line = 'Optimization="0"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    # TODO: tests for EnableIntrinsicFunctions=

    line = 'AdditionalIncludeDirectories="..\..\include;..\..\common"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    line = 'PreprocessorDefinitions="_CRT_SECURE_NO_DEPRECATE"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    line = 'BasicRuntimeChecks="3"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    line = 'SmallerTypeCheck="true"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    line = 'RuntimeLibrary="3"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    # TODO: tests for EnableFunctionLevelLinking=
    # TODO: tests for UsePrecompiledHeader=

    line = 'WarningLevel="4"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    # TODO: tests for Detect64BitPortabilityProblems=
    # TODO: tests for WarnAsError=

    line = 'DebugInformationFormat="3"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

    line = 'CompileAs="1"'
    file_reader._ParseToolCompilerConfiguration(project_configuration, line)

  # TODO: add tests for _ParseToolLibrarianConfiguration function.

  def testParseToolLinkerConfiguration(self):
    """Tests the _ParseToolLinkerConfiguration function."""
    project_configuration = resources.VSProjectConfiguration()

    file_reader = readers.VS2008ProjectFileReader()

    # TODO: tests for OutputDirectory=

    line = 'OutputFile="$(OutDir)\$(ProjectName).dll"'
    file_reader._ParseToolLinkerConfiguration(project_configuration, line)

    # TODO: tests for AdditionalDependencies=
    # TODO: tests for LinkIncremental=
    # TODO: tests for ModuleDefinitionFile=

    line = 'AdditionalLibraryDirectories="&quot;$(OutDir)&quot;"'
    file_reader._ParseToolLinkerConfiguration(project_configuration, line)

    line = 'GenerateDebugInformation="true"'
    file_reader._ParseToolLinkerConfiguration(project_configuration, line)

    # TODO: tests for SubSystem=
    # TODO: tests for OptimizeReferences=

    line = 'RandomizedBaseAddress="1"'
    file_reader._ParseToolLinkerConfiguration(project_configuration, line)

    # TODO: add more tests.

  # TODO: add tests for _ReadConfiguration function.
  # TODO: add tests for _ReadConfigurations function.
  # TODO: add tests for _ReadFiles function.

  def testReadProjectInformation(self):
    """Tests the _ReadProjectInformation function."""
    test_data = [
        '        Name="libcerror"',
        '        ProjectGUID="{C42F5217-137D-4F10-9D6A-3C6D44E43453}"',
        '        RootNamespace="libcerror"',
        '        TargetFrameworkVersion="131072"',
        '        >']

    project_information = resources.VSProjectInformation()

    file_reader = readers.VS2008ProjectFileReader()

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    file_reader._ReadProjectInformation(project_information)

  def testReadHeader(self):
    """Tests the ReadHeader function."""
    test_data = [
        '<?xml version="1.0" encoding="Windows-1252"?>',
        '<VisualStudioProject',
        '        ProjectType="Visual C++"',
        '        Version="9,00"']

    file_reader = readers.VS2008ProjectFileReader()

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    result = file_reader.ReadHeader()
    self.assertTrue(result)

    test_data[3] = ''

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    result = file_reader.ReadHeader()
    self.assertFalse(result)

    test_data[2] = ''

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    result = file_reader.ReadHeader()
    self.assertFalse(result)

    test_data[1] = ''

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    result = file_reader.ReadHeader()
    self.assertFalse(result)

    test_data[0] = ''

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    result = file_reader.ReadHeader()
    self.assertFalse(result)

  @test_lib.skipUnlessHasTestFile(['2008.vcproj'])
  def testReadProject(self):
    """Tests the ReadProject function."""
    file_reader = readers.VS2008ProjectFileReader()

    path = self._GetTestFilePath(['2008.vcproj'])
    file_reader.Open(path)

    file_reader.ReadHeader()
    file_reader.ReadProject()

    file_reader.Close()


# TODO: add tests for VS2010ProjectFileReader
# TODO: add tests for VS2012ProjectFileReader
# TODO: add tests for VS2013ProjectFileReader
# TODO: add tests for VS2015ProjectFileReader


class VSSolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio solution file reader tests."""

  # TODO: add tests for ReadConfigurations function.
  # TODO: add tests for ReadHeader function.
  # TODO: add tests for ReadProject function.
  # TODO: add tests for ReadProjects function.


class VS2008SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2008 solution file reader tests."""

  def testCheckFormatVersion(self):
    """Tests the _CheckFormatVersion function."""
    file_reader = readers.VS2008SolutionFileReader()

    line = 'Microsoft Visual Studio Solution File, Format Version 10.00'
    result = file_reader._CheckFormatVersion(line)
    self.assertTrue(result)

    line = 'Microsoft Visual Studio Solution File, Format Version BOGUS'
    result = file_reader._CheckFormatVersion(line)
    self.assertFalse(result)


class VS2010SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2010 solution file reader tests."""

  def testCheckFormatVersion(self):
    """Tests the _CheckFormatVersion function."""
    file_reader = readers.VS2010SolutionFileReader()

    line = 'Microsoft Visual Studio Solution File, Format Version 11.00'
    result = file_reader._CheckFormatVersion(line)
    self.assertTrue(result)

    line = 'Microsoft Visual Studio Solution File, Format Version BOGUS'
    result = file_reader._CheckFormatVersion(line)
    self.assertFalse(result)


class VS2012SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2012 solution file reader tests."""

  def testCheckFormatVersion(self):
    """Tests the _CheckFormatVersion function."""
    file_reader = readers.VS2012SolutionFileReader()

    line = 'Microsoft Visual Studio Solution File, Format Version 12.00'
    result = file_reader._CheckFormatVersion(line)
    self.assertTrue(result)

    line = 'Microsoft Visual Studio Solution File, Format Version BOGUS'
    result = file_reader._CheckFormatVersion(line)
    self.assertFalse(result)


# TODO: add tests for VS2013SolutionFileReader
# TODO: add tests for VS2015SolutionFileReader


if __name__ == '__main__':
  unittest.main()
