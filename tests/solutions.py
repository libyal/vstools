# -*- coding: utf-8 -*-
"""Tests for the solution classes."""

from __future__ import unicode_literals

import unittest

from vstools import solutions

from tests import test_lib


class VSSolutionTest(test_lib.BaseTestCase):
  """Visual Studio solution tests."""

  # pylint: disable=protected-access

  # TODO: add tests for _ConvertProject

  def testGetProjectFilename(self):
    """Tests the _GetProjectFilename function."""
    solution = solutions.VSSolution()

    project_filename = solution._GetProjectFilename('2008', 'test')
    self.assertEqual(project_filename, 'test.vcproj')

    project_filename = solution._GetProjectFilename('2010', 'test')
    self.assertEqual(project_filename, 'test.vcxproj')

    project_filename = solution._GetProjectFilename('bogus', 'test')
    self.assertIsNone(project_filename)

  def testGetProjectFileReader(self):
    """Tests the _GetProjectFileReader function."""
    solution = solutions.VSSolution()

    project_file_reader = solution._GetProjectFileReader('2008')
    self.assertIsNotNone(project_file_reader)

    project_file_reader = solution._GetProjectFileReader('2010')
    self.assertIsNotNone(project_file_reader)

    project_file_reader = solution._GetProjectFileReader('2012')
    self.assertIsNotNone(project_file_reader)

    project_file_reader = solution._GetProjectFileReader('2013')
    self.assertIsNotNone(project_file_reader)

    project_file_reader = solution._GetProjectFileReader('2015')
    self.assertIsNotNone(project_file_reader)

    project_file_reader = solution._GetProjectFileReader('bogus')
    self.assertIsNone(project_file_reader)

  def testGetProjectFileWriter(self):
    """Tests the _GetProjectFileWriter function."""
    solution = solutions.VSSolution()

    project_file_writer = solution._GetProjectFileWriter('2008')
    self.assertIsNotNone(project_file_writer)

    project_file_writer = solution._GetProjectFileWriter('2010')
    self.assertIsNotNone(project_file_writer)

    project_file_writer = solution._GetProjectFileWriter('2012')
    self.assertIsNotNone(project_file_writer)

    project_file_writer = solution._GetProjectFileWriter('2013')
    self.assertIsNotNone(project_file_writer)

    project_file_writer = solution._GetProjectFileWriter('2015')
    self.assertIsNotNone(project_file_writer)

    project_file_writer = solution._GetProjectFileWriter('bogus')
    self.assertIsNone(project_file_writer)

  def testGetSolutionFileReader(self):
    """Tests the _GetSolutionFileReader function."""
    solution = solutions.VSSolution()

    solution_file_reader = solution._GetSolutionFileReader('2008')
    self.assertIsNotNone(solution_file_reader)

    solution_file_reader = solution._GetSolutionFileReader('2010')
    self.assertIsNotNone(solution_file_reader)

    solution_file_reader = solution._GetSolutionFileReader('2012')
    self.assertIsNotNone(solution_file_reader)

    solution_file_reader = solution._GetSolutionFileReader('2013')
    self.assertIsNotNone(solution_file_reader)

    solution_file_reader = solution._GetSolutionFileReader('2015')
    self.assertIsNotNone(solution_file_reader)

    solution_file_reader = solution._GetSolutionFileReader('bogus')
    self.assertIsNone(solution_file_reader)

  def testGetSolutionFileWriter(self):
    """Tests the _GetSolutionFileWriter function."""
    solution = solutions.VSSolution()

    solution_file_writer = solution._GetSolutionFileWriter('2008')
    self.assertIsNotNone(solution_file_writer)

    solution_file_writer = solution._GetSolutionFileWriter('2010')
    self.assertIsNotNone(solution_file_writer)

    solution_file_writer = solution._GetSolutionFileWriter('2012')
    self.assertIsNotNone(solution_file_writer)

    solution_file_writer = solution._GetSolutionFileWriter('2013')
    self.assertIsNotNone(solution_file_writer)

    solution_file_writer = solution._GetSolutionFileWriter('2015')
    self.assertIsNotNone(solution_file_writer)

    solution_file_writer = solution._GetSolutionFileWriter('bogus')
    self.assertIsNone(solution_file_writer)

  # TODO: add tests for _WriteProject
  # TODO: add tests for _WriteSolution
  # TODO: add tests for Convert


if __name__ == '__main__':
  unittest.main()
