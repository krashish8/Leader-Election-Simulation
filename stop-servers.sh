# Check active ports: sudo netstat -tulpn

for (( i=$1; i<=$2; i++ ))
do
    kill -9 `lsof -t -i:$i`
done
