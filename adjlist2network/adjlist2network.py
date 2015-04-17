#! /usr/local/bin/python

# convert adjacent list to network, using networkx module
# file format:
#     #comment
#     #== indicate edge group
#

# yiqian, 20150417


import sys
import matplotlib.pyplot as plt
import networkx as nx


def adjlist2network(filename, delimiter = ','):
    G = nx.Graph()
    nodes = set()
    edges = list()
    edge_num_counter = 0
    edge_group_starts = [0]
    with open(filename,'r') as f:
        for line in f:
            if line[0] != '#':
                source, target = line.split(delimiter)
                nodes.add(source)
                nodes.add(target)
                edges.append((source, target,))
                edge_num_counter += 1
            elif line[:3] == '#==':
                edge_group_starts.append(edge_num_counter)
    
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    # # pos = nx.spring_layout(G) # positions for all nodes
    # pos=nx.get_node_attributes(G,'pos')
    
    # # nodes
    # # nx.draw_networkx_nodes(G, pos, nodelist = list(nodes))

    # print pos
    # # edges
    # edge_group_starts.append(len(edges))
    # edge_colors = ['r','b','k']
    # for i in range(len(edge_group_starts)-1):
    #     group_start = edge_group_starts[i]
    #     group_stop = edge_group_starts[i+1]
    #     nx.draw_networkx_edges(G, pos,
    #                        edgelist = edges[group_start: group_stop],
    #                        edge_color = edge_colors[i])

    # # label
    # node_list = list(nodes)
    # node_names = {i: node_list[i] for i in range(len(node_list))}
    # # nx.draw_networkx_labels(G, pos, node_names)
    nx.draw(G)
    plt.show()


if __name__ == "__main__":
    filename = sys.argv[1]
    adjlist2network(filename)
