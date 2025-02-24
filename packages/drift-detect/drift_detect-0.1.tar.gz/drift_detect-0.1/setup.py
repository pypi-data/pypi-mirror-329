from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="drift_detect",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=2.2.3', 
        'pandas>=2.2.3',
        'scipy>=1.15.2' ],

    entry_points={
        "console_scripts": [
            "drift_detect_hello = drift_detect:hello_datadrift",
        ],
    },
    
    long_description=description,
    long_description_content_type="text/markdown",
)