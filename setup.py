#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


name = 't4_geom_convert'
author = u'Davide Mancusi, Martin Maurey'
author_email = u'davide.mancusi@cea.fr'
pkg_copyright = u'2019, ' + author

test_deps = ['pytest', 'pytest-cov', 'pytest-xdist', 'pytest-timeout']
dev_deps = test_deps  + ['flake8', 'pylint', 'sphinx', 'sphinx_rtd_theme']

setup(name=name,
      author=author,
      author_email=author_email,
      url=r'https://github.com/arekfu/t4-geom-convert/',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*', 'Oracle']),
      python_requires='>=3.5',
      setup_requires=['pytest-runner', 'setuptools-scm'],
      install_requires=['TatSu==4.3.0', 'numpy', 'scipy'],
      tests_require=test_deps,
      extras_require={'dev': dev_deps},
      command_options={
          'build_sphinx': {
              'source_dir': ('setup.py', 'doc/src'),
              'build_dir': ('setup.py', 'doc/build'),
              }
          },
      include_package_data=True,
      use_scm_version=True,
      entry_points={
          'console_scripts': [
              't4_geom_convert = t4_geom_convert.main:main'
              ]
          }
      )
