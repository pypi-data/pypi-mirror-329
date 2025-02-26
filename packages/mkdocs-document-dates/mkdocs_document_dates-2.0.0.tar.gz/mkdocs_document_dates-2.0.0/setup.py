from setuptools import setup, find_packages
from setuptools.command.install import install

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A MkDocs plugin for displaying accurate document creation and last modification dates."

VERSION = '2.0.0'

class PostInstallCommand(install):
    """第一个入口：通过 setuptools 的 post_install 机制，在包安装完成后自动执行 hooks 安装"""
    def run(self):
        install.run(self)
        from mkdocs_document_dates.hooks_installer import install as install_hooks  # 重命名避免冲突
        result = install_hooks()

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
            # 第二个入口：提供命令行工具，允许用户手动执行 hooks 安装
            'mkdocs-document-dates-hooks=mkdocs_document_dates.hooks_installer:install'
        ]
    },
    package_data={
        'mkdocs_document_dates': ['hooks/*'],
    },
    python_requires=">=3.6",
    cmdclass={
        'install': PostInstallCommand,
    },
)