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

def load_versions():
    """从 versions.list 文件加载版本列表"""
    versions_file = Path("../.github/versions.list")
    if not versions_file.exists():
        print(f"错误: 版本文件不存在: {versions_file}")
        return []
        
    versions = []
    with open(versions_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                version = line.split('#')[0].strip()
                if version:
                    versions.append(version)
    
    print(f"加载版本配置: {versions}")
    return versions

def build_version_docs(version):
    """为指定版本构建文档"""
    print(f"\n开始构建版本 {version} 的文档...")
    
    # 创建版本输出目录
    if version == 'master':
        output_dir = Path("_build/html/latest")
    else:
        output_dir = Path(f"_build/html/{version}")
    
    # 清理输出目录
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 运行文档生成脚本
        subprocess.run([
            sys.executable, 'doc_generator.py'
        ], cwd=".", check=True)
        
        # 构建HTML文档
        subprocess.run([
            sys.executable, '-m', 'sphinx.cmd.build',
            '-b', 'html',
            '.',
            str(output_dir)
        ], cwd=".", check=True)
        
        print(f"✓ 版本 {version} 文档构建完成: {output_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 版本 {version} 文档构建失败: {e}")
        return False

def create_root_redirect():
    """创建根目录重定向页面"""
    print("\n创建根目录重定向页面...")
    
    # 创建根目录的 index.html，重定向到 latest
    root_index = Path("_build/html/index.html")
    root_index.parent.mkdir(parents=True, exist_ok=True)
    
    redirect_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EtherKit SDK 文档</title>
    <meta http-equiv="refresh" content="0; url=./latest/">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        h1 {
            margin: 0 0 10px 0;
            font-size: 24px;
        }
        p {
            margin: 0;
            opacity: 0.9;
        }
        a {
            color: white;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>EtherKit SDK 文档</h1>
        <p>正在跳转到最新版本...</p>
        <p><a href="./latest/">如果页面没有自动跳转，请点击这里</a></p>
    </div>
</body>
</html>"""
    
    with open(root_index, 'w', encoding='utf-8') as f:
        f.write(redirect_html)
    
    print(f"✓ 根目录重定向页面创建完成: {root_index}")
    return True

def main():
    """主函数"""
    print("开始生成多版本文档...")
    
    # 加载版本列表
    versions = load_versions()
    if not versions:
        print("错误: 没有找到有效的版本配置")
        return 1
    
    # 为每个版本构建文档
    results = {}
    for version in versions:
        success = build_version_docs(version)
        results[version] = success
    
    # 创建根目录重定向页面
    create_root_redirect()
    
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
