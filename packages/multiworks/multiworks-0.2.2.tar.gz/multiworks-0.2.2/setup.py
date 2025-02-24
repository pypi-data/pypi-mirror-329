from setuptools import setup, find_packages

setup(
    name="multiworks",
    version="0.2.2",
    packages=find_packages(),  
    include_package_data=True, 
    install_requires=[], 
    author="Mohammad Sabbir Hosen",
    author_email="hellowsabbir@gmail.com",
    description="Encrypts/decrypts messages and includes games of Rock, Paper, Scissors (RPS) and Snake, Water, Gun (SWG).",
    long_description=open("README.md", encoding="utf-8").read(), 
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://pypi.org/project/multiworks/", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)
