# Check active ports: sudo netstat -tulpn
# E.g.: ./start-servers.sh 1 200 wbs-modified.py 11.0-0.json 5

nodes=$(( $2 - $1 + 1 ))
for (( i=$1; i<=$2; i++ ))
do
    python3 $3 --id=$i --nodes=$nodes --input_file=$4 --history_count=$5 &
done
