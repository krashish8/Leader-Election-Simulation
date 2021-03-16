# Leader-Election

Check active ports on the system: `sudo netstat -tulpn`
Assume that ports 8001 - 8200 are free. So, run these commands sequentially for simulation:

```
./start-servers.sh 1 200 wbs-modified.py

python3 start_election.py --startport=8001 --endport=8200

./stop-servers.sh 8001 8200
```

### Results

Nodes 		WBS  		WBS-Modified

5			12				8
50			228				179
100			576				479
150			1082			933
200			1098			899
