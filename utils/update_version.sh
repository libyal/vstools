#!/bin/bash
# Script to update the version information.

DATE_VERSION=`date +"%Y%m%d"`;

sed -i -e "s/^\(__version__ = \)'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'$/\1'${DATE_VERSION}'/" vstools/__init__.py
