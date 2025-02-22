from setuptools import setup, find_packages

setup(
    name="custom_sklearn",
    version="0.3.3",
    packages=find_packages(),
    install_requires=[],
    author="WeareUs",
    author_email="1customer11service1@gmail.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
