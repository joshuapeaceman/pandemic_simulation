## pandemic_simulation 


## Table of contents
* [Disclaimer](#disclaimer)
* [Version](#version)
* [General info](#general-info)


## Disclaimer
I am a self taught software developer with no medical/virology background or any formal computer science education. 
The included virus characteristics are completly made up. 
If you notice any errors, feel free to contact me or comment on this project.

## Version
version 1.2
This is work in progress. Feel free to make feature requests.

## General info
This project is a simple pandemic simulator. It was inspired by the fallowing video by 3Blue1Brown youtube.com channel:
https://www.youtube.com/watch?v=gxAaO2rsdIs

This project is supposed to make a simple pandemic simulation available to everyone. The user can set up a pandemic simulation using a GUI and customize different simulation parameters. The program will plot the pandemic curve with Plotly and generate a scatter plot animation. The goal was to visualize how different settings and behaviours influnce the progression of a pandemic.

Many different general simulation and virus parameters can be customized to see how they change the behaviour of the pandemic.

Features:
*Simple GUI
*Plot pandemic curves using Plotly
*Animate the spread of the pandemic inside the population
*Runs on Windows and Linux based OS

## Example Pictures

[GUI example](https://github.com/joshuapeaceman/pandemic_simulation/blob/master/ressources/example_pictures/GUI.PNG)

[Standard Pandemic Settings](https://github.com/joshuapeaceman/pandemic_simulation/blob/master/ressources/example_pictures/standard_pandemic.PNG)

[Standard Pandemic Settings with contagious area set to 50](https://github.com/joshuapeaceman/pandemic_simulation/blob/master/ressources/example_pictures/stand_pandemic_contagious_area_50.PNG)

## Technologies/dependencies
Project is created with:
* Python version: 3.8
* Python random number generator (these or pseudo-random number generators)
* PyQt5 
* Plotly

## Known Issues
*Very long calculation time running on large populations (pop > 3000). I guess its a Python problem

## Future Features



```


