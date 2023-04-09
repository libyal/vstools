# -*- coding: utf-8 -*-
"""Tests for the project and solution file writer classes."""

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

    self.assertTrue(output_data.startswith(b'\t\t<Configuration\r\n'))
    self.assertTrue(output_data.endswith(b'\t\t</Configuration>\r\n'))

  def testWriteConfigurationLinkerTool(self):
    """Tests the _WriteConfigurationLinkerTool function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationLinkerTool(project_configuration)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t\t<Tool\r\n'
        b'\t\t\t\tName="VCLinkerTool"\r\n'
        b'\t\t\t\tAdditionalLibraryDirectories="&quot;$(OutDir)&quot;"\r\n'
        b'\t\t\t/>\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationOption(self):
    """Tests the _WriteConfigurationOption function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.compile_as = '1'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationOption(
        project_configuration, 'CompileAs', 'compile_as', False, 4)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\t\tCompileAs="1"\r\n'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationTool(self):
    """Tests the _WriteConfigurationTool function."""
    project_configuration = resources.VSProjectConfiguration()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationTool(
        project_configuration, 'VCCLCompilerTool',
        file_writer._TOOL_COMPILER_CONFIGURATION_OPTIONS)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t\t<Tool\r\n'
        b'\t\t\t\tName="VCCLCompilerTool"\r\n'
        b'\t\t\t\tAdditionalIncludeDirectories=""\r\n'
        b'\t\t\t\tPreprocessorDefinitions=""\r\n'
        b'\t\t\t\tRuntimeLibrary=""\r\n'
        b'\t\t\t\tWarningLevel=""\r\n'
        b'\t\t\t\tCompileAs=""\r\n'
        b'\t\t\t/>\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationToolFooter(self):
    """Tests the _WriteConfigurationToolFooter function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.compile_as = '1'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationToolFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'\t\t\t/>\r\n'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationToolHeader(self):
    """Tests the _WriteConfigurationToolHeader function."""
    project_configuration = resources.VSProjectConfiguration()
    project_configuration.compile_as = '1'

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationToolHeader('VCLinkerTool')

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\t\t\t<Tool\r\n'
        b'\t\t\t\tName="VCLinkerTool"\r\n')
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
        b'\t\t<Filter\r\n'
        b'\t\t\tName="Header Files"\r\n'
        b'\t\t\tFilter="h;hpp;hxx;hm;inl;inc;xsd"\r\n'
        b'\t\t\tUniqueIdentifier="{93995380-89BD-4b04-88EB-625FBE52EBFB}"\r\n'
        b'\t\t\t>\r\n'
        b'\t\t\t<File\r\n'
        b'\t\t\t\tRelativePath="test.h"\r\n'
        b'\t\t\t\t>\r\n'
        b'\t\t\t</File>\r\n'
        b'\t\t</Filter>\r\n')
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
        b'\t\t<Filter\r\n'
        b'\t\t\tName="Resource Files"\r\n'
        b'\t\t\tFilter="rc;ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe;'
        b'resx;tiff;tif;png;wav"\r\n'
        b'\t\t\tUniqueIdentifier="{67DA6AB6-F800-4c08-8B7A-83BB121AAD01}"\r\n'
        b'\t\t\t>\r\n'
        b'\t\t\t<File\r\n'
        b'\t\t\t\tRelativePath="test.rc"\r\n'
        b'\t\t\t\t>\r\n'
        b'\t\t\t</File>\r\n'
        b'\t\t</Filter>\r\n')
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
        b'\t\t<Filter\r\n'
        b'\t\t\tName="Source Files"\r\n'
        b'\t\t\tFilter="cpp;c;cc;cxx;def;odl;idl;hpj;bat;asm;asmx"\r\n'
        b'\t\t\tUniqueIdentifier="{4FC737F1-C7A5-4376-A066-2A32D752A2FF}"\r\n'
        b'\t\t\t>\r\n'
        b'\t\t\t<File\r\n'
        b'\t\t\t\tRelativePath="test.c"\r\n'
        b'\t\t\t\t>\r\n'
        b'\t\t\t</File>\r\n'
        b'\t\t</Filter>\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'<?xml version="1.0" encoding="Windows-1252"?>\r\n'
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurations(self):
    """Tests the WriteConfigurations function."""
    project_configurations = resources.VSConfigurations()

    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteConfigurations(project_configurations)

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    self.assertTrue(output_data.startswith(b'\t<Configurations>\r\n'))
    self.assertTrue(output_data.endswith(
        b'\t</Configurations>\r\n'
        b'\t<References>\r\n'
        b'\t</References>\r\n'))

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

    self.assertTrue(output_data.startswith(b'\t<Files>\r\n'))
    self.assertTrue(output_data.endswith(
        b'\t</Files>\r\n'
        b'\t<Globals>\r\n'
        b'\t</Globals>\r\n'))

  def testWriteFooter(self):
    """Tests the WriteFooter function."""
    file_writer = writers.VS2008ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'</VisualStudioProject>\r\n'
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
        b'<VisualStudioProject\r\n'
        b'\tProjectType="Visual C++"\r\n'
        b'\tVersion="9,00"\r\n'
        b'\tName=""\r\n'
        b'\tProjectGUID="{}"\r\n'
        b'\tRootNamespace=""\r\n'
        b'\tTargetFrameworkVersion="131072"\r\n'
        b'\t>\r\n'
        b'\t<Platforms>\r\n'
        b'\t\t<Platform\r\n'
        b'\t\t\tName="Win32"\r\n'
        b'\t\t/>\r\n'
        b'\t</Platforms>\r\n'
        b'\t<ToolFiles>\r\n'
        b'\t</ToolFiles>\r\n')
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
        b'    <ClCompile>\r\n'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>\r\n'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>\r\n'
        b'      <RuntimeLibrary></RuntimeLibrary>\r\n'
        b'      <WarningLevel></WarningLevel>\r\n'
        b'    </ClCompile>\r\n')
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
        b' Label="Configuration">\r\n'
        b'    <ConfigurationType></ConfigurationType>\r\n'
        b'  </PropertyGroup>\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurationPropertyGroupFooter(self):
    """Tests the _WriteConfigurationPropertyGroupFooter function."""
    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteConfigurationPropertyGroupFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'  </PropertyGroup>\r\n'
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
        b'Label="Configuration">\r\n')
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
        b'  <ItemGroup>\r\n'
        b'    <ClInclude Include="test.h" />\r\n'
        b'  </ItemGroup>\r\n')
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
        b' Condition="\'$(Configuration)|$(Platform)\'==\'|\'">\r\n'
        b'    <ClCompile>\r\n'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>\r\n'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>\r\n'
        b'      <RuntimeLibrary></RuntimeLibrary>\r\n'
        b'      <WarningLevel></WarningLevel>\r\n'
        b'    </ClCompile>\r\n'
        b'  </ItemDefinitionGroup>\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteItemDefinitionGroupFooter(self):
    """Tests the _WriteItemDefinitionGroupFooter function."""
    file_writer = writers.VS2010ProjectFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteItemDefinitionGroupFooter()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = b'  </ItemDefinitionGroup>\r\n'
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
        b' Condition="\'$(Configuration)|$(Platform)\'==\'|\'">\r\n')
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
        b'    <Lib>\r\n'
        b'      <OutputFile></OutputFile>\r\n'
        b'      <ModuleDefinitionFile>\r\n'
        b'      </ModuleDefinitionFile>\r\n'
        b'    </Lib>\r\n')
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
        b'    <Link>\r\n'
        b'    </Link>\r\n')
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
        b'  <PropertyGroup>\r\n'
        b'    <_ProjectFileVersion>10.0.40219.1</_ProjectFileVersion>\r\n'
        b'  </PropertyGroup>\r\n')
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
        b'  <ItemGroup>\r\n'
        b'    <ResourceCompile Include="test.rc" />\r\n'
        b'  </ItemGroup>\r\n')
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
        b'  <ItemGroup>\r\n'
        b'    <ClCompile Include="test.c" />\r\n'
        b'  </ItemGroup>\r\n')
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
        b'Microsoft.Cpp.Default.props" />\r\n'))
    self.assertTrue(output_data.endswith(b'  </PropertyGroup>\r\n'))

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

    self.assertTrue(output_data.startswith(b'  <ItemGroup>\r\n'))
    self.assertTrue(output_data.endswith(b'  </ItemGroup>\r\n'))

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
        b'\xef\xbb\xbf<?xml version="1.0" encoding="utf-8"?>\r\n'
        b'<Project DefaultTargets="Build" ToolsVersion="4.0" '
        b'xmlns="http://schemas.microsoft.com/developer/msbuild/2003">\r\n')
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
        b'  <ItemGroup Label="ProjectConfigurations">\r\n'
        b'  </ItemGroup>\r\n')
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
        b'  <PropertyGroup Label="Globals">\r\n'
        b'    <ProjectGuid>{}</ProjectGuid>\r\n'
        b'    <RootNamespace></RootNamespace>\r\n'
        b'  </PropertyGroup>\r\n')
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
        b'    <ClCompile>\r\n'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>\r\n'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>\r\n'
        b'      <RuntimeLibrary></RuntimeLibrary>\r\n'
        b'      <WarningLevel></WarningLevel>\r\n'
        b'    </ClCompile>\r\n')
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
        b' Label="Configuration">\r\n'
        b'    <ConfigurationType></ConfigurationType>\r\n'
        b'    <PlatformToolset>v110</PlatformToolset>\r\n'
        b'  </PropertyGroup>\r\n')
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
        b'Condition="\'$(Configuration)|$(Platform)\'==\'|\'">\r\n'
        b'    <ClCompile>\r\n'
        b'      <AdditionalIncludeDirectories>%(AdditionalIncludeDirectories)'
        b'</AdditionalIncludeDirectories>\r\n'
        b'      <PreprocessorDefinitions>%(PreprocessorDefinitions)'
        b'</PreprocessorDefinitions>\r\n'
        b'      <RuntimeLibrary></RuntimeLibrary>\r\n'
        b'      <WarningLevel></WarningLevel>\r\n'
        b'    </ClCompile>\r\n'
        b'  </ItemDefinitionGroup>\r\n')
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
        b'    <Lib>\r\n'
        b'      <OutputFile></OutputFile>\r\n'
        b'      <ModuleDefinitionFile />\r\n'
        b'    </Lib>\r\n')
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
        b'    <Link>\r\n'
        b'    </Link>\r\n')
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
        b'  <PropertyGroup>\r\n'
        b'    <_ProjectFileVersion>11.0.61030.0</_ProjectFileVersion>\r\n'
        b'  </PropertyGroup>\r\n')
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


class VS2017ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2017 project file writer test."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    file_writer = writers.VS2017ProjectFileWriter()
    self.assertIsNotNone(file_writer)


class VS2019ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2019 project file writer test."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    file_writer = writers.VS2019ProjectFileWriter()
    self.assertIsNotNone(file_writer)


class VS2022ProjectFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2022 project file writer test."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    file_writer = writers.VS2022ProjectFileWriter()
    self.assertIsNotNone(file_writer)


class VSSolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio solution file writer test."""

  # pylint: disable=protected-access

  # TODO: add tests for _WriteProjectConfigurationPlatforms.
  # TODO: add tests for _WriteSolutionConfigurationPlatforms.

  def testWriteSolutionProperties(self):
    """Tests the _WriteSolutionProperties function."""
    file_writer = writers.VSSolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteSolutionProperties()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\tGlobalSection(SolutionProperties) = preSolution\r\n'
        b'\t\tHideSolutionNode = FALSE\r\n'
        b'\tEndGlobalSection\r\n')
    self.assertEqual(output_data, expected_output_data)

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


class VS2017SolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2017 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteExtensibilityGlobals(self):
    """Tests the _WriteExtensibilityGlobals function."""
    file_writer = writers.VS2017SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer._WriteExtensibilityGlobals()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    expected_output_data = (
        b'\tGlobalSection(ExtensibilityGlobals) = postSolution\r\n'
        b'\t\tSolutionGuid = {E41FC29C-7FE6-4F98-85AD-1ED968E86446}\r\n'
        b'\tEndGlobalSection\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteConfigurations(self):
    """Tests the WriteConfigurations function."""
    solution_configurations = resources.VSConfigurations()
    solution_project = resources.VSSolutionProject('name', 'filename', 'guid')

    file_writer = writers.VS2017SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteConfigurations(solution_configurations, [solution_project])

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()

    # TODO: add ExtensibilityGlobals
    expected_output_data = (
        b'Global\r\n'
        b'\tGlobalSection(SolutionProperties) = preSolution\r\n'
        b'\t\tHideSolutionNode = FALSE\r\n'
        b'\tEndGlobalSection\r\n'
        b'EndGlobal\r\n')
    self.assertEqual(output_data, expected_output_data)

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2017SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 12.00\r\n'
        b'# Visual Studio 15\r\n'
        b'VisualStudioVersion = 15.0.26730.10\r\n'
        b'MinimumVisualStudioVersion = 10.0.40219.1\r\n')
    self.assertEqual(output_data, expected_output_data)


class VS2019SolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2019 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2019SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 12.00\r\n'
        b'# Visual Studio Version 16\r\n'
        b'VisualStudioVersion = 16.0.33423.256\r\n'
        b'MinimumVisualStudioVersion = 10.0.40219.1\r\n')
    self.assertEqual(output_data, expected_output_data)


class VS2022SolutionFileWriterTest(test_lib.BaseTestCase):
  """Visual Studio 2022 solution file writer test."""

  # pylint: disable=protected-access

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    file_writer = writers.VS2022SolutionFileWriter()

    file_writer._file = io.BytesIO()

    file_writer.WriteHeader()

    file_writer._file.seek(0, os.SEEK_SET)
    output_data = file_writer._file.read()
    expected_output_data = (
        b'\xef\xbb\xbf\r\n'
        b'Microsoft Visual Studio Solution File, Format Version 12.00\r\n'
        b'# Visual Studio Version 17\r\n'
        b'VisualStudioVersion = 17.5.33516.290\r\n'
        b'MinimumVisualStudioVersion = 10.0.40219.1\r\n')
    self.assertEqual(output_data, expected_output_data)


if __name__ == '__main__':
  unittest.main()
