# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

# import sys
# from distutils.command.build_py import build_py as _build_py
# from distutils.command.sdist import sdist as _sdist

# import setuptools
from setuptools import find_packages
from setuptools import setup
# from setuptools.command.develop import develop as _develop


# https://docs.python.org/3/distutils/setupscript.html
setup(
    name='wstool_wrapper',
    version='0.1.0',
    license='None',
    description='',
    author='Lionel Atty',
    author_email='yoyonel@hotmail.com',
    url='https://github.com/yoyonel/wstool_wrapper',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # http://setuptools.readthedocs.io/en/latest/setuptools.html
    # https://github.com/pypa/sampleproject/issues/30
    # https://docs.python.org/3/distutils/sourcedist.html#the-manifest-in-template
    # https://stackoverflow.com/questions/24291695/cannot-include-non-python-files-with-setup-py
    include_package_data=True,
    package_data={
        'wstool_wrappers': [
            'data/Pipfile',
            'data/Pipfile.lock'
        ]
    },
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[

    ],
    install_requires=[
        "wstool",
        "colorlog",
    ],
    extras_require={
        ':python_version == "2.7"': [

        ],
    },
    entry_points={
        'console_scripts': [
            'wstool_wrapper = wstool_wrapper.wstool_wrapper:main'
        ]
    },
    # cmdclass={
    #     'build_py': BuildPyCommand,
    #     'build_proto_modules': BuildPackageProtos,
    #     'develop': DevelopCommand,
    #     'sdist': SDistCommand
    # }
)
