# Sternberg Task
This repository contains a PsychoPY implementation of the Sternberg Working Memory Task, designed to synchronize with a Matlab SIMULINK Model of an EEG amplifier. 

## TODO List
* Add timing synchronization
* Add logging data for reaction time and accuracy [linked here](https://discourse.psychopy.org/t/how-to-calculate-average-response-time/5513)

## Mapping Headset
This experiment uses the [g.tec Nautilus 8-Channel Dry EEG Headset](https://www.gtec.at/product/g-nautilus-research/?srsltid=AfmBOopZi8mVtdq8GTyisuGzCSdBA6f8W5MG8NtzNnF6aHY3dzxtEMB9).
Prior to putting on the headset, ensure the channels are lined up like so:
| C3 | C4 | F3 | F4 | P3 | P4 | Pz | Cz | REF | GND |
|---|---|---|---|---|---|---|---|---|---|
| Ch.1 | Ch.2 | Ch.3 | Ch.4 | Ch.5 | Ch.6 | Ch.7 | Ch.8 | Left Mastoid | Right Mastoid |

## Today's Tasks
* Figure out the currentLoop attributes
1. continue loop after timeout to gather consistently 10 files
2. send a udp signal after the end of each loop to accurately record 
* record average reaction time and response correctness in log file
1. log each reaction time separately, and add a final data column at the end

## Research on Free Time
* look at sources for Sternberg EEG research (find comparisons)