from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='inf_tda',
    version='0.1',
    description='Differentially private hierarchical queries with a Top-Down Approach for pandas Series with MultiIndex',
    long_description=long_description,  # Include README content here
    long_description_content_type='text/markdown',  # Specify Markdown format
    author='Fabrizio Boninsegna',
    url='https://github.com/NynsenFaber/InfTDA_py',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.2',
        'opendp>=0.12'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)