import copy
import os

import dimacs

from math import inf

from Flow import ford_fulkerson_list, graph_search

import stoer_wagner


def create_graph(Edges, n):
    G = [[] for _ in range(n)]

    for (u, v, w) in Edges:
        G[u - 1].append((v - 1, 1))
        G[v - 1].append((u - 1, 1))

    return G


def connectivity_using_Ford_Fulkerson(Edges, n):
    ListGraph = create_graph(Edges, n)

    minFlow = inf
    for u in range(n):
        for v in range(u + 1, n):
            if u != v:
                Graph = copy.deepcopy(ListGraph)
                currentFlow = ford_fulkerson_list.FordFulkerson_List(Graph, u, v, graph_search.DFS_list)
                minFlow = min(minFlow, currentFlow)

    return minFlow


def test_file(filename, function):
    print("Testing file: " + filename)
    n, L = dimacs.loadWeightedGraph(filename)

    minFlow = function(L, n)
    result = dimacs.readSolution(filename)

    print(result, minFlow)

    return result == minFlow


def test_algorithm(algorithm):
    path = os.getcwd() + "/connectivity"
    files = os.listdir(path)
    print(files)
    files.sort(key=lambda file: os.path.getsize(path + "/" + file))
    print(files)

    for file in files:
        good = test_file(path + "/" + file, algorithm)
        if not good:
            print("Bad result for file: " + file)

    return


if __name__ == '__main__':
    test_algorithm(stoer_wagner.Stoer_Wagner)
    test_algorithm(connectivity_using_Ford_Fulkerson)
