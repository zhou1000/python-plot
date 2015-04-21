#! /usr/local/bin/python

# convert adjacent list to network, using networkx module
# plot edge and nodes separately
# yiqian, 20150420


import sys
import matplotlib.pyplot as plt
import networkx as nx
import argparse

def load_file(file):
    """ Read the file, return a list of strlist, strlist is a list of string, separate by #==
    file format:
        # commentting
        #== indicating a new set of strings/lines
    """
    strlists = []
    with open(file, 'r') as f:
        strlist = []
        for line in f:
            if line in ['\n','\r\n']:
                continue
            if line[0] != '#':
                strlist.append(line.strip())
            elif line[:3] == '#==':
                if len(strlist) > 0:
                    strlists.append(strlist)
                    strlist = []
        if len(strlist) > 0:
            strlists.append(strlist)
        return strlists

def load_nodelists(file):
    """ Read the file, return a list of nodelist, a nodelist contains a group of nodes
    file format:
        single column
        # commenting
        #== indicating a new set of nodes
    """
    nodelists = load_file(file)
    return nodelists

def load_edgelists(file, delimiter = ','):
    """ Read the file, return a list of edgelist
    file format:
        two column
        # commentting
        #== indicating a new set of edges
    """
    strlists = load_file(file)
    edgelists = []
    for strlist in strlists:
        edgelist = []
        for string in strlist:
            source, target = string.split(delimiter)
            edgelist.append((source.strip(), target.strip(),))
        edgelists.append(edgelist)
    return edgelists


def load_opts(file, delimiter = ','):
    """ Read the options for plotting graph, return a list of dictionary
        opt file format:
            two column: key, value
            # commenting
            #== indicating a new set of options
    """
    strlists = load_file(file)
    opts = []
    for strlist in strlists:
        opt = {}
        for string in strlist:
            key, val = string.split(delimiter)
            opt[key.strip()] = val.strip()
        opts.append(opt)
    return opts


def plot_graph(nodelists, edgelists, node_opts, edge_opts):
    """ Given the lists of nodelist and edgelist, plot them together
    """
    # integrate all the nodes and edges
    G = nx.Graph()
    for nodelist in nodelists:
        G.add_nodes_from(nodelist)
    for edgelist in edgelists:
        G.add_edges_from(edgelist)

    # position of each nodes
    pos = nx.spring_layout(G) # Fruchterman-Reingold force-directed algorithm.

    # plot nodes and edges separately
    for i in range(len(nodelists)):
        nodelist = nodelists[i]
        node_opt = node_opts[i]
        nx.draw_networkx_nodes(G, pos, nodelist = nodelist, 
                               node_color = node_opt['node_color'], 
                               alpha = float(node_opt['node_alpha']), 
                               node_size = int(node_opt['node_size']))
    for i in range(len(edgelists)):
        edgelist = edgelists[i]
        edge_opt = edge_opts[i]
        nx.draw_networkx_edges(G, pos, edgelist = edgelist,
                               edge_color = edge_opt['edge_color'], 
                               alpha = float(edge_opt['edge_alpha']), 
                               width = int(edge_opt['edge_width']))
    # label the nodes
    nx.draw_networkx_labels(G, pos)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('nodelists', help="the file containing the list of all nodes")
    parser.add_argument('edgelists', help="the file containing the list of all edges")
    parser.add_argument('node_opts', help="the file containing the plot options for nodes")
    parser.add_argument('edge_opts', help="the file containing the plot options for edges")
    args = parser.parse_args()

    nodelists = load_nodelists(args.nodelists)
    edgelists = load_edgelists(args.edgelists)
    node_opts = load_opts(args.node_opts)
    edge_opts = load_opts(args.edge_opts)

    plot_graph(nodelists, edgelists, node_opts, edge_opts)
