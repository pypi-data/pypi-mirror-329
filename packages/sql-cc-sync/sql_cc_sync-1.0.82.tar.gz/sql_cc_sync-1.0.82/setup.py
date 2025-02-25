import os
import sys

from setuptools import setup, find_packages


def get_version() -> str:
    """
    Extracts the __version__ from sql_cc_sync.__init__.py
    """
    with open('sql_cc_sync/__init__.py', 'r') as f:
        for line in f.readlines():
            if '__version__' in line.strip():
                # parse: __version__ == x.x.x and extract
                # only the version number after the = sign
                parts = line.strip().split('=')
                version = parts[1].strip()

                # we don't want a quoted string literal
                return version.replace("'", "").replace('"', '')

    raise ValueError('No version number found')


with open('README.md', 'r') as f:
    long_description = f.read().strip()

AUTHOR = [
    'David S. Fulford',
]

AUTHOR_EMAIL = [
    'dfulford@eivcapital.com',
]

INSTALL_REQUIRES = [
    'combocurve-api-helper>=1.1.6',
    'pandas>=2.0',
    'percival>=1.2.0',
    'rich',
]

if sys.argv[-1] == 'build':
    print('\nBuilding...')
    os.system('rm -r dist\\')
    os.system('python setup.py sdist bdist_wheel')

setup(
    name='sql-cc-sync',
    version=get_version(),
    description='SQL <-> CC synchronization interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/gryphonog/eiv/cc_api_scripts',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=None,
    zip_safe=False,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['sql-cc-sync=sql_cc_sync.main:main']
    },
)
