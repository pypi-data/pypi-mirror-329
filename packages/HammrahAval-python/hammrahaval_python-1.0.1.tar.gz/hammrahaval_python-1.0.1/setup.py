import setuptools

with open("README.md", "r+") as file: long_description = file.read()

setuptools.setup(
    name="HammrahAval-python",
    version="1.0.1",
    author="Sepehr Dehghan",
    author_email="sepehrbiggamer@gmail.com",
    description="A library for HammrahAval Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ItsOkp-TM/HammrahAval",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)