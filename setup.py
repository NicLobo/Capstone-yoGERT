# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# This call to setup() does all the work
setup(
    name="yoGERT",
    version="0.0.2",
    description="An open source version of the GERT toolbox",
    long_description="An open source version of the GERT library. Used for analysis of GPS datasets.",
    long_description_content_type="text/markdown",
    url="https://medium-multiply.readthedocs.io/",
    author="Abeer Al-Yasiri, Longwei Ye, Nicholas Lobo, Niyatha Rangarajan, Smita Singh, Moksha Srinivasan",
    author_email="moksha.srinivas@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(include=['yoGERT','yoGERT.*']),
    include_package_data=True,
    install_requires=["pandas>=1.0.1", "numpy>=1.18.4", "scipy>=1.8.0", "geopandas>=0.10.2", "h3>=3.4.1", "osmnx>=1.0.0", "networkx>=2.8.4", "scikit-learn>=1.1.3", "overpy>=0.6", "geopy>=1.12.0", "requests>=2.12.1", "python-dateutil>=2.7.5", "branca>=0.1.0", "folium>=0.9.0"]
)