import sys
from setuptools import setup


with open('README.md', 'rb') as readme_file:
    readme = readme_file.read().decode('utf-8')

setup(name='instax_api',
      version='0.4',
      description='Fujifilm Instax SP2 Library',
      long_description=readme,
      url='https://github.com/jpwsutton/instax_api',
      author='James Sutton',
      author_email='james@jsutton.co.uk',
      license='MIT',
      keywords='instax',
      packages=['instax'],
      install_requires=[
          'Pillow',
      ],
      scripts=['bin/instax-print'],
      zip_safe=False)
