## Project Name: yoGERT

![MicrosoftTeams-image](https://user-images.githubusercontent.com/59780995/230817195-7d554f40-5cee-4bff-b651-677b526a2dee.png)  

## Introduction

yoGERT is a Python open source library of the reimplementation of the GIS-based Episode Reconstruction Toolkit (GERT) toolbox functionality. It is main purpose is to match GPS traces to a transportation network without the use of any proprietary software such as ArcPro. GPS traces are found in many different applications, including shared bicycle systems, ride hailing applications, and mobility data; matching GPS traces to transportation networks is an important step to analyze mobility data in the geospatial industry.  

_To better understand the project's domain please refer to the [Common Terminology](https://github.com/NicLobo/Capstone-yoGERT/wiki/Common-Terminology) wiki page._

## yoGERT's Functionality:
- Processing GPS data to clean and reformat data. 
- Episode generation (stop, walk, or drive mode detection) to faciliate movement behaviour analysis.
- Activity location generation to identify amenities of interest at stop points. 
- Route generation (with the entity's detected transportation mode or bus transportation mode) from GPS traces or extracted episodes. 
- Visualization of outputs on interactive maps. 

## How To Use

The library is available on pip. It can be installed on command-line using the command:  
```
pip install yoGERT 
```
To learn more about the library functions please refer to the [User Guide](https://github.com/NicLobo/Capstone-yoGERT/blob/main/docs/UserGuide/UserGuide.pdf) document.   
_To better understand the typical system use case check out the [System End Behaviour](https://github.com/NicLobo/Capstone-yoGERT/wiki/System-End-Behaviour) wiki page._

## Repository Structure:

- [__doc__](https://github.com/NicLobo/Capstone-yoGERT/tree/main/docs): Technical documentation for the project  
- [__src__](https://github.com/NicLobo/Capstone-yoGERT/tree/main/src): Implementation of the project
- [__test__](https://github.com/NicLobo/Capstone-yoGERT/tree/main/test): Manual and automated testing for the project
- [__setup__](https://github.com/NicLobo/Capstone-yoGERT/tree/main/setup): Enviornment dependency information
- [__refs__](https://github.com/NicLobo/Capstone-yoGERT/tree/main/refs): Project supporting and referenced material

## Project Video

![vidqr](https://user-images.githubusercontent.com/59780995/230816029-558f6400-c813-4206-b5c5-1b4eee2b9ebe.png)

## Developers  
Abeer Alyasiri, Longwei Ye, Moksha Srinivasan, Nicholas Lobo, Niyatha Rangarajan, Smita Singh

__Starting Date of Project__: 21st September, 2022

