import os

from setuptools import setup, find_packages

setup(
    name='treesumstats',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'treesumstats': [os.path.join('..', 'README.md'),
                                   os.path.join('..', 'LICENCE')]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    version='0.5',
    description='Encoding phylogenetic trees with summary statistics.',
    author='Anna Zhukova',
    author_email='anna.zhukova@pasteur.fr',
    url='https://github.com/evolbioinfo/treesumstats',
    keywords=['phylogenetics', 'summary statistics', 'phylogenetic trees', 'phylogeny'],
    install_requires=['ete3', 'numpy==2.0.2', "scipy==1.14.1", 'biopython', 'pandas==2.2.3'],
    entry_points={
            'console_scripts': [
                'treesumstats_encode = treesumstats.calculator:main',
            ]
    },
)
