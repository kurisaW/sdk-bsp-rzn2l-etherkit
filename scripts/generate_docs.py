#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成 EtherKit SDK 文档脚本
扫描 project 目录下的所有项目，完整拷贝每个项目目录到 source 下。
"""

import os
import shutil
from pathlib import Path
from typing import List

class DocGenerator:
    def __init__(self):
        self.project_dir = Path("projects")
        self.output_dir = Path("source")
        # 使用英文目录名，但保持中文显示
        self.categories = {
            "basic": "基础篇",
            "driver": "驱动篇", 
            "component": "组件篇",
            "protocol": "工业协议篇"
        }
        self.category_mapping = {
            "basic": [],
            "driver": [],
            "component": [],
            "protocol": []
        }

    def scan_projects(self):
        """扫描项目目录并分类"""
        print("开始扫描项目...")
        if not self.project_dir.exists():
            print(f"项目目录不存在: {self.project_dir}")
            return

        for project_dir in self.project_dir.iterdir():
            if project_dir.is_dir():
                project_name = project_dir.name
                if project_name.startswith("etherkit_basic_") or project_name == "etherkit_blink_led":
                    self.category_mapping["basic"].append(project_name)
                elif project_name.startswith("etherkit_driver_") or project_name.startswith("etherkit_usb_"):
                    self.category_mapping["driver"].append(project_name)
                elif project_name.startswith("etherkit_component_"):
                    self.category_mapping["component"].append(project_name)
                elif project_name.startswith("etherkit_ethercat_") or project_name.startswith("etherkit_modbus_") or project_name.startswith("etherkit_profinet_") or project_name.startswith("etherkit_ethernetip_") or project_name == "etherkit_ethernet":
                    self.category_mapping["protocol"].append(project_name)
                elif project_name == "etherkit_factory":
                    self.category_mapping["basic"].append(project_name)

    def copy_project_directory(self, project_name: str, category: str):
        """拷贝项目的特定文件"""
        source_project = self.project_dir / project_name
        dest_project = self.output_dir / f"{category}" / project_name
        if source_project.exists():
            if dest_project.exists():
                shutil.rmtree(dest_project)
            dest_project.mkdir(parents=True, exist_ok=True)
            files_to_copy = ["README.md", "README_zh.md"]
            for file_name in files_to_copy:
                source_file = source_project / file_name
                if source_file.exists():
                    shutil.copy2(source_file, dest_project)
                    print(f"拷贝文件: {project_name}/{file_name}")
            figures_dir = source_project / "figures"
            if figures_dir.exists() and figures_dir.is_dir():
                dest_figures = dest_project / "figures"
                shutil.copytree(figures_dir, dest_figures)
                print(f"拷贝目录: {project_name}/figures")
            print(f"处理项目: {project_name} -> {dest_project}")

    def get_readme_title(self, project_name: str, category: str) -> str:
        """从README_zh.md文件中提取一级标题"""
        readme_path = self.output_dir / category / project_name / "README_zh.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 查找第一个一级标题
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('# ') and len(line) > 2:
                            return line[2:].strip()  # 移除 "# " 前缀
            except Exception as e:
                print(f"读取 {project_name}/README_zh.md 标题时出错: {e}")
        
        # 如果无法读取标题，使用项目名称作为后备
        return project_name.replace("etherkit_", "").replace("_", " ").title()

    def generate_category_index(self, category: str, category_name: str, projects: List[str]) -> str:
        """生成分类索引页面"""
        title_length = len(category_name.encode('utf-8'))
        underline = '=' * title_length
        content = f"""{category_name}
{underline}

这里包含了 EtherKit SDK 的 {category_name}。

.. toctree::
   :maxdepth: 2
   :caption: {category_name}

"""
        for project in projects:
            title = self.get_readme_title(project, category)
            content += f"   {project}/README_zh <{title}>\n"
        content += f"\n这些示例展示了 EtherKit SDK 的 {category_name}。\n"
        return content

    def generate_main_index(self):
        """生成主索引页面"""
        main_title = "欢迎来到 EtherKit_SDK_Docs 文档！"
        title_length = len(main_title.encode('utf-8'))
        main_underline = '=' * title_length

        content = f""".. EtherKit_SDK_Docs documentation master file, created by sphinx-quickstart

{main_title}
{main_underline}

.. toctree::
   :maxdepth: 2
   :caption: 目录

   basic/index
   driver/index
   component/index
   protocol/index

项目简介
--------
这里是 EtherKit_SDK_Docs 的简要介绍。

EtherKit SDK 提供了丰富的示例项目，包括基础功能、驱动示例和组件示例。
"""
        index_path = self.output_dir / "index.rst"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def run(self):
        """运行文档生成"""
        # 保存Sphinx必需的文件
        sphinx_files = {}
        if self.output_dir.exists():
            for file_name in ['conf.py', 'requirements.txt']:
                file_path = self.output_dir / file_name
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sphinx_files[file_name] = f.read()
            
            # 保存静态文件目录
            static_dir = self.output_dir / '_static'
            templates_dir = self.output_dir / '_templates'
            
            # 清理输出目录
            shutil.rmtree(self.output_dir)
        
        # 重新创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        
        # 恢复Sphinx必需的文件
        for file_name, content in sphinx_files.items():
            file_path = self.output_dir / file_name
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 重新创建静态文件目录
        if static_dir.exists():
            shutil.copytree(static_dir, self.output_dir / '_static')
        else:
            (self.output_dir / '_static').mkdir(exist_ok=True)
            
        if templates_dir.exists():
            shutil.copytree(templates_dir, self.output_dir / '_templates')
        else:
            (self.output_dir / '_templates').mkdir(exist_ok=True)

        # 扫描项目
        self.scan_projects()

        # 处理每个分类
        for category, category_name in self.categories.items():
            projects = self.category_mapping[category]
            if projects:
                print(f"\n处理 {category_name} 分类...")
                for project in projects:
                    self.copy_project_directory(project, category)
                
                # 生成分类索引
                index_content = self.generate_category_index(category, category_name, projects)
                index_path = self.output_dir / category / "index.rst"
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(index_content)
                print(f"已生成: {index_path}")

        # 生成主索引
        print("\n生成主索引...")
        self.generate_main_index()
        print("\n文档生成完成!")

if __name__ == "__main__":
    generator = DocGenerator()
    generator.run() 