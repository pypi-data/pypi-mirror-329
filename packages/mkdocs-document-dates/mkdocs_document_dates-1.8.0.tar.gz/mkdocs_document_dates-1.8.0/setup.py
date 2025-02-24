from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py
import os
import sys
import subprocess
from pathlib import Path

def install_git_hooks():
    try:
        # 获取当前执行的 Python 解释器路径
        python_path = sys.executable
        
        # 获取包的安装路径（使用 -c 参数在所有平台都有效）
        result = subprocess.check_output(
            [python_path, '-c', 'import mkdocs_document_dates; print(mkdocs_document_dates.__file__)'],
            text=True,
            shell=True if os.name == 'nt' else False  # Windows 需要 shell=True
        ).strip()
        
        install_dir = Path(result).parent  # Path 自动处理不同系统的路径分隔符
        hooks_dir = install_dir / 'hooks'
        
        if not hooks_dir.exists():
            print("Warning: Hooks directory not found")
            return

        # 跨平台设置文件权限
        hook_path = hooks_dir / 'pre-commit'
        if not hook_path.exists():
            print("Warning: pre-commit hook not found")
            return
            
        # 使用 os.chmod 代替 chmod 命令
        if os.name != 'nt':  # 非 Windows 系统才设置权限
            os.chmod(hooks_dir, 0o755)
            os.chmod(hook_path, 0o755)
        
        # 设置全局 hooks 路径（git 命令在所有平台都一样）
        subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(hooks_dir)], 
                      check=True)
        
        print(f"Git hooks installed successfully at: {hooks_dir}")
            
    except Exception as e:
        print(f"Warning: Failed to install git hooks: {e}")

class CustomInstall(install):
    def run(self):
        install.run(self)
        install_git_hooks()

class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        install_git_hooks()

class CustomBuildPy(build_py):
    def run(self):
        build_py.run(self)
        install_git_hooks()

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A MkDocs plugin for displaying accurate document creation and last modification dates."

VERSION = '1.8.0'

setup(
    name="mkdocs-document-dates",
    version=VERSION,
    author="Aaron Wang",
    description="A MkDocs plugin for displaying accurate document creation and last modification dates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaywhj/mkdocs-document-dates",
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'mkdocs.plugins': [
            'document-dates = mkdocs_document_dates.plugin:DocumentDatesPlugin',
        ]
    },
    cmdclass={
        'build_py': CustomBuildPy,
        'install': CustomInstall,
        'develop': CustomDevelop,
    },
    package_data={
        'mkdocs_document_dates': ['hooks/*'],
    },
    python_requires=">=3.6",
)