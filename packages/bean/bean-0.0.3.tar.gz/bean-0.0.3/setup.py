#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'bean',
  version = '0.0.3',
  description = 'A simple devops toolkit',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/bean',
  download_url = 'https://github.com/acegik/bean/downloads',
  keywords = ['tools'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=3.7",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)
