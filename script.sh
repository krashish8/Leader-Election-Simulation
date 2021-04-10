

nodes=5
algo='wbs.py'
startport=8001
endport=$((startport-1+nodes))


algo_without_ext="${algo%.*}"

if [ ! -d "results" ]; then
	mkdir "results"
fi

if [ ! -d "results/log-${algo_without_ext}" ]; then
	mkdir "results/log-${algo_without_ext}"
fi

if [ ! -f "results/log-${algo_without_ext}/result.txt" ]; then
	echo "Algo,Nodes,Network Filename,Sent Messages,Received Messages" > "results/log-${algo_without_ext}/result.csv"
fi

for file in data/$nodes/*;
do
	# Start the server
	filename=${file##*/}
	./start-servers.sh 1 $nodes $algo $filename

	# Start the election
	sleep 10s
	python3 start_election.py --startport=$startport --endport=$endport

	# Check if every node receives the leader ID
	sleep 1s
	filename_without_ext="${filename%.*}"
	while true;
	do
		if [[ $(cat "results/log-${algo_without_ext}/${nodes}/${filename_without_ext}-count.txt") -eq $nodes ]];
		then
			break
		fi
		sleep 1s
	done

	# Save the result
	sleep 1s
	log_file="results/log-${algo_without_ext}/${nodes}/${filename_without_ext}.txt"
	sent=$(cat $log_file | grep 'Sent' | wc -l)
	received=$(cat $log_file | grep 'Received' | wc -l)
	echo "${algo_without_ext},${nodes},${filename_without_ext},${sent},${received}" >> "results/log-${algo_without_ext}/result.csv"


	sleep 1s
	./stop-servers.sh $startport $endport
done

