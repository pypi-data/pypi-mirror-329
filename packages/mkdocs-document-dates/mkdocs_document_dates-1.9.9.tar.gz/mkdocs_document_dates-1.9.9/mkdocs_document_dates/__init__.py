"""MkDocs Document Dates Plugin."""

__version__ = '1.0.0'

from .hooks_installer import install

# 当包被导入时自动安装 hooks
try:
    install()
except Exception as e:
    print(f"自动安装 git hooks 失败: {e}")