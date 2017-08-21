# -*- coding: utf-8 -*-
"""Tests for the libyal sources classes."""

from __future__ import unicode_literals

import unittest

from vstools import libyal

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

  # TODO: add tests for _ConfigureAsBzip2Dll
  # TODO: add tests for _ConfigureAsDll
  # TODO: add tests for _ConfigureAsDokanDll
  # TODO: add tests for _ConfigureAsExe
  # TODO: add tests for _ConfigureAsLibrary
  # TODO: add tests for _ConfigureAsZlibDll
  # TODO: add tests for _ConfigureLibcrypto
  # TODO: add tests for _ConfigureLibuuid
  # TODO: add tests for _CreateThirdPartyDepencies
  # TODO: add tests for _ReadMakefile
  # TODO: add tests for _ReadMakefilePrograms
  # TODO: add tests for Convert


if __name__ == '__main__':
  unittest.main()
