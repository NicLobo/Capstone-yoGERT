#author: Moksha Srinivasan, 400181518
#last updated: 2023-02-07

#this script assumes the following:  
#1. you are running the toolbox in a unix environment and already have python 3 installed
#2. you are a superuser with sudo privileges, keep your password handy!

#!/usr/bin/env bash

#updating your system
sudo apt-get update

#installing required python packages
pip install pandas
pip install numpy
pip install scipy
pip install geopandas
pip install h3
pip install osmnx
pip install networkx
pip install -U scikit-learn
