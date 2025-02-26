"""MkDocs Document Dates Plugin."""

__version__ = '2.0.0'

from .hooks_installer import install

# 第三个入口：当包被导入时自动执行 hooks 安装，作为额外保障
try:
    install()
except Exception as e:
    print(f"安装 git hooks 失败: {e}")