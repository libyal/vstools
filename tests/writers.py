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

  def testWriteConfiguration(self):
    """Tests the _WriteConfiguration function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfiguration(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.startswith(b'\t\t<Configuration'))
    self.assertTrue(output_data.endswith(b'\t\t</Configuration>'))

  def testWriteConfigurationAdditionalIncludeDirectories(self):
    """Tests the _WriteConfigurationAdditionalIncludeDirectories function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationAdditionalIncludeDirectories(
        project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\t\tAdditionalIncludeDirectories=""'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationBasicRuntimeChecks(self):
    """Tests the _WriteConfigurationBasicRuntimeChecks function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.basic_runtime_checks = '3'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationBasicRuntimeChecks(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\t\tBasicRuntimeChecks="3"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationCharacterSet(self):
    """Tests the _WriteConfigurationCharacterSet function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.character_set = '1'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationCharacterSet(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\tCharacterSet="1"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationManagedExtensions(self):
    """Tests the _WriteConfigurationManagedExtensions function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.managed_extensions = '.test'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationManagedExtensions(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\tManagedExtensions=".test"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationOptimization(self):
    """Tests the _WriteConfigurationOptimization function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.optimization = '0'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationOptimization(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\t\tOptimization="0"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationPreprocessorDefinitions(self):
    """Tests the _WriteConfigurationPreprocessorDefinitions function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.preprocessor_definitions = '_CRT_SECURE_NO_DEPRECATE'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationPreprocessorDefinitions(
        project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t\t\tPreprocessorDefinitions="_CRT_SECURE_NO_DEPRECATE"')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationSmallerTypeCheck(self):
    """Tests the _WriteConfigurationSmallerTypeCheck function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.smaller_type_check = 'true'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationSmallerTypeCheck(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\t\tSmallerTypeCheck="true"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationType(self):
    """Tests the _WriteConfigurationType function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.output_type = '2'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationType(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\tConfigurationType="2"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationWholeProgramOptimization(self):
    """Tests the _WriteConfigurationWholeProgramOptimization function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.whole_program_optimization = '0'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationWholeProgramOptimization(
        project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\tWholeProgramOptimization="0"'
    self.assertEqual(output_data, expected_output_data)

  def testWriteHeaderFiles(self):
    """Tests the _WriteHeaderFiles function."""
    header_files = ['test.h']

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteHeaderFiles(header_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t<Filter'
        b'\t\t\tName="Header Files"'
        b'\t\t\tFilter="h;hpp;hxx;hm;inl;inc;xsd"'
        b'\t\t\tUniqueIdentifier="{93995380-89BD-4b04-88EB-625FBE52EBFB}"'
        b'\t\t\t>'
        b'\t\t\t<File'
        b'\t\t\t\tRelativePath="test.h"'
        b'\t\t\t\t>'
        b'\t\t\t</File>'
        b'\t\t</Filter>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteResourceFiles(self):
    """Tests the _WriteResourceFiles function."""
    resource_files = ['test.rc']

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteResourceFiles(resource_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t<Filter'
        b'\t\t\tName="Resource Files"'
        b'\t\t\tFilter="rc;ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe;'
        b'resx;tiff;tif;png;wav"'
        b'\t\t\tUniqueIdentifier="{67DA6AB6-F800-4c08-8B7A-83BB121AAD01}"'
        b'\t\t\t>'
        b'\t\t\t<File'
        b'\t\t\t\tRelativePath="test.rc"'
        b'\t\t\t\t>'
        b'\t\t\t</File>'
        b'\t\t</Filter>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteSourceFiles(self):
    """Tests the _WriteSourceFiles function."""
    source_files = ['test.c']

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteSourceFiles(source_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t<Filter'
        b'\t\t\tName="Source Files"'
        b'\t\t\tFilter="cpp;c;cc;cxx;def;odl;idl;hpj;bat;asm;asmx"'
        b'\t\t\tUniqueIdentifier="{4FC737F1-C7A5-4376-A066-2A32D752A2FF}"'
        b'\t\t\t>'
        b'\t\t\t<File'
        b'\t\t\t\tRelativePath="test.c"'
        b'\t\t\t\t>'
        b'\t\t\t</File>'
        b'\t\t</Filter>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'<?xml version="1.0" encoding="Windows-1252"?>'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurations(self):
    """Tests the WriteConfigurations function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteConfigurations(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.startswith(b'\t<Configurations>'))
    self.assertTrue(output_data.endswith(
        b'\t</Configurations>'
        b'\t<References>'
        b'\t</References>'))

  def testWriteDependencies(self):
    """Tests the WriteDependencies function."""
    dependencies = []
    solution_projects_by_guid = {}

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteDependencies(dependencies, solution_projects_by_guid)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')

  def testWriteFiles(self):
    """Tests the WriteFiles function."""
    header_files = ['test.h']
    resource_files = ['test.rc']
    source_files = ['test.c']

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteFiles(source_files, header_files, resource_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.startswith(b'\t<Files>'))
    self.assertTrue(output_data.endswith(
        b'\t</Files>'
        b'\t<Globals>'
        b'\t</Globals>'))

  def testWriteFooter(self):
    """Tests the WriteFooter function."""
    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'</VisualStudioProject>'
    self.assertEqual(output_data, expected_output_data)

  def testWriteProjectConfigurations(self):
    """Tests the WriteProjectConfigurations function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteProjectConfigurations(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')

  def testWriteProjectInformation(self):
    """Tests the WriteProjectInformation function."""
    project_information = resources.VSProjectInformation()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteProjectInformation(project_information)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'<VisualStudioProject'
        b'\tProjectType="Visual C++"'
        b'\tVersion="9,00"'
        b'\tName=""'
        b'\tProjectGUID="{}"'
        b'\tRootNamespace=""'
        b'\tTargetFrameworkVersion="131072"'
        b'\t>'
        b'\t<Platforms>'
        b'\t\t<Platform'
        b'\t\t\tName="Win32"'
        b'\t\t/>'
        b'\t</Platforms>'
        b'\t<ToolFiles>'
        b'\t</ToolFiles>')
    self.assertEqual(output_data, expected_output_data)


class VS2010ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2010 project file writer test."""

  # pylint: disable=protected-access

  def testWriteClCompileSection(self):
    """Tests the _WriteClCompileSection function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteClCompileSection(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'    <ClCompile>'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>'
        b'      <RuntimeLibrary></RuntimeLibrary>'
        b'      <WarningLevel></WarningLevel>'
        b'    </ClCompile>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationPropertyGroup(self):
    """Tests the _WriteConfigurationPropertyGroup function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationPropertyGroup(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'==\'|\'"'
        b' Label="Configuration">'
        b'    <ConfigurationType></ConfigurationType>'
        b'  </PropertyGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationPropertyGroupFooter(self):
    """Tests the _WriteConfigurationPropertyGroupFooter function."""
    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationPropertyGroupFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'  </PropertyGroup>'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationPropertyGroupHeader(self):
    """Tests the _WriteConfigurationPropertyGroupHeader function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationPropertyGroupHeader(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'==\'|\'" '
        b'Label="Configuration">')
    self.assertEqual(output_data, expected_output_data)

  def testWriteHeaderFiles(self):
    """Tests the _WriteHeaderFiles function."""
    header_files = ['test.h']

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteHeaderFiles(header_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemGroup>'
        b'    <ClInclude Include="test.h" />'
        b'  </ItemGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteItemDefinitionGroup(self):
    """Tests the _WriteItemDefinitionGroup function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteItemDefinitionGroup(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemDefinitionGroup'
        b' Condition="\'$(Configuration)|$(Platform)\'==\'|\'">'
        b'    <ClCompile>'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>'
        b'      <RuntimeLibrary></RuntimeLibrary>'
        b'      <WarningLevel></WarningLevel>'
        b'    </ClCompile>'
        b'  </ItemDefinitionGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteItemDefinitionGroupFooter(self):
    """Tests the _WriteItemDefinitionGroupFooter function."""
    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteItemDefinitionGroupFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'  </ItemDefinitionGroup>'
    self.assertEqual(output_data, expected_output_data)

  def testWriteItemDefinitionGroupHeader(self):
    """Tests the _WriteItemDefinitionGroupHeader function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteItemDefinitionGroupHeader(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemDefinitionGroup'
        b' Condition="\'$(Configuration)|$(Platform)\'==\'|\'">')
    self.assertEqual(output_data, expected_output_data)

  def testWriteLibrarianSection(self):
    """Tests the _WriteLibrarianSection function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteLibrarianSection(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'    <Lib>'
        b'      <OutputFile></OutputFile>'
        b'      <ModuleDefinitionFile>'
        b'      </ModuleDefinitionFile>'
        b'    </Lib>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteLinkerSection(self):
    """Tests the _WriteLinkerSection function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteLinkerSection(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'    <Link>'
        b'    </Link>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteOutIntDirConditions(self):
    """Tests the _WriteOutIntDirConditions function."""
    configuration_name = 'Release'
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteOutIntDirConditions(
        configuration_name, project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')

  def testWriteOutIntDirPropertyGroups(self):
    """Tests the _WriteOutIntDirPropertyGroups function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteOutIntDirPropertyGroups(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <PropertyGroup>'
        b'    <_ProjectFileVersion>10.0.40219.1</_ProjectFileVersion>'
        b'  </PropertyGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteResourceFiles(self):
    """Tests the _WriteResourceFiles function."""
    resource_files = ['test.rc']

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteResourceFiles(resource_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemGroup>'
        b'    <ResourceCompile Include="test.rc" />'
        b'  </ItemGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteSourceFiles(self):
    """Tests the _WriteSourceFiles function."""
    source_files = ['test.c']

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteSourceFiles(source_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemGroup>'
        b'    <ClCompile Include="test.c" />'
        b'  </ItemGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurations(self):
    """Tests the WriteConfigurations function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteConfigurations(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.startswith(
        b'  <Import Project="$(VCTargetsPath)\\'
        b'Microsoft.Cpp.Default.props" />'))
    self.assertTrue(output_data.endswith(b'  </PropertyGroup>'))

  def testWriteDependencies(self):
    """Tests the WriteDependencies function."""
    dependencies = []
    solution_projects_by_guid = {}

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteDependencies(dependencies, solution_projects_by_guid)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')

  def testWriteFiles(self):
    """Tests the WriteFiles function."""
    header_files = ['test.h']
    resource_files = ['test.rc']
    source_files = ['test.c']

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteFiles(source_files, header_files, resource_files)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.startswith(b'  <ItemGroup>'))
    self.assertTrue(output_data.endswith(b'  </ItemGroup>'))

  def testWriteFooter(self):
    """Tests the WriteFooter function."""
    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.endswith(b'</Project>'))

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\xef\xbb\xbf<?xml version="1.0" encoding="utf-8"?>'
        b'<Project DefaultTargets="Build" ToolsVersion="4.0" '
        b'xmlns="http://schemas.microsoft.com/developer/msbuild/2003">')
    self.assertEqual(output_data, expected_output_data)

  def testWriteProjectConfigurations(self):
    """Tests the WriteProjectConfigurations function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteProjectConfigurations(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemGroup Label="ProjectConfigurations">'
        b'  </ItemGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteProjectInformation(self):
    """Tests the WriteProjectInformation function."""
    project_information = resources.VSProjectInformation()

    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteProjectInformation(project_information)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <PropertyGroup Label="Globals">'
        b'    <ProjectGuid>{}</ProjectGuid>'
        b'    <RootNamespace></RootNamespace>'
        b'  </PropertyGroup>')
    self.assertEqual(output_data, expected_output_data)


class VS2012ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2012 project file writer test."""

  # pylint: disable=protected-access

  def testWriteClCompileSection(self):
    """Tests the _WriteClCompileSection function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteClCompileSection(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'    <ClCompile>'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>'
        b'      <RuntimeLibrary></RuntimeLibrary>'
        b'      <WarningLevel></WarningLevel>'
        b'    </ClCompile>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationPropertyGroup(self):
    """Tests the _WriteConfigurationPropertyGroup function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationPropertyGroup(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'==\'|\'"'
        b' Label="Configuration">'
        b'    <ConfigurationType></ConfigurationType>'
        b'    <PlatformToolset>v110</PlatformToolset>'
        b'  </PropertyGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteItemDefinitionGroup(self):
    """Tests the _WriteItemDefinitionGroup function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteItemDefinitionGroup(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <ItemDefinitionGroup '
        b'Condition="\'$(Configuration)|$(Platform)\'==\'|\'">'
        b'    <ClCompile>'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>'
        b'      <RuntimeLibrary></RuntimeLibrary>'
        b'      <WarningLevel></WarningLevel>'
        b'    </ClCompile>'
        b'  </ItemDefinitionGroup>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteLibrarianSection(self):
    """Tests the _WriteLibrarianSection function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteLibrarianSection(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'    <Lib>'
        b'      <OutputFile></OutputFile>'
        b'      <ModuleDefinitionFile />'
        b'    </Lib>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteLinkerSection(self):
    """Tests the _WriteLinkerSection function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteLinkerSection(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'    <Link>'
        b'    </Link>')
    self.assertEqual(output_data, expected_output_data)

  def testWriteOutIntDirConditions(self):
    """Tests the _WriteOutIntDirConditions function."""
    configuration_name = 'Release'
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteOutIntDirConditions(
        configuration_name, project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')

  def testWriteOutIntDirPropertyGroups(self):
    """Tests the _WriteOutIntDirPropertyGroups function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2012ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteOutIntDirPropertyGroups(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'  <PropertyGroup>'
        b'    <_ProjectFileVersion>11.0.61030.0</_ProjectFileVersion>'
        b'  </PropertyGroup>')
    self.assertEqual(output_data, expected_output_data)


class VS2013ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2013 project file writer test."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    file_writer = writers.VS2013ProjectFileWriter()
    self.assertIsNotNone(file_writer)


class VS2015ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2015 project file writer test."""

  # pylint: disable=protected-access

  def testWriteOutIntDirConditions(self):
    """Tests the _WriteOutIntDirConditions function."""
    configuration_name = 'Release'
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2015ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteOutIntDirConditions(
        configuration_name, project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')


class VSSolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio solution file writer test."""

  # pylint: disable=protected-access

  def testWriteProjects(self):
    """Tests the WriteProjects function."""
    solution_project = resources.VSSolutionProject('name', 'file', 'guid')

    file_writer = writers.VSSolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteProjects([solution_project])

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertEqual(output_data, b'')


class VS2008SolutionFileWriter(test_lib.BaseTestCase):
  """Visual Studio 2008 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteConfigurations(self):
    """Tests the WriteConfigurations function."""
    solution_configurations = resources.VSConfigurations()
    solution_project = resources.VSSolutionProject('name', 'filename', 'guid')

    file_writer = writers.VS2008SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteConfigurations(solution_configurations, [solution_project])

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'Global\r\n'
        b'\tGlobalSection(SolutionProperties) = preSolution\r\n'
        b'\t\tHideSolutionNode = FALSE\r\n'
        b'\tEndGlobalSection\r\n'
        b'EndGlobal\r\n')
    self.assertEqual(output_data, expected_output_data)


class VS2010SolutionFileWriter(test_lib.BaseTestCase):
  """Visual Studio 2010 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteConfigurations(self):
    """Tests the WriteConfigurations function."""
    solution_configurations = resources.VSConfigurations()
    solution_project = resources.VSSolutionProject('name', 'filename', 'guid')

    file_writer = writers.VS2010SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteConfigurations(solution_configurations, [solution_project])

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'Global\r\n'
        b'\tGlobalSection(SolutionProperties) = preSolution\r\n'
        b'\t\tHideSolutionNode = FALSE\r\n'
        b'\tEndGlobalSection\r\n'
        b'EndGlobal\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2010SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 11.00\r\n'
        b'# Visual C++ Express 2010\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteProject(self):
    """Tests the WriteProject function."""
    solution_project = resources.VSSolutionProject('name', 'filename', 'guid')

    file_writer = writers.VS2010SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteProject(solution_project)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "name",'
        b' "filename.vcxproj", "{GUID}"\r\n'
        b'EndProject\r\n')
    self.assertEqual(output_data, expected_output_data)


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
    solution_project = resources.VSSolutionProject('name', 'filename', 'guid')

    file_writer = writers.VS2012SolutionFileWriter()

    file_writer._file = io.BytesIO()

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
