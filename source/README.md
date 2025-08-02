# SDK 文档构建系统

这是一个模块化的 SDK 文档构建系统，支持配置化的文档生成和自动化部署。

## 系统特点

- **模块化设计**: 将文档生成拆分为多个独立模块
- **配置驱动**: 通过 YAML 配置文件控制所有行为
- **可复用**: 一套代码可以用于多个 SDK 项目
- **自动化**: 支持 GitHub Actions 自动部署

## 目录结构

```
source/
├── config.yaml              # 主配置文件
├── template_config.yaml     # 模板配置文件
├── doc_generator.py         # 主文档生成器
├── conf.py                  # Sphinx 配置文件
├── requirements.txt         # Python 依赖
├── utils/                   # 工具模块
│   ├── __init__.py
│   ├── config_loader.py     # 配置加载器
│   ├── project_scanner.py   # 项目扫描器
│   ├── file_processor.py    # 文件处理器
│   └── index_generator.py   # 索引生成器
└── _static/                 # 静态文件
```

## 快速开始

### 1. 配置项目

复制模板配置文件并修改：

```bash
cp template_config.yaml config.yaml
```

编辑 `config.yaml` 文件，修改以下关键信息：

- `project.name`: 你的 SDK 名称
- `project.title`: 文档标题
- `repository.name`: 仓库名称
- `categories`: 根据你的项目调整分类和命名模式

### 2. 运行文档生成

```bash
cd source
python doc_generator.py
```

### 3. 查看统计信息

```bash
python doc_generator.py --stats
```

## 配置说明

### 项目配置 (project)

```yaml
project:
  name: "Your_SDK_Docs"      # SDK 文档名称
  title: "Your SDK 文档"      # 文档标题
  description: "SDK 描述"     # 文档描述
  version: "0.0.1"           # 版本号
  author: "your_name"        # 作者
  copyright: "2025, company" # 版权信息
  language: "zh_CN"          # 语言
```

### 仓库配置 (repository)

```yaml
repository:
  name: "your-sdk-repo"      # 仓库名称
  projects_dir: "../projects" # 项目目录路径
  docs_dir: "."              # 文档输出目录
```

### 分类配置 (categories)

```yaml
categories:
  basic:
    name: "基础篇"
    description: "基础功能示例"
    patterns:
      - "your_basic_*"       # 项目命名模式
```

### 生成配置 (generation)

```yaml
generation:
  copy_files:                # 要复制的文件
    - "README.md"
    - "README_zh.md"
  copy_dirs:                 # 要复制的目录
    - "figures"
  output_structure:          # 输出目录结构
    - "basic"
    - "driver"
```

## 模块说明

### ConfigLoader
负责加载和验证配置文件，提供配置信息的访问接口。

### ProjectScanner
扫描项目目录，根据配置的模式对项目进行分类。

### FileProcessor
处理文件复制操作，支持指定文件和目录的复制。

### IndexGenerator
生成各种索引文件，包括主索引和分类索引。

## 自定义扩展

### 添加新的分类

1. 在 `config.yaml` 中添加新的分类配置
2. 在 `output_structure` 中添加新分类
3. 更新主索引文件中的 toctree

### 修改文件复制规则

在 `generation.copy_files` 和 `generation.copy_dirs` 中添加或删除项目。

### 自定义 Sphinx 配置

在 `sphinx` 部分添加或修改 Sphinx 相关配置。

## GitHub Actions 集成

系统已配置好 GitHub Actions，支持自动部署到 GitHub Pages：

1. 推送到 master 分支时自动触发
2. 自动生成文档
3. 构建 Sphinx 文档
4. 部署到 GitHub Pages

## 故障排除

### 常见问题

1. **配置文件不存在**: 确保 `config.yaml` 文件存在且格式正确
2. **项目目录不存在**: 检查 `projects_dir` 路径是否正确
3. **依赖安装失败**: 确保安装了所有 Python 依赖
4. **Sphinx 构建失败**: 检查生成的文档文件是否完整

### 调试命令

```bash
# 查看项目统计
python doc_generator.py --stats

# 使用自定义配置文件
python doc_generator.py --config my_config.yaml
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

Apache License 2.0 