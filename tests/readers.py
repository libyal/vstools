# -*- coding: utf-8 -*-
"""Tests for the project and solution file reader classes."""

import unittest

from vstools import readers

from tests import test_lib


class FileReaderTest(test_lib.BaseTestCase):
  """File reader tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    file_reader = readers.FileReader()
    self.assertIsNotNone(file_reader)

  # TODO: add tests for _ReadLine function.
  # TODO: add tests for Close function.
  # TODO: add tests for Open function.


# TODO: add tests for VSProjectFileReader
# TODO: add tests for VS2008ProjectFileReader
# TODO: add tests for VS2010ProjectFileReader
# TODO: add tests for VS2012ProjectFileReader
# TODO: add tests for VS2013ProjectFileReader
# TODO: add tests for VS2015ProjectFileReader
# TODO: add tests for VSSolutionFileReader
# TODO: add tests for VS2008SolutionFileReader
# TODO: add tests for VS2010SolutionFileReader
# TODO: add tests for VS2012SolutionFileReader
# TODO: add tests for VS2013SolutionFileReader
# TODO: add tests for VS2015SolutionFileReader


if __name__ == '__main__':
  unittest.main()
