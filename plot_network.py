import numpy as np
import matplotlib.pyplot as plt

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--nodes', required=True, type=int, help='Number of nodes in the network')
args = parser.parse_args()

nodes = args.nodes

network = None

with open('data/network-' + str(nodes) + '.json', 'r') as fp:
    network = json.load(fp)

X = []
Y = []
node_range = network["1"]["node_range"]

for i in range(1, nodes + 1):
	X.append(network[str(i)]["x"])
	Y.append(network[str(i)]["y"])

plt.scatter(X, Y)

for i in range(0, nodes):
	plt.annotate(i + 1, (X[i], Y[i]))
	circle = plt.Circle((X[i], Y[i]), node_range, color='b', fill=False)
	plt.gca().add_patch(circle)


plt.show()
