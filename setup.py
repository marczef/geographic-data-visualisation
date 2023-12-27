# setup.py

from setuptools import setup, find_packages

setup(
    name='geographic-data-visualisation',
    version='0.1.0',
    description='Air Pollution on Poland Map',
    author='Marcjanna Bąkowska',
    author_email='bakowska@student.agh.edu.pl',
    url='https://github.com/marczef/geographic-data-visualisation',
    packages=find_packages(),
    install_requires=[
        'geopandas',
        'pandas',
        'pytest',
        'plotly',
        'dash',
        'numpyencoder',
        'geopandas',
        'dash-bootstrap-components',
        'plotly-express',
        'statistics',
        'sphinx_rtd_theme'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)