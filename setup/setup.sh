# this script assumes you're on a linux environment and already have python installed
# update the paths based on your own system

#!/bin/bash

#updating your system
sudo apt-get update

#installing required python packages
pip install pandas
pip install geopandas
pip install h3
pip install osmnx
pip install networkx
