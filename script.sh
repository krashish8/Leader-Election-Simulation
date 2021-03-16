# Check active ports: sudo netstat -tulpn

for i in {1..5}
do
    python3 leader_election.py --id=$i --nodes=5 &
done
