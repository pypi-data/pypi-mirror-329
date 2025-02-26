from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mukh",
    version="0.0.1",
    author="Ishan Dutta",
    author_email="duttaishan098@gmail.com",
    description="A python package to perform a variety of tasks on face images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishandutta0098/mukh",
    project_urls={
        "Bug Tracker": "https://github.com/ishandutta0098/mukh/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.19.0",
        # Uncomment dependencies as needed
        # "opencv-python>=4.5.0",
    ],
) 