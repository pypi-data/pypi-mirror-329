from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name="havinosh_data_loader",
    version="0.0.1",
    author="Vishal Singh Sangral",
    author_email="support@havinosh.com",
    description="A Python package to dynamically load CSV files into PostgreSQL tables.",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/havinosh_data_loader",  # Update with actual repo
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "data-loader=loader.scripts.ingest:main",  # CLI command
        ]
    },
    include_package_data=True,
)
