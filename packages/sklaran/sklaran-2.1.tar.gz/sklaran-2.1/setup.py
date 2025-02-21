from setuptools import setup, find_packages

setup(
    name="sklaran",  # Package name
    version="2.1",  # Version
    packages=find_packages(),  # Automatically find packages
    install_requires=[],  # Dependencies (leave empty if none)
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python package",
    long_description=open("README.md").read(),

    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",  # GitHub link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
