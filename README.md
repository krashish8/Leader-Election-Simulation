# Leader-Election-Algorithm

Simulation of Leader Election algorithm, using Flask framework in Python:
- [WBS Algorithm](https://www.researchgate.net/publication/320933776_A_Wait-Before-Starting_Algorithm_for_Fast_Fault-Tolerant_and_Low_Energy_Leader_Election_in_WSNs_dedicated_to_Smart-cities_and_IoT)
- [WBS Modified Algorithm Dedicated to Smart-cities](https://dl.acm.org/doi/pdf/10.1145/3341325.3342014)
- My Approach

### Usage

Check active ports on the system: `sudo netstat -tulpn`  
Assuming that ports 8001 - 8200 are free, run one of these commands for simulation:

```
./script.sh     # For WBS algorithm, and WBS modified algorithm
./script-my.sh  # For my approach
```

### Results

Average Number of Sent Messages:

| Nodes |  WBS  | WBS-Modified | My Approach |
| ----- | ----- | -------------| ----------- |
|5|5|4.36|2.08|
|50|50|47.84|36.48|
|100|100|96.36|79.24|
|150|150|145.12|119.28|
|200|200|193.48|160.24

Average Number of Received Messages:

| Nodes |  WBS   | WBS-Modified | My Approach |
| ----- | ------ | -------------| ----------- |
|5|13.12|9.44|3.96|
|50|329.52|281.64|114.48|
|100|658.88|562.44|256.44|
|150|989.28|844.12|386.08|
|200|1318.88|1124.44|524.64


