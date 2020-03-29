## pandemic_simulation 


## Table of contents
* [Disclaimer](#disclaimer)
* [Version](#version)
* [General info](#general-info)
* [Technologies](#technologies)
* [Known Issues](#issues)

## Disclaimer
I am a self taught software developer with no medical/virology background or any formal computer science education. 
The included virus characteristics are completly made up. 
If you notice any errors, feel free to contact me or comment on this project.


## Version
This is work in progress.

## General info
This project is a simple pandemic simulator. It was inspired by the fallowing video by 3Blue1Brown youtube.com channel:
https://www.youtube.com/watch?v=gxAaO2rsdIs

This project is supposed to make a simple pandemic simulation available to everyone. The user can set up a pandemic simulation using a simple GUI,
customize different simulation parameters and plot the pandemic curve with Plotly. The goal was to visualize how different settings and behaviours influnce the progression of a pandemic.

The fallowing simulation parameters can be customized:
*Simulation population size
*No of infected people at the beginning of the simulation

*Distance a single person can move every day

*Virus name
*Virus death rate (How deadly a virus is during the infected period.)
*Virus contagiousness (Propability a healthy person inside a contagious area around a sick person will be infected.)
*Virus contagious area (Area around a infected person that is contagious)
*Virus infection time (Time someone is sick and can spread the infection)


Features:
*Simple GUI
*Save virus profiles to .json file in ./ressources/ directory
*Plot pandemic curve using Plotly

## Technologies
Project is created with:
* Python version: 3.8
* PyQt version: 5
* Plotly: 4.5.4
	
## Known Issues
*Very long calculation time with large populations (pop > 3000)

```


