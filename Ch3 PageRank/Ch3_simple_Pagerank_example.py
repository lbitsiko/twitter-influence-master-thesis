import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

plt.close('all')
fig, ax = plt.subplots()
ax.axis('off')
G = nx.Graph()  # an undirected graph object

for i in range(6): G.add_node(i + 1)

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(3, 1)
G.add_edge(3, 2)
G.add_edge(4, 5)
G.add_edge(4, 6)
G.add_edge(5, 4)
G.add_edge(5, 6)
G.add_edge(6, 4)
G.add_edge(3, 5)
spring_layout_for_G = nx.spring_layout(G, seed=100) # position of nodes not random
nx.draw_networkx(G, pos=spring_layout_for_G)
fig.savefig('./plots/Simple_pagerank_G.png', format='PNG')

fig2, ax = plt.subplots()
ax.axis('off')
G = nx.DiGraph()  # a directed graph object
for i in range(6): G.add_node(i + 1)

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(3, 1)
G.add_edge(3, 2)
G.add_edge(4, 5)
G.add_edge(4, 6)
G.add_edge(5, 4)
G.add_edge(5, 6)
G.add_edge(6, 4)
G.add_edge(3, 5)
nx.draw_networkx(G, pos=spring_layout_for_G)
fig2.savefig('./plots/Simple_pagerank_DiGraph.png', format='PNG')

H = nx.adjacency_matrix(G).astype(float)
out_degree_for_nodes_of_G = G.out_degree
for i, j in zip(H.nonzero()[0], H.nonzero()[1]):
    try:
        H[i, j] = 1. / out_degree_for_nodes_of_G[i + 1]
    except ZeroDivisionError:
        print("non zero elements appear to be zero")

