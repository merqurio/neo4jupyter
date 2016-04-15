from setuptools import setup, find_packages

setup(
    name='neo4jupyter',
    version='0.1.0',
    keywords='jupyter neo4j graphdb',
    url='https://github.com/merqurio/neo4jupyter',
    license='MIT',
    author='Gabriel de Maeztu',
    author_email='gabriel.maeztu@gmail.com',
    scripts=['neo4jupyter.py'],
    description='A neo4j visualizer for Jupyter',
    long_description='To be done',
    packages=find_packages(exclude=['docs', 'build', 'test*', '*.egg-info']),
    install_requires=[
        'IPython >= 4.0.0',
        'py2neo'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
