from setuptools import setup, find_packages

setup(
    name="omniscale",  # Package name (should be unique if publishing to PyPI)
    version="0.2a",
    packages=find_packages(),
    install_requires=[],  # List dependencies if needed
    author="Valhal4o1331",
    description="A Python package for various unit conversions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AleksandarOvcharov/Omniscale",  # Change this if uploading to GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)