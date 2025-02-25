[![PyPI version](https://img.shields.io/pypi/v/jupyterlab-client.svg)](https://pypi.org/project/jupyterlab-client/)
[![Python Version](https://img.shields.io/pypi/pyversions/jupyterlab-client.svg)](https://pypi.org/project/jupyterlab-client/)
[![License](https://img.shields.io/github/license/Haskely/jupyterlab-client.svg)](https://github.com/Haskely/jupyterlab-client/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/jupyterlab-client)](https://pepy.tech/project/jupyterlab-client)
[![GitHub Stars](https://img.shields.io/github/stars/Haskely/jupyterlab-client.svg)](https://github.com/Haskely/jupyterlab-client/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Haskely/jupyterlab-client.svg)](https://github.com/Haskely/jupyterlab-client/issues)
[![Dependencies](https://img.shields.io/librariesio/github/Haskely/jupyterlab-client)](https://libraries.io/github/Haskely/jupyterlab-client)

# jupyterlab-client

一个用于以编程方式与 JupyterLab 服务进行交互的 Python 客户端库。

## 功能特点

- 远程执行 Jupyter Notebook 中的 Python 代码
- 执行服务器端命令行指令
- 文件操作
  - 上传文件至 JupyterLab 服务器
  - 从 JupyterLab 服务器下载文件

## 安装

```bash
pip install jupyterlab-client
```

## 使用示例

```python
from jupyterlab_client import JupyterLabClient

# 连接到 JupyterLab 服务
client = JupyterLabClient("http://your-jupyterlab-server:8888", token="your-token")

# TODO: 添加示例代码
```

## 开发

### 安装依赖

```bash
uv sync --all-extras --dev

pre-commit install
```

### 运行测试

```bash
uv run pytest
```

### 提交代码

```bash
cz commit
```

### 发布

```bash
# 1. 确保有符合规范的提交
cz commit

# 2. 如果是首次发布，先初始化
cz init

# 3. 升级版本号
cz bump

# 4. 推送标签和更改
git push --follow-tags
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！
