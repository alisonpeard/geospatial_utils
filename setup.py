from setuptools import setup, find_packages

setup(
    name="geospatial-utils",
    version="0.01",
    author="Alison Peard",
    author_email="alison.peard@gmail.com",
    description="Handy geospatial functions for processing and visualisation. Recommend to install with -e flag.",
    packages=find_packages(),
    install_requires=[
        "python-igraph",
        "pandas",
        "geopandas",
        "networkx",
        "numpy",
        "scipy",
        "sklearn",
        "matplotlib"
    ]
)
