# Leader-Election

```
./start-servers.sh 1 5 wbs.py

python3 start_election.py --startport=8001 --endport=8005

./stop-servers.sh 8001 8005
```


Check active ports: `sudo netstat -tulpn`
