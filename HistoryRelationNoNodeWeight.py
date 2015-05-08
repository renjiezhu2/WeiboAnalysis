#!/usr/bin/python
import networkx as nx
import operator


DG = nx.DiGraph()

inputFileName = raw_input("Enter a path for input File: \n")
outputFileName = raw_input("Enter a file name for output File: \n")

index = 1
with open(inputFileName, "r") as inputData:
	for line in inputData:
		print index;
		user_1, user_2 = line.split()

		if not DG.has_node(user_1):
			DG.add_node(user_1, weight=0)
		if not DG.has_node(user_2):
			DG.add_node(user_2, weight=0)

		if DG.has_edge(user_1, user_2):
			DG[user_1][user_2]['weight'] += 1
		else:
			DG.add_edge(user_1, user_2, weight=1)

		index += 1
inputData.close()

print "Performing Page Rank"
# Classic Page Rank
pr = nx.pagerank(DG)
# Personalized Page Rank
pr_personalized = nx.pagerank_numpy(DG)

sorted_pr = sorted(pr_personalized.items(), key=operator.itemgetter(1))
sorted_pr.reverse()

print "Writing Output Files"
output = open(outputFileName, "wb")
for user in sorted_pr:
	line = user[0] + "\t" + str(user[1]) + "\n"
	output.write(line)
output.close()