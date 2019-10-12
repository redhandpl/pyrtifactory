import os
from setuptools import find_packages
from setuptools import setup

with open(os.path.join('pyrtifactory', 'VERSION')) as file:
    version = file.read().strip()

with open('README.md') as file:
    long_description = file.read()

setup(
    name='pyrtifactory',
    description='Python Artifactory REST API Wrapper',
    long_description=long_description,
    version=version,
    download_url='https://github.com/redhandpl/pyrtifactory',

    author='Krzysztof Pedrys <redhand>',
    author_email='redhand@countzero.eu.org',
    url='https://github.com/redhandpl/pyrtifactory',
    keywords='artifactory rest api',

    packages=find_packages(),
    package_dir={'pyrtifactory': 'pyrtifactory'},
    include_package_data=True,

    zip_safe=False,
    install_requires=[
        'requests',
    ],
    platforms='Platform Independent',

    classifiers=[
        'Development Status :: 0.1 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.x',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
