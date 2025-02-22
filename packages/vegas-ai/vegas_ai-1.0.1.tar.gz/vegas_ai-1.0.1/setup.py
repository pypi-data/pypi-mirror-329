from setuptools import setup, find_packages

setup(
    name="vegas_ai",
    version="1.0.1",
    author="Saurav Shrestha , Winsmano awazico ambani",
    author_email="newarsaurav@gmail.com",
    description="A simple library for randomly selecting winners and to test if this class works.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/newarsaurav/vegas_ai.git", 
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
