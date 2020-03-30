## pandemic_simulation 


## Table of contents
* [Disclaimer](#disclaimer)
* [Version](#version)
* [General info](#general-info)
* [Example Pictures](#example pictures)
* [Technologies/dependencies](#technologies/dependencies)
* [Known Issues](#known issues)
* [Future Features](#future features)

## Disclaimer
I am a self taught software developer with no medical/virology background or any formal computer science education. 
The included virus characteristics are completly made up. 
If you notice any errors, feel free to contact me or comment on this project.

## Version
This is work in progress. Feel free to make feature requests.

## General info
This project is a simple pandemic simulator. It was inspired by the fallowing video by 3Blue1Brown youtube.com channel:
https://www.youtube.com/watch?v=gxAaO2rsdIs

This project is supposed to make a simple pandemic simulation available to everyone. The user can set up a pandemic simulation using a GUI to
customize different simulation parameters and plot the pandemic curve with Plotly. The goal was to visualize how different settings and behaviours influnce the progression of a pandemic.

The fallowing simulation parameters can be customized:
*Simulation population size
*No of infected people at the beginning of the simulation

*Distance a single person can move every day

*Virus name
*Virus death rate (How deadly a virus is during the infected period.)
*Virus contagiousness (Propability that a healthy person inside a contagious area around a sick person will be infected.)
*Virus contagious area (Area around a infected person that is contagious. It this program it is a square shape and not a circle.)
*Virus infection time (Time someone is sick and can spread the infection)


Features:
*Simple GUI
*Save virus profiles to .json file in ./ressources/ directory
*Plot pandemic curve using Plotly

## Example Pictures

[GUI example](https://github.com/joshuapeaceman/pandemic_simulation/blob/master/ressources/example_pictures/GUI.PNG)

[Standard Pandemic Settings](https://github.com/joshuapeaceman/pandemic_simulation/blob/master/ressources/example_pictures/standard_pandemic.PNG)

[Standard Pandemic Settings with contagious area set to 50](https://github.com/joshuapeaceman/pandemic_simulation/blob/master/ressources/example_pictures/stand_pandemic_contagious_area_50.PNG)

## Technologies/dependencies
Project is created with:
* Python version: 3.8
* Python random number generator (these or pseudo-random number generators)
* PyQt5 
* Plotly: 4.5.4

## Known Issues
*Very long calculation time running on large populations (pop > 3000)

## Future Features
*include quarantin settings in model
*include symptoms in model
*provide binaries


```


