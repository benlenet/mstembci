# Sternberg Task
This repository contains a PsychoPY implementation of the Sternberg Working Memory Task, designed to synchronize with a Matlab SIMULINK Model of an EEG amplifier. 

## TODO List
* Finalize prompting text for the participant
* Add practice trial run 
* Add timing synchronization
* Add logging data for reaction time and Accuracy 

## Mapping Headset
This experiment uses the [g.tec Nautilus 8-Channel Dry EEG Headset](https://www.gtec.at/product/g-nautilus-research/?srsltid=AfmBOopZi8mVtdq8GTyisuGzCSdBA6f8W5MG8NtzNnF6aHY3dzxtEMB9)
Prior to putting on the headset, ensure the channels are lined up like so:
| F3 | F4 | F7 | F8 | P3 | P4 | T7 | T8 | REF | GND |
-----------------------------------------------------
| Ch.1 | Ch.2 | Ch.3 | Ch.4 | Ch.5 | Ch.6 | Ch.7 | Ch.8 | Left Mastoid | Right Mastoid |

