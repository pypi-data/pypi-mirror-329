from setuptools import setup, find_packages
from setuptools.command.install_egg_info import install_egg_info
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.build_py import build_py
import os
import sys
import subprocess
from pathlib import Path
import site

def install_git_hooks():
    print("\n...Starting hooks installation...\n")
    try:
        # 先清除旧的配置
        subprocess.run(['git', 'config', '--global', '--unset', 'core.hooksPath'], 
                     check=False)
        
        # 使用 site-packages 路径
        for site_dir in site.getsitepackages():
            hooks_dir = Path(site_dir) / 'mkdocs_document_dates' / 'hooks'
            print(f"Checking hooks in: {hooks_dir}")
            if hooks_dir.exists():
                hook_path = hooks_dir / 'pre-commit'
                if hook_path.exists():
                    if os.name != 'nt':
                        os.chmod(hooks_dir, 0o755)
                        os.chmod(hook_path, 0o755)
                    subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(hooks_dir)],
                                check=True)
                    print(f"Hooks installed at: {hooks_dir}")
                    
                    # 验证配置
                    result = subprocess.run(['git', 'config', '--global', 'core.hooksPath'],
                                         capture_output=True, text=True)
                    print(f"Verified hooks path: {result.stdout.strip()}")
                    return True
        
        # 如果在 site-packages 中没找到，尝试开发目录
        dev_hooks_dir = Path(__file__).parent.resolve() / 'mkdocs_document_dates' / 'hooks'
        if dev_hooks_dir.exists():
            hook_path = dev_hooks_dir / 'pre-commit'
            if hook_path.exists():
                if os.name != 'nt':
                    os.chmod(dev_hooks_dir, 0o755)
                    os.chmod(hook_path, 0o755)
                subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(dev_hooks_dir)],
                            check=True)
                print(f"Hooks installed at (dev mode): {dev_hooks_dir}")
                return True
                
        print("Error: Hooks directory not found in any location")
        return False
    except Exception as e:
        print(f"Error installing hooks: {e}")
        return False

class CustomInstallEggInfo(install_egg_info):

    def run(self):
        print("\n=== Starting CustomInstallEggInfo run ===\n")
        print(f"Installation mode: {'Development' if '-e' in sys.argv else 'Production'}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Setup file location: {__file__}")
        print(f"Command line args: {sys.argv}")
        
        install_egg_info.run(self)
        install_git_hooks()

class CustomInstall(install):
    def run(self):
        print("\n=== Starting CustomInstall run ===\n")
        print(f"Current directory: {os.getcwd()}")
        install.run(self)
        install_git_hooks()

class CustomDevelop(develop):
    def run(self):
        print("\n=== Starting CustomDevelop run ===\n")
        develop.run(self)
        install_git_hooks()

class CustomBuildPy(build_py):
    def run(self):
        print("\n=== Starting CustomBuildPy run ===\n")
        print(f"Current directory: {os.getcwd()}")
        print(f"Build lib dir: {self.build_lib}")
        build_py.run(self)
        install_git_hooks()

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A MkDocs plugin for displaying accurate document creation and last modification dates."

VERSION = '1.9.9'

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
        ],
        'console_scripts': [
            'install-mkdocs-hooks=mkdocs_document_dates.hooks_installer:install'
        ]
    },

    package_data={
        'mkdocs_document_dates': ['hooks/*'],
    },
    python_requires=">=3.6",
)