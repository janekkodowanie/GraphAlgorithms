import multiprocessing
import os
import time
from typing import Any

import dimacs
from ford_fulkerson_list import FordFulkerson_List
from ford_fulkerson_matrix import FordFulkerson_Matrix
from graph_search import DFS_list, BFS_list, DFS_matrix, BFS_matrix


def create_matrix(Edges: list[tuple[int, int]], n: int) -> list[list[int]]:
    Matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v, w in Edges:
        try:
            Matrix[u - 1][v - 1] = w

        except IndexError:
            print(f"IndexError: {u}, {v}, {w}")

    return Matrix


def transform_to_list(Matrix) -> list[list[Any]]:
    n = len(Matrix)
    Graph = [[] for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if Matrix[u][v]:
                Graph[u].append((v, Matrix[u][v]))
                Graph[v].append((u, Matrix[v][u]))

    return Graph


def import_for_function(function, L, V):
    if function == FordFulkerson_List:
        return transform_to_list(create_matrix(L, V))
    elif function == FordFulkerson_Matrix:
        return create_matrix(L, V)


def run_function(function, G, source, sink, queue, graph_search_func):
    res = function(G, source, sink, graph_search_func)
    queue.put(res)


def test_file(function, graph_search_func, name):
    V, L = dimacs.loadDirectedWeightedGraph(name)

    G = import_for_function(function, L, V)

    expected_result = dimacs.readSolution(name)

    result_queue = multiprocessing.Queue()  # Create a multiprocessing Queue

    process = multiprocessing.Process(target=run_function, args=(function, G, 0, V - 1, result_queue, graph_search_func))
    process.start()
    process.join(TIME_LIMIT)

    if process.is_alive():
        process.terminate()
        print(f"Function exceeded time limit.")
        return False

    result = result_queue.get()

    if expected_result != result:
        print(f"Expected: {expected_result}, got: {result}")

    return expected_result == result


def test_function(function, graph_search_func):

    start_time = time.time()

    print(f"Testing {function.__name__} {graph_search_func}\n")
    directory = os.path.join(os.curdir, "flow")
    for file in os.listdir(directory):
        print(f"Testing {file}")
        if test_file(function, graph_search_func, os.path.join(directory, file)):
            print(f"Passed {file}")
        else:
            print(f"Failed on {file}")
        print()

    print(f"Testing {function.__name__} {graph_search_func} took {time.time() - start_time} seconds")


TIME_LIMIT = 15

if __name__ == '__main__':

    # List representation
    test_function(FordFulkerson_List, DFS_list)
    print()
    test_function(FordFulkerson_List, BFS_list)
    print()

    # Matrix representation
    test_function(FordFulkerson_Matrix, DFS_matrix)
    print()
    test_function(FordFulkerson_Matrix, BFS_matrix)
