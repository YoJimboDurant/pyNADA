from setuptools import setup, find_packages

setup(
    name='pyNADA',
    version='0.0.1.dev1',
    description='This python program is an attempt to '
    'translate the R function ros from the package NADA '
    '(Lee 2013) into python 2.',
    classifiers=[
      'Development Status :: 1 - Planning',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python :: 2.7',
      'Topic :: Scientific/Engineering',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Topic :: Scientific/Engineering :: Bio-Informatics',
      'Topic :: Scientific/Engineering :: Information Analysis',
      'Topic :: Scientific/Engineering :: Mathematics'
    ],

    author='James Durant',
    author_email='jamesdrenda@charter.net',

    install_requires=['numpy', 'scipy'],
    packages=find_packages(),
    include_package_data=True
)
