# -*- coding: utf-8 -*-
"""Tests for the project and solution file writer classes."""

from __future__ import unicode_literals
import io
import os
import unittest

from vstools import resources
from vstools import writers

from tests import test_lib


class FileWriterTest(test_lib.BaseTestCase):
  """File writer tests."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    file_writer = writers.FileWriter()
    self.assertIsNotNone(file_writer)

  def testOpenClose(self):
    """Tests the Open and Close functions."""
    file_writer = writers.FileWriter()

    with test_lib.TempDirectory() as temp_directory:
      filename = os.path.join(temp_directory, 'testfile')
      file_writer.Open(filename)

      file_writer.Close()

  def testWriteBinaryData(self):
    """Tests the WriteBinaryData function."""
    file_writer = writers.FileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteBinaryData(b'Binary data')

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = b'Binary data'
    self.assertEqual(output_data, expected_output_data)

  def testWriteLine(self):
    """Tests the WriteLine function."""
    file_writer = writers.FileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteLine('Line of text')

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = b'Line of text\r\n'
    self.assertEqual(output_data, expected_output_data)

  def testWriteLines(self):
    """Tests the WriteLines function."""
    file_writer = writers.FileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteLines([
        'First line of text',
        'Second line of text'])

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'First line of text\r\nSecond line of text\r\n')
    self.assertEqual(output_data, expected_output_data)


class VS2008ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2008 project file writer test."""

  # pylint: disable=protected-access

  # TODO: add tests for _WriteConfiguration function.
  # TODO: add tests for _WriteHeaderFiles function.
  # TODO: add tests for _WriteResourceFiles function.
  # TODO: add tests for _WriteSourceFiles function.

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = b'<?xml version="1.0" encoding="Windows-1252"?>'
    self.assertEqual(output_data, expected_output_data)

  # TODO: add tests for WriteConfigurations function.
  # TODO: add tests for WriteDependencies function.
  # TODO: add tests for WriteFiles function.

  def testWriteFooter(self):
    """Tests the WriteFooter function."""
    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = b'</VisualStudioProject>'
    self.assertEqual(output_data, expected_output_data)

  # TODO: add tests for WriteProjectConfigurations function.
  # TODO: add tests for WriteProjectInformation function.


# TODO: add tests for VS2010ProjectFileWriter
# TODO: add tests for VS2012ProjectFileWriter
# TODO: add tests for VS2013ProjectFileWriter
# TODO: add tests for VS2015ProjectFileWriter
# TODO: add tests for VSSolutionFileWriter
# TODO: add tests for VS2008SolutionFileWriter
# TODO: add tests for VS2010SolutionFileWriter


class VS2012SolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2012 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2012SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 12.00\r\n'
        b'# Visual Studio Express 2012 for Windows Desktop\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteProject(self):
    """Tests the WriteProject function."""
    file_writer = writers.VS2012SolutionFileWriter()

    file_writer._file = io.BytesIO()

    solution_project = resources.VSSolutionProject(
        'name', 'filename', 'guid')
    file_writer.WriteProject(solution_project)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "name", '
        b'"filename.vcxproj", "{GUID}"\r\nEndProject\r\n')
    self.assertEqual(output_data, expected_output_data)


class VS2013SolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2013 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2013SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 12.00\r\n'
        b'# Visual Studio Express 2013 for Windows Desktop\r\n'
        b'VisualStudioVersion = 12.0.21005.1\r\n'
        b'MinimumVisualStudioVersion = 10.0.40219.1\r\n')
    self.assertEqual(output_data, expected_output_data)


class VS2015SolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2015 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2015SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 12.00\r\n'
        b'# Visual Studio 14\r\n'
        b'VisualStudioVersion = 14.0.25420.1\r\n'
        b'MinimumVisualStudioVersion = 10.0.40219.1\r\n')
    self.assertEqual(output_data, expected_output_data)


if __name__ == '__main__':
  unittest.main()
