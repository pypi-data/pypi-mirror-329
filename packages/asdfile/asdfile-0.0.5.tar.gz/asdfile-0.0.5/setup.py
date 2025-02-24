from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='asdfile',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],  # Add a comma here
    author='Hemant Nikam',
    author_email='nikhemant@gmail.com',
    description='Flat file format for multi-tabular data storage using ASCII separator characters.',
    # python_requires='>=3.7',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
     project_urls={
        #    'Source Repository': 'https://github.com/myrepo/' #replace with your github source
    }
)
