# -*- coding: utf-8 -*-
"""Tests for the project and solution file reader classes."""

from __future__ import unicode_literals

import io
import unittest

from vstools import readers
from vstools import resources

from tests import test_lib


class FileReaderTest(test_lib.BaseTestCase):
  """File reader tests."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    file_reader = readers.FileReader()
    self.assertIsNotNone(file_reader)

  @test_lib.skipUnlessHasTestFile(['2008.sln'])
  def testReadBinaryData(self):
    """Tests the _ReadBinaryData function."""
    file_reader = readers.FileReader()

    path = self._GetTestFilePath(['2008.sln'])
    file_reader.Open(path)

    binary_data = file_reader._ReadBinaryData(5)
    self.assertEqual(binary_data, b'\xef\xbb\xbf\r\n')

    file_reader.Close()

  @test_lib.skipUnlessHasTestFile(['2008.vcproj'])
  def testReadLine(self):
    """Tests the _ReadLine function."""
    file_reader = readers.FileReader()

    path = self._GetTestFilePath(['2008.vcproj'])
    file_reader.Open(path)

    file_reader._ReadLine()

    line_look_ahead = file_reader._ReadLine(look_ahead=True)
    line = file_reader._ReadLine()
    self.assertEqual(line, line_look_ahead)

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

  # pylint: disable=protected-access

  # TODO: add tests for _ParseConfigurationOption function.

  def testParseConfigurationOption(self):
    """Tests the _ParseConfigurationOption function."""
    project_configuration = resources.VSProjectConfiguration()

    file_reader = readers.VS2008ProjectFileReader()

    line = 'Optimization="0"'
    file_reader._ParseConfigurationOption(
        project_configuration, 'Optimization', 'optimization', line)
    self.assertEqual(project_configuration.optimization, '0')

  def testParseConfigurationOptions(self):
    """Tests the _ParseConfigurationOptions function."""
    project_configuration = resources.VSProjectConfiguration()

    file_reader = readers.VS2008ProjectFileReader()

    configuration_options = {'Optimization': 'optimization'}

    line = 'Optimization="0"'
    file_reader._ParseConfigurationOptions(
        project_configuration, configuration_options, line)
    self.assertEqual(project_configuration.optimization, '0')

  def testReadConfiguration(self):
    """Tests the _ReadConfiguration function."""
    test_data = [
        '                        Name="Release|Win32"',
        ('                        OutputDirectory='
         '"$(SolutionDir)$(ConfigurationName)"'),
        '                        IntermediateDirectory="$(ConfigurationName)"',
        '                        ConfigurationType="2"',
        '                        CharacterSet="1"',
        '                        >',
        '                </Configuration>']

    file_reader = readers.VS2008ProjectFileReader()

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)

    project_configuration = file_reader._ReadConfiguration('<Configuration')
    self.assertIsNotNone(project_configuration)

    self.assertEqual(project_configuration.character_set, '1')
    self.assertEqual(project_configuration.output_type, '2')

    project_configuration = file_reader._ReadConfiguration('')
    self.assertIsNone(project_configuration)

  # TODO: add tests for _ReadConfigurations function.

  def testReadFiles(self):
    """Tests the _ReadFiles function."""
    test_data = [
        '        <Files>',
        '                <Filter',
        '                        Name="Source Files"',
        ('                        Filter='
         '"cpp;c;cc;cxx;def;odl;idl;hpj;bat;asm;asmx"'),
        ('                        UniqueIdentifier='
         '"{4FC737F1-C7A5-4376-A066-2A32D752A2FF}"'),
        '                        >',
        '                        <File',
        '                                RelativePath="test.c"',
        '                                >',
        '                        </File>',
        '                </Filter>',
        '        </Files>']

    project_information = resources.VSProjectInformation()

    file_reader = readers.VS2008ProjectFileReader()

    file_data = '\n'.join(test_data).encode('utf-8')
    file_reader._file = io.BytesIO(file_data)
    file_reader._ReadFiles(project_information)

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
# TODO: add tests for VS2017ProjectFileReader


class VSSolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio solution file reader tests."""

  def testCheckVisualStudioVersion(self):
    """Tests the _CheckVisualStudioVersion function."""
    file_reader = readers.VS2012SolutionFileReader()

    result = file_reader._CheckVisualStudioVersion('')
    self.assertFalse(result)

  # TODO: add tests for ReadConfigurations function.
  # TODO: add tests for ReadHeader function.
  # TODO: add tests for ReadProject function.
  # TODO: add tests for ReadProjects function.


class VS2008SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2008 solution file reader tests."""

  # pylint: disable=protected-access

  def testCheckFormatVersion(self):
    """Tests the _CheckFormatVersion function."""
    file_reader = readers.VS2008SolutionFileReader()

    line = 'Microsoft Visual Studio Solution File, Format Version 10.00'
    result = file_reader._CheckFormatVersion(line)
    self.assertTrue(result)

    line = 'Microsoft Visual Studio Solution File, Format Version BOGUS'
    result = file_reader._CheckFormatVersion(line)
    self.assertFalse(result)

  @test_lib.skipUnlessHasTestFile(['2008.sln'])
  def testReadHeader(self):
    """Tests the ReadHeader function."""
    file_reader = readers.VS2008SolutionFileReader()

    path = self._GetTestFilePath(['2008.sln'])
    file_reader.Open(path)

    result = file_reader.ReadHeader()
    self.assertTrue(result)

    file_reader.Close()

  @test_lib.skipUnlessHasTestFile(['2008.sln'])
  def testReadProjects(self):
    """Tests the ReadProjects function."""
    file_reader = readers.VS2008SolutionFileReader()

    path = self._GetTestFilePath(['2008.sln'])
    file_reader.Open(path)

    file_reader.ReadHeader()

    solution_projects = file_reader.ReadProjects()
    self.assertEqual(len(solution_projects), 3)

    file_reader.Close()


class VS2010SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2010 solution file reader tests."""

  # pylint: disable=protected-access

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

  # pylint: disable=protected-access

  def testCheckFormatVersion(self):
    """Tests the _CheckFormatVersion function."""
    file_reader = readers.VS2012SolutionFileReader()

    line = 'Microsoft Visual Studio Solution File, Format Version 12.00'
    result = file_reader._CheckFormatVersion(line)
    self.assertTrue(result)

    line = 'Microsoft Visual Studio Solution File, Format Version BOGUS'
    result = file_reader._CheckFormatVersion(line)
    self.assertFalse(result)


class VS2013SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2013 solution file reader tests."""

  # pylint: disable=protected-access

  def testCheckVisualStudioVersion(self):
    """Tests the _CheckVisualStudioVersion function."""
    file_reader = readers.VS2013SolutionFileReader()

    line = 'VisualStudioVersion = 12.0.21005.10'
    result = file_reader._CheckVisualStudioVersion(line)
    self.assertTrue(result)

    line = 'VisualStudioVersion = BOGUS'
    result = file_reader._CheckVisualStudioVersion(line)
    self.assertFalse(result)


class VS2015SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2015 solution file reader tests."""

  # pylint: disable=protected-access

  def testCheckVisualStudioVersion(self):
    """Tests the _CheckVisualStudioVersion function."""
    file_reader = readers.VS2015SolutionFileReader()

    line = 'VisualStudioVersion = 14.0.25420.1'
    result = file_reader._CheckVisualStudioVersion(line)
    self.assertTrue(result)

    line = 'VisualStudioVersion = BOGUS'
    result = file_reader._CheckVisualStudioVersion(line)
    self.assertFalse(result)


class VS2017SolutionFileReaderTest(test_lib.BaseTestCase):
  """Visual Studio 2017 solution file reader tests."""

  # pylint: disable=protected-access

  def testCheckVisualStudioVersion(self):
    """Tests the _CheckVisualStudioVersion function."""
    file_reader = readers.VS2017SolutionFileReader()

    line = 'VisualStudioVersion = 15.0.26730.10'
    result = file_reader._CheckVisualStudioVersion(line)
    self.assertTrue(result)

    line = 'VisualStudioVersion = BOGUS'
    result = file_reader._CheckVisualStudioVersion(line)
    self.assertFalse(result)


if __name__ == '__main__':
  unittest.main()
