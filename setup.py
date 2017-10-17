from setuptools import setup

setup(name='instax_api',
      version='0.1',
      description='Fujifilm Instax SP2 Library',
      url='https://github.com/jpwsutton/instax_api',
      author='James Sutton',
      author_email='james@jsutton.co.uk',
      license='MIT',
      packages=['instax'],
      install_requires=[
          'Pillow',
      ],
      scripts=['bin/instax-print'],
      zip_safe=False)
