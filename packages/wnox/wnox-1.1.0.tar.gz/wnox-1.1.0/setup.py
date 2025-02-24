from setuptools import setup, find_packages

setup(
    name="wnox",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Ethan (Armin) Cardan",
    author_email="armin.fire@gmail.com",
    description="QE nexus client.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arminkardan/pywnox",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
