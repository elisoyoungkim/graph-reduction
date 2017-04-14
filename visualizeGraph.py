'''
Created on May 27, 2016
@author: SoyoungKim
'''
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import database, parseDataset

if __name__ == '__main__':
    pass

graph = parseDataset.graph
prob_table = parseDataset.prob_table
np.random.seed(0)
fig = plt.figure(facecolor='white')
G = nx.DiGraph()
for node, edges in graph.items():
    G.add_node(node)
    for edge in edges:
        G.add_edges_from([(node, edge)], weight=prob_table[node + edge])

edge_labels = {}
for edge in G.edges():
    l_edge = list(edge)
    edge_labels.update({edge:prob_table[reduce(lambda x, y:x+y, l_edge)]}) 
# There are 4 graph layouts: shell, spring, spectral, and random
if len(G.nodes()) < 5:
    pos = nx.random_layout(G)
elif len(G.nodes()) >= 5 and len(G.nodes()) < 12:
    pos = nx.shell_layout(G)
else:
    pos = nx.random_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=G.nodes(), node_color='deeppink')
nx.draw_networkx_edges(G, pos, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=3, font_family='sans-serif')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
#nx.draw_networkx_nodes(G,pos,node_size=800,nodelist=[start_vertex],node_color= 'green')
#nx.draw_networkx_nodes(G,pos,node_size=800,nodelist=[end_vertex],node_color='red')
nx.draw_networkx_labels(G, pos)
ax = fig.add_subplot(111)
#ax.text(0.95, 0.01, 'Connectivity: {0}'.format(ans),
#          verticalalignment='bottom', horizontalalignment='right',
#          transform=ax.transAxes,
#          color='green', fontsize=15)
plt.axis('off')
plt.show()
