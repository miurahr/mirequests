#!/usr/bin/env python

import io
import os

from setuptools import setup


def readme():
    with io.open(os.path.join(os.path.dirname(__file__), 'README.rst'), mode="r", encoding="UTF-8") as readmef:
        return readmef.read()


setup(name='mirequests',
      version='0.0.1',
      description='mirequests',
      url='http://github.com/miurahr/mirror_requests',
      license='LGPL-2.1',
      long_description=readme(),
      author='Hioshi Miura',
      author_email='miurahr@linux.com',
      packages=['mirequests'],
      install_requires=['requests', 'six'],
      extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'flake8'
        ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: LGPLv3 License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          ],
      )
