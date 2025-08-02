#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本生成器
根据 .github/versions.list 文件生成不同版本的文档
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

class VersionGenerator:
    def __init__(self, source_dir: str = "source", versions_file: str = ".github/versions.list"):
        self.source_dir = Path(source_dir)
        self.versions_file = Path(versions_file)
        self.versions = []
        
    def load_versions(self) -> List[str]:
        """从 versions.list 文件加载版本列表"""
        if not self.versions_file.exists():
            print(f"警告: 版本文件不存在: {self.versions_file}")
            return []
            
        versions = []
        with open(self.versions_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # 提取版本名称（去掉注释）
                    version = line.split('#')[0].strip()
                    if version:
                        versions.append(version)
        
        print(f"加载版本配置: {versions}")
        return versions
    
    def build_version_docs(self, version: str) -> bool:
        """为指定版本构建文档"""
        print(f"\n开始构建版本 {version} 的文档...")
        
        # 创建版本输出目录
        if version == 'master':
            output_dir = self.source_dir / '_build' / 'html' / 'latest'
        else:
            output_dir = self.source_dir / '_build' / 'html' / version
        
        # 清理输出目录
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 运行文档生成脚本
            subprocess.run([
                sys.executable, 'doc_generator.py'
            ], cwd=self.source_dir, check=True)
            
            # 构建HTML文档
            subprocess.run([
                sys.executable, '-m', 'sphinx.cmd.build',
                '-b', 'html',
                '.',
                str(output_dir)
            ], cwd=self.source_dir, check=True)
            
            print(f"✓ 版本 {version} 文档构建完成: {output_dir}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ 版本 {version} 文档构建失败: {e}")
            return False
    
    def generate_all_versions(self) -> Dict[str, bool]:
        """生成所有版本的文档"""
        print("开始生成所有版本的文档...")
        
        # 加载版本列表
        self.versions = self.load_versions()
        if not self.versions:
            print("错误: 没有找到有效的版本配置")
            return {}
        
        results = {}
        
        # 为每个版本构建文档
        for version in self.versions:
            success = self.build_version_docs(version)
            results[version] = success
        
        return results
    
    def create_version_index(self) -> bool:
        """创建版本索引页面"""
        print("\n创建版本索引页面...")
        
        index_html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EtherKit SDK 文档 - 版本选择</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .version-list {
            display: grid;
            gap: 20px;
            margin-top: 30px;
        }
        .version-card {
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s ease;
        }
        .version-card:hover {
            border-color: #0969da;
            box-shadow: 0 4px 12px rgba(9, 105, 218, 0.15);
            transform: translateY(-2px);
        }
        .version-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #0969da;
        }
        .version-desc {
            color: #666;
            margin: 0;
        }
        .latest-badge {
            background: #28a745;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            margin-left: 8px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>EtherKit SDK 文档</h1>
        <p>选择您需要的文档版本</p>
    </div>
    
    <div class="version-list">
"""
        
        # 添加版本链接
        for version in self.versions:
            if version == 'master':
                display_name = '最新版本'
                description = '最新的开发版本，包含最新的功能和改进'
                badge = '<span class="latest-badge">最新</span>'
                link = '/latest/'
            else:
                display_name = version
                description = f'{version} 稳定版本'
                badge = ''
                link = f'/{version}/'
            
            index_html += f"""
        <a href="{link}" class="version-card">
            <div class="version-title">
                {display_name} {badge}
            </div>
            <p class="version-desc">{description}</p>
        </a>
"""
        
        index_html += """
    </div>
</body>
</html>
"""
        
        # 写入索引文件
        index_file = self.source_dir / '_build' / 'html' / 'index.html'
        index_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"✓ 版本索引页面创建完成: {index_file}")
        return True

def main():
    """主函数"""
    generator = VersionGenerator()
    
    # 生成所有版本的文档
    results = generator.generate_all_versions()
    
    # 创建版本索引页面
    generator.create_version_index()
    
    # 输出结果
    print("\n" + "="*50)
    print("版本生成结果:")
    for version, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"  {version}: {status}")
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"\n总计: {success_count}/{total_count} 个版本生成成功")
    
    if success_count == total_count:
        print("🎉 所有版本生成完成！")
        return 0
    else:
        print("⚠️  部分版本生成失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 