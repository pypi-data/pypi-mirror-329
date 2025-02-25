import codecs
import os
from setuptools import find_packages, setup

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.5'
DESCRIPTION = 'A light weight command line menu that supports Windows, MacOS, and Linux'
LONG_DESCRIPTION = 'A light weight command line menu. Supporting Windows, MacOS, and Linux. It has support for hotkeys'

# Setting up
setup(
    name="yyyutils",
    version=VERSION,
    author="kyw",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'lxml',
        'colorama',
        'matplotlib',
        'numpy',
        # 'scipy',
        'openpyxl',
        'psutil',
        'python-docx',  # 替换 'docx'
        'mysql-connector-python',  # 替换 'mysql-connector'
        'comtypes',  # 确认是否为第三方库
        'sortedcontainers',
        # 'pynput',
        # 'pywinauto',
        # 'pywin32',  # 替换 'win32api'
        'Pillow',
        'loguru',
        'keyboard',  # 确认是否为第三方库
        'sympy'
    ],
    license='GPL-3.0',
    keywords=['python', 'utils'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
