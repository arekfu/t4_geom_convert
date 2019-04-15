#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages




name = 'Converter'
author = u'Martin Maurey'
author_email = u'martin.maurey@cea.fr'
pkg_copyright = u'2019, ' + author

test_deps = ['hypothesis', 'pytest', 'pytest-cov', 'pytest-xdist',
             'pytest-timeout']
dev_deps = test_deps  + ['flake8', 'pylint', 'sphinx', 'sphinx_rtd_theme']

setup(name=name,
      author=author,
      author_email=author_email,
      url=r'http://',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*', 'Oracle']),
      python_requires='>=3.4',
      setup_requires=['pytest-runner'],
      install_requires=['TatSu'],
      tests_require=test_deps,
      extras_require={'dev': dev_deps},
      command_options={
          'build_sphinx': {
              'source_dir': ('setup.py', 'doc/src'),
              'build_dir': ('setup.py', 'doc/build'),
              }
          },
#       data_files=[('', ['README.rst'])]
#       ,
#       use_scm_version=True
#       ,
#       entry_points={
#           'console_scripts': [
#               'valjean = valjean.cambronne.main:main'
#               ]
#           }
      )
