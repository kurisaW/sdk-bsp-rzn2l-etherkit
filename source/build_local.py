#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地文档构建脚本
用于快速构建和预览文档
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import sphinx
        import yaml
        import myst_parser
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def build_docs(clean=False, serve=False, port=8000):
    """构建文档"""
    print("开始构建文档...")
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    try:
        # 1. 生成文档结构
        print("1. 生成文档结构...")
        subprocess.run([
            sys.executable, 'doc_generator.py'
        ], cwd=".", check=True)
        
        # 2. 构建HTML文档
        print("2. 构建HTML文档...")
        build_dir = Path("_build/html")
        if clean and build_dir.exists():
            import shutil
            shutil.rmtree(build_dir)
            print("已清理构建目录")
        
        subprocess.run([
            sys.executable, '-m', 'sphinx.cmd.build',
            '-b', 'html',
            '.',
            str(build_dir)
        ], cwd=".", check=True)
        
        print(f"✓ 文档构建完成: {build_dir.absolute()}")
        
        # 3. 启动本地服务器（如果需要）
        if serve:
            print(f"3. 启动本地服务器 (http://localhost:{port})...")
            try:
                subprocess.run([
                    sys.executable, '-m', 'http.server', str(port)
                ], cwd=str(build_dir))
            except KeyboardInterrupt:
                print("\n服务器已停止")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="本地文档构建工具")
    parser.add_argument('--clean', action='store_true', help='清理构建目录')
    parser.add_argument('--serve', action='store_true', help='启动本地服务器')
    parser.add_argument('--port', type=int, default=8000, help='服务器端口 (默认: 8000)')
    parser.add_argument('--check', action='store_true', help='仅检查依赖')
    parser.add_argument('--check-branch', action='store_true', help='检查分支版本映射')
    
    args = parser.parse_args()
    
    if args.check:
        check_dependencies()
        return
    
    if args.check_branch:
        # 运行分支检查
        try:
            subprocess.run([sys.executable, 'check_branch_versions.py'], check=True)
            return
        except subprocess.CalledProcessError:
            sys.exit(1)
    
    success = build_docs(clean=args.clean, serve=args.serve, port=args.port)
    
    if success:
        print("\n🎉 构建成功!")
        if not args.serve:
            print(f"📁 文档位置: {Path('_build/html').absolute()}")
            print("💡 提示: 使用 --serve 参数启动本地服务器预览")
    else:
        print("\n❌ 构建失败!")
        sys.exit(1)

if __name__ == "__main__":
    main() 