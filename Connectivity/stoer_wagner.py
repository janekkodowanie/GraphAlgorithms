from math import inf

from queue import PriorityQueue


class Node:
    def __init__(self):
        self.edges = {}

    def add_edge(self, node, weight):
        self.edges[node] = self.edges.get(node, 0) + weight

    def remove_edge(self, node):
        del self.edges[node]


def merge_vertices(G, u, v):
    v_vertices = list(G[v].edges.items())
    for vertex, w in v_vertices:
        if vertex != u:
            G[u].add_edge(vertex, w)
            G[vertex].add_edge(u, w)

        G[v].remove_edge(vertex)
        G[vertex].remove_edge(v)


def min_cut_phase(G):
    n = len(G)
    a = 0

    S = []

    Q = PriorityQueue()
    Q.put((0, a))

    visited = [False for _ in range(n)]
    weights = [0 for _ in range(n)]

    while not Q.empty():
        (w, v) = Q.get()

        if not visited[v]:
            S.append(v)
            visited[v] = True
            for u, weight in G[v].edges.items():
                if not visited[u]:
                    weights[u] += weight
                    Q.put((-weights[u], u))

    s = S[-1]
    t = S[-2]

    cut = 0
    for v, weight in G[s].edges.items():
        cut += weight
    merge_vertices(G, t, s)
    return cut


def Stoer_Wagner(Edges, n):
    G = [Node() for _ in range(n)]

    for (u, v, w) in Edges:
        G[u - 1].add_edge(v - 1, w)
        G[v - 1].add_edge(u - 1, w)

    res = inf
    while n > 1:
        res = min(res, min_cut_phase(G))
        n -= 1

    return res
