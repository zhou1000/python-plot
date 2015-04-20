#! /usr/local/bin/python

# convert adjacent list to network, using networkx module
# subgraph has its own edge/node color and size.
# yiqian, 20150417


import sys
import matplotlib.pyplot as plt
import networkx as nx
import argparse


def parse_opt(file, delimiter = ','):
    """ Read the options for plotting graph into a list
        opt file format:
            two column: key, value
            # commenting
            #== indicating a new subgraph
    """
    opts = []
    with open(file, 'r') as f:
        opt = {} # save option in a dictionary
        for line in f:
            if line in ['\n','\r\n']:
                continue
            if line[0] != '#':
                key, val = line.split(delimiter)
                opt[key.strip()] = val.strip()
            elif line[:3] == '#==':
                if opt: # opt is not emptyx
                    opts.append(opt)
                    opt = {}
        if opt:
            opts.append(opt)
    return opts

def read_twocolumn_adjlist(filename, delimiter = ','):
    """ Read the file and save it into list of Graphs 
    twocolumn_adjlist file format:
        two column
        # commentting
        #== indicating a new graph

    Note: networkx already support multiple file format:
       adjlist, multiline_adjlist, edgelist, ...
       http://networkx.github.io/documentation/latest/reference/readwrite.html
    """
    Gs = [] # list of graphs
    with open(filename, 'r') as f:
        edges = []
        for line in f:
            if line in ['\n','\r\n']:
                continue
            if line[0] != '#':
                source, target = line.split(delimiter)
                edges.append((source.strip(), target.strip(),))
            elif line[:3] == '#==':
                if len(edges) > 0:
                    Gs.append(nx.Graph(edges))
                    edges = []
        if len(edges) > 0:
            Gs.append(nx.Graph(edges))
        return Gs

def combine_graph(Gs, opts):
    # combine the graphs in the list Gs
    G = Gs[0]
    for i in range(1,len(Gs)):
        G = nx.compose(G, Gs[i])

    # position of each nodes
    pos = nx.spring_layout(G) # Fruchterman-Reingold force-directed algorithm.

    # plot nodes and edges separately
    for i in range(len(Gs)):
        nodes = Gs[i].nodes()
        edges = Gs[i].edges()
        opt = opts[i]
        nx.draw_networkx_nodes(G, pos, nodelist = nodes, 
                               node_color = opt['node_color'], 
                               alpha = float(opt['node_alpha']), 
                               node_size = int(opt['node_size']))
        nx.draw_networkx_edges(G, pos, edgelist = edges, 
                               edge_color = opt['edge_color'], 
                               alpha = float(opt['edge_alpha']), 
                               width = int(opt['edge_width']))
    # label the nodes
    nx.draw_networkx_labels(G, pos)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_adjlist', help="the adjacent list file containing two column")
    parser.add_argument('file_opt', help="the option file")
    args = parser.parse_args()
    Gs = read_twocolumn_adjlist(args.file_adjlist)
    opts = parse_opt(args.file_opt)
    combine_graph(Gs, opts)
