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
            print("Warning: Hooks directory not found")
            return

        # 确保 hooks 目录存在且有执行权限
        subprocess.run(['chmod', '-R', '755', str(hooks_dir)], check=True)
        
        # 设置全局 hooks 路径
        subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(hooks_dir)], 
                      check=True)
        
        # 验证 hook 是否正确安装
        hook_path = hooks_dir / 'pre-commit'
        if not hook_path.exists():
            print("Warning: pre-commit hook not found")
            return
            
        os.chmod(hook_path, 0o755)
        print(f"Git hooks installed successfully at: {hooks_dir}")
            
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

VERSION = '1.3.0'

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