from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="EpidemicKabu",
    version='0.2.0',
    description="New methodology to identify waves, peaks, and valleys from epidemic curve",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LinaMRuizG/EpidemicKabuLibrary",
    author="Lina M. Ruiz G. and Anderson A. Ruales B.",
    author_email="lina.ruiz2@udea.edu.co",
    license = 'MIT',
    packages=find_packages(include=['EpidemicKabu']),
    install_requires=['pandas==1.5.3', 'scipy==1.10.1', 'matplotlib==3.7.1','matplotlib-inline==0.1.6','numpy==1.25.2'],
    keywords=['epidemic curve', 'waves', 'peaks', 'valleys', 'gaussian filter'],
    python_requires=">=3.10.6"
)
