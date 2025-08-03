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
        
        # 创建根目录重定向页面（本地构建时重定向到当前文档）
        create_root_redirect_local(build_dir)
        
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

def create_root_redirect_local(build_dir):
    """为本地构建创建根目录重定向页面"""
    print("\n创建根目录重定向页面...")
    
    # 创建根目录的 index.html，重定向到当前文档
    root_index = build_dir / "index.html"
    
    redirect_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDK 文档</title>
    <meta http-equiv="refresh" content="0; url=./basic/index.html">
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
        <h1>SDK 文档</h1>
        <p>正在跳转到文档首页...</p>
        <p><a href="./basic/index.html">如果页面没有自动跳转，请点击这里</a></p>
    </div>
</body>
</html>"""
    
    with open(root_index, 'w', encoding='utf-8') as f:
        f.write(redirect_html)
    
    print(f"✓ 根目录重定向页面创建完成: {root_index}")
    return True

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