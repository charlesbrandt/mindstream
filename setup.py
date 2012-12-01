from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='mindstream',
      version=version,
      description="A collection of scripts, applications and modules for use with the moments library",
      long_description="""A collection of scripts, applications and modules for use with the moments library. These applications include a desktop application for creating moments/journals, scripts for sorting and processing moments, web based application to browse moments, and a desktop application to help with manually tagging moments.  For moments, please see: http://bitbucket.org/cbrandt/moments
     
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='moments mindstream journal self_tracking quantified_self wx editor playlists',
      author='Charles Brandt',
      author_email='code@contextiskey.com',
      url='http://contextiskey.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
