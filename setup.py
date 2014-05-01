import os
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    sys.exit(os.system('python setup.py sdist upload'))



def read(fname):
   with open(os.path.join(os.path.dirname(__file__), fname)) as f:
       return f.read()


setup(
    name='mdtogh',
    version='0.0.9',
    packages=find_packages(),
    #install requirements
    install_requires=read('requirements.txt'),

    package_data={'mdtogh': ['templates/*']},
    include_package_data=True,

    entry_points={'console_scripts': ['mdtogh = mdtogh.command:main']},

    zip_safe=False,

    author='Summer Ruan',
    author_email='marchtea213@gmail.com',
    description='Transform markdown files into html with styles of github',
    long_description=read('descriptions.rst'),
    url='http://github.com/marchtea/mdtogh',
    platforms='any',
)
