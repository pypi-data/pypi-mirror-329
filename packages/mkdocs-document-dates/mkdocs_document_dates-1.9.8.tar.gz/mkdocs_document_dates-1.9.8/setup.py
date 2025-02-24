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
        print("Starting hooks installation...")
        
        # 直接使用系统 Python 路径
        python_path = sys.prefix
        hooks_dir = Path(python_path) / 'lib' / f'python{sys.version_info.major}.{sys.version_info.minor}' / 'site-packages' / 'mkdocs_document_dates' / 'hooks'
        
        print(f"Looking for hooks in: {hooks_dir}")
        
        if not hooks_dir.exists():
            print(f"Error: Hooks directory not found at {hooks_dir}")
            return

        hook_path = hooks_dir / 'pre-commit'
        if not hook_path.exists():
            print(f"Error: pre-commit hook not found at {hook_path}")
            return
            
        # 设置权限
        if os.name != 'nt':
            print(f"Setting permissions for {hooks_dir}")
            os.chmod(hooks_dir, 0o755)
            os.chmod(hook_path, 0o755)
        
        # 设置 git hooks 路径
        print(f"Configuring git hooks path to: {hooks_dir}")
        result = subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(hooks_dir)], 
                              capture_output=True,
                              text=True)
        
        if result.returncode != 0:
            print(f"Error setting git hooks path: {result.stderr}")
            return
        
        print(f"Git hooks installed successfully at: {hooks_dir}")
            
    except Exception as e:
        print(f"Error installing git hooks: {e}")
        import traceback
        print(traceback.format_exc())

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

VERSION = '1.9.8'

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
        'install': CustomInstall,
        'develop': CustomDevelop,
        'build_py': CustomBuildPy,
    },
    package_data={
        'mkdocs_document_dates': ['hooks/*'],
    },
    python_requires=">=3.6",
)