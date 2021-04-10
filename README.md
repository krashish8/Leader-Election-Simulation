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
|5|5|4.36|4.36|
|50|50|47.84|47.52|
|100|100|96.36|96.12|
|150|150|145.12|144.32|
|200|200|193.48|192.52|

Average Number of Received Messages:

| Nodes |  WBS   | WBS-Modified | My Approach |
| ----- | ------ | -------------| ----------- |
|5|13.12|9.44|9.2|
|50|329.52|281.64|273.36|
|100|658.88|562.44|547.4|
|150|989.28|844.12|819.24|
|200|1318.88|1124.44|1086.48|


