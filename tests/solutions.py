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
  # TODO: add tests for _WriteProject
  # TODO: add tests for _WriteSolution
  # TODO: add tests for Convert


if __name__ == '__main__':
  unittest.main()
