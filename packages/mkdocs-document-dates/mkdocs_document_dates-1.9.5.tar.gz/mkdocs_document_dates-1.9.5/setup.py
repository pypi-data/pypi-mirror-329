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
        # 先卸载旧的 hooks 配置
        subprocess.run(['git', 'config', '--global', '--unset', 'core.hooksPath'], 
                      check=False)  # 忽略错误，因为可能本来就没有配置
        
        # 等待包安装完成
        subprocess.run([
            sys.executable, 
            '-c', 
            'import time; time.sleep(2); import mkdocs_document_dates'
        ], check=True)
        
        # 重新运行安装脚本
        install_script = """
#!/usr/bin/env python3
import site
import os
import sys
from pathlib import Path

def setup_hooks():
    # 先在系统路径中查找
    for site_dir in site.getsitepackages():
        hooks_dir = Path(site_dir) / 'mkdocs_document_dates' / 'hooks'
        if hooks_dir.exists():
            break
    else:
        # 再在用户路径中查找
        hooks_dir = Path(site.getusersitepackages()) / 'mkdocs_document_dates' / 'hooks'
        if not hooks_dir.exists():
            print("Error: Hooks directory not found in", site.getsitepackages())
            print("Error: Hooks directory not found in", site.getusersitepackages())
            sys.exit(1)
    
    hook_path = hooks_dir / 'pre-commit'
    if not hook_path.exists():
        print("Error: pre-commit hook not found in", hooks_dir)
        sys.exit(1)
        
    # 设置权限
    if os.name != 'nt':
        os.chmod(hooks_dir, 0o755)
        os.chmod(hook_path, 0o755)
    
    # 设置 git hooks 路径
    result = os.system(f'git config --global core.hooksPath "{hooks_dir}"')
    if result != 0:
        print("Error: Failed to set git hooks path")
        sys.exit(1)
        
    print(f"Git hooks installed successfully at: {hooks_dir}")
    return True

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

VERSION = '1.9.5'

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