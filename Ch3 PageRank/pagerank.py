import numpy.linalg as LA
import sys

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from power_method import power_method

plt.close('all')

# G1 = nx.DiGraph()
# for i in range(6):
#     G1.add_node(i + 1)
# G1.add_edge(1, 2)
# G1.add_edge(1, 3)
# G1.add_edge(3, 1)
# G1.add_edge(3, 2)
# G1.add_edge(3, 5)
# G1.add_edge(4, 5)
# G1.add_edge(4, 6)
# G1.add_edge(5, 4)
# G1.add_edge(5, 6)
# G1.add_edge(6, 4)
# nx.draw_networkx(G1)
# plt.title('G1')


# plt.show()

# G2 = nx.DiGraph()
# for i in range(6):
#     G2.add_node(i + 1)
# G2.add_edge(1, 2)
# G2.add_edge(1, 3)
# G2.add_edge(2, 3)
# G2.add_edge(3, 1)
# G2.add_edge(3, 2)
# G2.add_edge(3, 5)
# G2.add_edge(4, 5)
# G2.add_edge(4, 6)
# G2.add_edge(5, 3)
# G2.add_edge(5, 4)
# G2.add_edge(5, 6)
# G2.add_edge(6, 4)
# nx.draw_networkx(G2)
# plt.title('G2')
# plt.show()

# nx.pagerank(G)

# matrix H - hyperlink matrix
def hyperlink_matrix(G):
    H = nx.adjacency_matrix(G).astype(float)
    abs_Ps = G.out_degree
    for i, j in zip(H.nonzero()[0], H.nonzero()[1]):
        if abs_Ps[f"{i + 1}"] ==0:
            print(i,j)
    #     H[i, j] = 1. / abs_Ps[f"{i + 1}"]
    # return H


# H = hyperlink_matrix(G1)

# def stochastic_matrix(G):
#     S = nx.adjacency_matrix(G).astype(float)
#     out_degrees = G.out_degree
#     for i, j in zip(S.nonzero()[0], S.nonzero()[1]):
#         S[i, j] = 1. / out_degrees[i + 1]
#     zero_row_indexes = S.getnnz(1)
#     for this in np.where(zero_row_indexes == 0):
#         for index in this:
#             for j in range(S.shape[1]):
#                 S[index, j] = 1. / S.shape[1]
#     return S
#
#
# def somewhat_inefficient_pagerank():
#     x0 = np.array(6 * [1 / 6])
#     alpha = 0.9
#     google_matrix = alpha * S
#     n = H.shape[0]
#     add_matrix = ((1 - alpha) / n) * np.ones(H.shape)
#     google_matrix = google_matrix.todense() + add_matrix
#     return power_method(google_matrix.A, x0, 30, False)
#
#
# def somewhat_inefficient_naive_pagerank():
#     x0 = np.array(6 * [1 / 6])
#     return power_method(H.todense().A, x0, 30, False)
#
#
def pagerank_power_method(H, pi0, a=0.9, maxiter=100, tol=0.001, print_everything=True):
    pi0=np.ones(H.shape[0])/H.shape[0]
    # a vector
    zero_row_indexes = H.getnnz(1)
    alpha = np.zeros(H.shape[0])
    for this in np.where(zero_row_indexes == 0):
        for index in this:
            alpha[index] = 1.0

    for k in range(maxiter):
        # todo: which one is correct???
        # pi_new = a * pi0.dot(H.A) + (a * pi0.dot(alpha) + 1 - a) * np.ones(H.shape[0]) / H.shape[0]
        pi_new = a * np.matmul(H.A, pi0) + (a * pi0.dot(alpha) + 1 - a) * np.ones(H.shape[0]) / H.shape[0]

        err = LA.norm(pi_new-pi0)
        if err <= tol:
            print("converged!")
            return pi_new
        if print_everything:
            print_power_meth_status(k, pi_new)
        pi0 = pi_new
    return pi_new
#
#
def print_power_meth_status(k, x):
    print("iteration: ", k + 1)
    print("eigenvector: ", x)
#
#
# # pagerank_power_method(H)
#
# with open('./cit-HepPh/cit-HepPh.edges', 'r') as f:
#     lines = f.readlines()
#     weighted_edges = [line.replace('\n','').split(' ') for line in lines[1:]]
# import pickle
#
# pickle.dump(weighted_edges, open("weighted_edges.p", "wb"))
#
# G = nx.DiGraph()
# for edge in weighted_edges:
#     G.add_edge(edge[0], edge[1])
# pickle.dump(G, open("G.p", "wb"))
#
# # H = hyperlink_matrix(G)
# # H = hyperlink_matrix(G)
#
# H = nx.adjacency_matrix(G).astype(float)
# pickle.dump(H, open("H.p", "wb"))
#
# plt.spy(H, markersize= 1 )
# plt.show()
#
# # from pyvis.network import Network
# # net = Network(notebook=True)
# # net.from_nx(G)
# # net.show("example.html")

import pickle

G = pickle.load(open("G.p", "rb"))
H = pickle.load(open("H.p", "rb"))

abs_Ps = G.out_degree
i_zeros = []
j_zeros = []
for i, j in zip(H.nonzero()[0], H.nonzero()[1]):
    if abs_Ps[f"{i + 1}"] ==0:
        i_zeros.append(i)
        j_zeros.append(j)
    else:
        H[i, j] = 1. / abs_Ps[f"{i + 1}"]
    # print(i, j)