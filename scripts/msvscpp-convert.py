#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to generate different versions of Visual Studio (express) files.

Currently supported input formats:
* libyal source directory (configure.ac and Makefile.am)
* 2008 (9.0)

Currently supported output formats:
* 2008 (9.0)
* 2010 (10.0)
* 2012 (11.0)
* 2013 (12.0)
* 2015 (14.0)
"""

# TODO: add automated tests.
# TODO: add vs2010 reader.
# TODO: add vs2012 reader.
# TODO: add vs2013 reader.
# TODO: add vs2015 reader.
# TODO: add vs2017 reader.
# TODO: add vs2017 writer.

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import os
import sys

from vstools import libyal
from vstools import solutions


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  output_formats = frozenset(['2008', '2010', '2012', '2013', '2015'])

  argument_parser = argparse.ArgumentParser(description=(
      'Converts source directory (autoconf and automake files) into '
      'Visual Studio express solution and project files. It is also '
      'possible to convert from one version of Visual Studio to another.'))

  argument_parser.add_argument(
      'solution_file', nargs='?', action='store', metavar='FILENAME',
      default=None, help=(
          'location of the source directory or the Visual Studio solution '
          'file (.sln).'))

  argument_parser.add_argument(
      '--no_python_dll', '--no-python-dll', dest='generate_python_dll',
      action='store_false', default=True, help=(
          'do not generate a project file to build the Python module DLL if '
          'present.'))

  argument_parser.add_argument(
      '--output_format', '--output-format', '--to', dest='output_format',
      nargs='?', choices=sorted(output_formats), action='store',
      metavar='FORMAT', default='2010', help='output format.')

  argument_parser.add_argument(
      '--python_path', '--python-path', dest='python_path',
      nargs='?', action='store', metavar='PATH', default='C:\\Python27',
      help='location of the Python installation.')

  options = argument_parser.parse_args()

  if not options.solution_file:
    print('Solution file missing.')
    print('')
    argument_parser.print_help()
    print('')
    return False

  if options.output_format not in output_formats:
    print('Unsupported output format: {0:s}.'.format(options.format_to))
    print('')
    return False

  logging.basicConfig(
      level=logging.INFO, format='[%(levelname)s] %(message)s')

  if os.path.isdir(options.solution_file):
    input_solution = libyal.LibyalSourceVSSolution(
        generate_python_dll=options.generate_python_dll,
        python_path=options.python_path)
  else:
    input_solution = solutions.VSSolution(
        generate_python_dll=options.generate_python_dll,
        python_path=options.python_path)

  if not input_solution.Convert(options.solution_file, options.output_format):
    print('Unable to convert Visual Studio solution file.')
    return False

  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
