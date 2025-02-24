#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#


from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='motorcortex-robot-control-python',
      version='3.1.3',
      description='Python bindings for Motorcortex Robot Control',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alexey Zakharov',
      author_email='info@vectioneer.com',
      url='https://www.motorcortex.io',
      license='MIT',
      packages=['robot_control'],
      install_requires=['motorcortex-python'],
      include_package_data=True,
      )
