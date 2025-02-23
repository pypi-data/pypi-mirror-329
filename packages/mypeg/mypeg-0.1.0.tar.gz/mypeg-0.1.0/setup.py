from setuptools import setup, find_packages

setup(
    name="mypeg",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple PEG parser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypeg",
    packages=find_packages(),
    install_requires=["lark-parser"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
