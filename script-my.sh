

nodes=5
algo='my-approach.py'
startport=8001
endport=$((startport-1+nodes))


algo_without_ext="${algo%.*}"

if [ ! -d "log-${algo_without_ext}" ]; then
	mkdir "log-${algo_without_ext}"
fi

if [ ! -f "log-${algo_without_ext}/result.csv" ]; then
	echo "Algo,Nodes,Network Filename,History Length,Sent Messages,Received Messages" > "log-${algo_without_ext}/result.csv"
fi

for (( history_count=2; history_count<=25; history_count++ ));
do
	rm -rf log-${algo_without_ext}/${nodes}/*
	for file in data/$nodes/*;
	do
		# Start the server
		filename=${file##*/}
		./start-servers-my.sh 1 $nodes $algo $filename $history_count

		# Start the election
		sleep 10s
		python3 start_election.py --startport=$startport --endport=$endport

		# Check if every node receives the leader ID
		sleep 1s
		filename_without_ext="${filename%.*}"
		while true;
		do
			if [[ $(cat "log-${algo_without_ext}/${nodes}/${filename_without_ext}-count.txt") -eq $nodes ]];
			then
				break
			fi
			sleep 1s
		done

		# Save the result
		sleep 1s
		log_file="log-${algo_without_ext}/${nodes}/${filename_without_ext}.txt"
		sent=$(cat $log_file | grep 'Sent' | wc -l)
		received=$(cat $log_file | grep 'Received' | wc -l)
		echo "${algo_without_ext},${nodes},${filename_without_ext},${history_count},${sent},${received}" >> "log-${algo_without_ext}/result.csv"


		sleep 1s
		./stop-servers.sh $startport $endport
	done

done
