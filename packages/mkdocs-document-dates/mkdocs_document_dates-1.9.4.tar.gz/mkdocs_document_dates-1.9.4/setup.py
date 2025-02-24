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
        # 创建一个安装脚本
        install_script = """
#!/usr/bin/env python3
import site
import os
from pathlib import Path

def setup_hooks():
    # 查找 hooks 目录
    for site_dir in site.getsitepackages():
        hooks_dir = Path(site_dir) / 'mkdocs_document_dates' / 'hooks'
        if hooks_dir.exists():
            hook_path = hooks_dir / 'pre-commit'
            if hook_path.exists():
                # 设置权限
                if os.name != 'nt':
                    os.chmod(hooks_dir, 0o755)
                    os.chmod(hook_path, 0o755)
                # 设置 git hooks 路径
                os.system(f'git config --global core.hooksPath "{hooks_dir}"')
                print(f"Git hooks installed at: {hooks_dir}")
                return
    print("Warning: Hooks directory not found")

if __name__ == "__main__":
    setup_hooks()
"""
        # 创建安装脚本
        script_dir = Path.home() / '.mkdocs_document_dates'
        script_dir.mkdir(exist_ok=True)
        script_path = script_dir / 'setup_hooks.py'
        script_path.write_text(install_script)
        
        # 设置脚本权限
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
        
        # 执行脚本
        subprocess.run([sys.executable, str(script_path)], check=True)
            
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

VERSION = '1.9.4'

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