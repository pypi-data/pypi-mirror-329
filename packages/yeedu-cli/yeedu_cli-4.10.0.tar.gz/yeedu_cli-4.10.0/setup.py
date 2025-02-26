from setuptools import setup, find_packages
import codecs
import re
import os.path
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='yeedu-cli',
    version=find_version("yeeducli", "__init__.py"),
    description='Universal Command Line Interface for Yeedu.',
    long_description=read('README.rst'),
    author='Yeedu',
    author_email='yeedu@yeedu.io',
    url="https://yeedu.io",
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=[
        'argparse==1.4.0',
        'requests==2.28.1',
        'python-dotenv==1.0.0',
        'PyYAML==6.0',
        'setuptools==59.6.0'
    ],
    license='All Rights Reserved',
    entry_points='''
    [console_scripts]
    yeedu=yeeducli.yeedu:yeedu
    '''
)
