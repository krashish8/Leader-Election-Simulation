# Check active ports: sudo netstat -tulpn

nodes=$(( $2 - $1 + 1 ))
for (( i=$1; i<=$2; i++ ))
do
    python3 $3 --id=$i --nodes=$nodes &
done
