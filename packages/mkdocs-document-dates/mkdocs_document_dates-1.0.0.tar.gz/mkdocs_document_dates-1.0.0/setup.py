from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import subprocess
from pathlib import Path

def install_git_hooks():
    try:
        project_dir = Path(__file__).parent.absolute()
        hooks_dir = project_dir / 'mkdocs_document_dates' / 'hooks'
        
        if not hooks_dir.exists():
            return

        # 通过 git hooks 机制捕获 git commit 事件，git 在执行 commit 时会自动查找并执行 pre-commit hook
        subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(hooks_dir)], 
                      check=True)
        
        hook_path = hooks_dir / 'pre-commit'
        if hook_path.exists():
            os.chmod(hook_path, 0o755)
            
    except Exception as e:
        print(f"Warning: Failed to install git hooks: {e}")

class CustomBuildPy(build_py):
    def run(self):
        build_py.run(self)
        install_git_hooks()

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A MkDocs plugin for displaying accurate document creation and last modification dates."

VERSION = '1.0.0'

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
        'build_py': CustomBuildPy,  # 在构建时安装 hooks，无论是正式安装还是开发模式安装，都会经过构建阶段
    },
    package_data={
        'mkdocs_document_dates': ['hooks/*'],
    },
    python_requires=">=3.6",
)