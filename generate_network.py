"""
Generate a homogeneous network of some nodes
Sample run:
python3 generate_network.py --nodes=100 --x1=0 --x2=100 --y1=0 --y2=100 --node_range=15 --test_cases=5
"""

import argparse
import json
import math
import random

parser = argparse.ArgumentParser()
parser.add_argument('--nodes', required=True, type=int, help='Number of nodes in the network')
parser.add_argument('--x1', required=True, type=int, help='Starting x-coordinate of nodes')
parser.add_argument('--x2', required=True, type=int, help='Ending x-coordinate of nodes')
parser.add_argument('--y1', required=True, type=int, help='Starting y-coordinate of nodes')
parser.add_argument('--y2', required=True, type=int, help='Ending y-coordinate of nodes')
parser.add_argument('--node_range', required=True, type=float, help='Range of each node/sensor')
parser.add_argument('--test_cases', required=True, type=int, help='Number of networks to generate')
args = parser.parse_args()

nodes = args.nodes

x1 = args.x1
x2 = args.x2
y1 = args.y1
y2 = args.y2
node_range = args.node_range
test_cases = args.test_cases

if x1 > x2 or y1 > y2:
    print('Start coordinates must be less than end coordinates')
    exit(1)

import os
os.makedirs('data/' + str(nodes), exist_ok=True)

tc = 0

avg = 0

while tc < test_cases:

    network = dict()

    for i in range(1, nodes + 1):
        network[i] = dict()
        network[i]["x"] = round(random.uniform(x1, x2), 6)
        network[i]["y"] = round(random.uniform(y1, y2), 6)
        network[i]["neighbours"] = []
        network[i]["node_range"] = node_range

    def euclidean_dist(node1, node2):
        return math.sqrt((network[node1]["x"] - network[node2]["x"]) ** 2 +
                          (network[node1]["y"] - network[node2]["y"]) ** 2)

    for i in range(1, nodes + 1):
        for j in range(i + 1, nodes + 1):
            if i == j:
                continue
            # If the node j is in the range of node i, then they are neighbours
            if (euclidean_dist(i, j) <= node_range):
                network[i]["neighbours"].append(j);
                network[j]["neighbours"].append(i);

    min_neighbours = nodes
    sum_neighbours = 0

    for i in range(1, nodes + 1):
        sum_neighbours += len(network[i]["neighbours"])
        min_neighbours = min(min_neighbours, len(network[i]["neighbours"]))

    if min_neighbours == 0:
        continue

    with open('data/' + str(nodes) + '/' + str(node_range) + '-' + str(tc) + '.json', 'w') as fp:
        json.dump(network, fp, sort_keys=True)

    tc = tc + 1
    print('Density', sum_neighbours / nodes)
    avg += sum_neighbours / nodes

print('Average', avg / test_cases)
