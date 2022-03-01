import numpy as np


def follower_rank(graph, f1, f3):
    """
        followerRank(i) = F1 / (F1 + F3)
        Nagmoti et al. (2010)
    """
    # degree_dict = dict(graph.degree)
    fr_dict = {}
    for i in graph.nodes:
        fr_dict[i] = f1[i] / (f1[i] + f3[i])
        # fr_dict[i] = float(f1[i]) / float(f1[i] + f3[i])
    return fr_dict


def tff(graph, f1, f3):
    """
        Twitter Follower-Followee ratio

        TFF(i) = F1 / F3

        Bigonha, Cardoso, Moro, Gonçalves, and Almeida (2012)
    """
    tff_dict = {}
    for i in graph.nodes:
        try:
            tff_dict[i] = float(f1[i]) / float(f3[i])
        except ZeroDivisionError:
            tff_dict[i] = 0.0  # 'infty'
    return tff_dict


def popularity(graph, f1):
    """
        Popularity(i) = 1 - exp(-F1)
    """
    pop_dict = {}
    for i in graph.nodes:
        pop_dict[i] = 1.0 - np.exp(0.0 - f1[i])
    return pop_dict


def paradoxical_discounted(graph, df, f1, f3):
    reciprocal_dict = reciprocal_i(graph, df)
    paradox_disc_dict = {}
    for i in graph.nodes:
        try:
            if f1[i] > f3[i]:
                paradox_disc_dict[i] = float(f1[i]) / float(f3[i])
            else:
                paradox_disc_dict[i] = float(f1[i] - reciprocal_dict[i]) / float(
                    f3[i] - reciprocal_dict[i])
        except ZeroDivisionError:
            paradox_disc_dict[i] = 0.0  # 'infty'
    return paradox_disc_dict


def reciprocal_i(graph, df):
    followers = {}
    for i in graph.nodes:
        followers[i] = []

    for _, row in df.iterrows():
        followers[row.A].append(row.B)

    return_dict = {}
    for i in graph.nodes:
        for j in followers[i]:
            if i in followers[j]:
                return_dict[i] += 1.0

    return return_dict


# def reciprocal_inefficient(graph, df):
#     return_dict = {}
#     for i in graph.nodes:
#         i_is_a_followee_of = set(df.where(df.A == i).dropna().B)
#         followers_of_i = set(df.where(df.B == i).dropna().A)
#         return_dict[i] = len(i_is_a_followee_of.intersection(followers_of_i))
#         # print(f'node {i} follows back nodes: {list(i_is_a_followee_of.intersection(followers_of_i))}')
#         # print()
#     return return_dict


def a_score(graph, f1, m4, rp3, rt3):
    """
        Acquaintance Score

        A(i) = (F1 + M4 + RP3 + RT3) / n

        Srinivasan et al. (2013)
    """
    a_score_dict = {}
    for i in graph.nodes():
        val = f1[i] + m4[i] + rp3[i] + rt3[i] / len(graph.nodes())
        a_score_dict[i] = val
    return a_score_dict


def retweet_impact(graph_social, rt2, rt3):
    """
        Retweet Impact

        RI(i) = RT2 * log(RT3)

        Pal and Counts (2011)
    """
    ri_dict = {}
    for i in graph_social.nodes():
        if rt3[i] != 0.0:
            ri_dict[i] = rt2[i] * np.log(rt3[i])
        else:
            ri_dict[i] = 0.0  # '-infty'
    return ri_dict


def mention_impact(graph_social, m1, m2, m3, m4):
    """
        Mention Impact

        Mi(i) = M3 * log(M4) - M1 * log(M2)

        Pal and Counts (2011)
    """
    mi_dict = {}
    for i in graph_social.nodes():
        if m4[i] != 0.0 and m2[i] != 0.0:
            mi_dict[i] = m3[i] * np.log(float(m4[i])) - m1[i] * np.log(float(m2[i]))
        else:
            mi_dict[i] = 0.0  # '-infty'
    return mi_dict

import networkx as nx
import scipy.sparse
import scipy.sparse.csgraph
def closeness_centrality_approx(graph):
    """
        Closeness centrality approximation
        based on:
        https://medium.com/@pasdan/closeness-centrality-via-networkx-is-taking-too-long-1a58e648f5ce
    """
    adj_matr = nx.adjacency_matrix(graph).tolil()
    dcap = scipy.sparse.csgraph.floyd_warshall(adj_matr, directed=True, unweighted=False)

    n = dcap.shape[0]
    closeness_centrality = {}
    for r in range(0, n):
        cc = 0.0
        possible_paths = list(enumerate(dcap[r, :]))
        shortest_paths = dict(filter(lambda x: not x[1] == np.inf, possible_paths))

        total = sum(shortest_paths.values())
        n_shortest_paths = len(shortest_paths) - 1.0

        if total > 0.0 and n > 1:
            s = n_shortest_paths / (n - 1)
            cc = (n_shortest_paths / total) * s
        closeness_centrality[r] = cc

    return closeness_centrality
