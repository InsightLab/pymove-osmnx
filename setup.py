try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Get the long description from the README file
try:
    long_description = open('README.md', 'r').read()
except Exception as e:
    raise e

DEPENDENCIES = [
    'pymove',
    'osmnx'
]
setup(
    name='pymove-osmnx',
    version='1.0.0',
    author='Insight Data Science Lab',
    author_email='insightlab@dc.ufc.br',
    license='MIT',
    python_requires='>=3.6',
    description='A lib python to processing and visualization '
                'of trajectories and other spatial-temporal data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/InsightLab/pymove-osmnx',
    packages=[
        'pymove-osmnx'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=DEPENDENCIES,
    include_package_data=True
)