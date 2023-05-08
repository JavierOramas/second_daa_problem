from collections import deque
from graph import Edge, Bellman_Ford, Dijkstra, build_graph, prepare_network
import numpy as np


class MinCostMaxFlow:
    def __init__(self, n, source, sink, graph, edges):
        self.n = n
        self.source = source
        self.sink = sink
        self.graph = graph
        self.edges = edges
        self.flow = []
        self.sink_potential = 0
        self.dist_from_source = []

    def is_in_dag(self, node, n_node):
        return self.dist_from_source[node]+1 == self.dist_from_source[n_node]

    def apply_potentials(self, distances):
        for e in self.edges:
            if distances[e.source] >= np.inf or distances[e.dest] >= np.inf:
                continue
            e.cost += distances[e.source] - distances[e.dest]
            # print(self.sink_potential)
        self.sink_potential += distances[self.sink]

    def __dinitz_dfs(self, node, flow, mark):
        if node == self.sink:
            return flow, mark

        current_flow = 0
        marked = True

        for e in self.graph[node]:
            n_node = e.get_oposite_side(node)
            if not self.is_in_dag(node, n_node):
                continue

            if e.get_capacity(node) != 0 and not mark[n_node] and e.get_cost(node) == 0:
                new_flow, mark = self.__dinitz_dfs(
                    n_node, min(flow, e.get_capacity(node)), mark)
                current_flow += new_flow
                flow -= new_flow
                e.push_flow(node, new_flow)

            if e.get_capacity(node) != 0 and not mark[n_node] and e.get_cost(node) == 0:
                marked = False
        if marked:
            mark[node] = True

        return current_flow, mark

    def dinitz_dfs(self, verbose=1):
        mark = [False] * self.n
        res = self.__dinitz_dfs(self.source, np.inf, mark)[0]

        # if verbose >= 3:
        # print(f"DFS: {res}")
        return res

    def dinitz_bfs(self, verbose=1):
        self.dist_from_source = [self.n + 1] * self.n

        Q = deque()
        Q.append(self.source)

        self.dist_from_source[self.source] = 0

        while len(Q) > 0:
            node = Q.popleft()
            for e in self.graph[node]:
                if not e.get_capacity(node) != 0 or e.get_cost(node) != 0:
                    continue
                n_node = e.get_oposite_side(node)

                if self.dist_from_source[n_node] > self.n:
                    self.dist_from_source[n_node] = self.dist_from_source[node]+1
                    Q.append(n_node)

    def calculate(self):
        any_path, potentials = Bellman_Ford(
            self.n, self.edges, self.source, self.sink)
        print(potentials)
        if not any_path:
            return 0, 0

        self.apply_potentials(potentials)
        total_flow = 0
        total_cost = 0

        while True:
            any_path, potentials = Dijkstra(
                self.n, self.graph, self.source, self.sink)
            # print(any_path)
            if not any_path:
                break

            self.apply_potentials(potentials)
            while True:
                self.dinitz_bfs()
                # print('here')
                if self.dist_from_source[self.sink] >= self.n:
                    break
            current_flow = self.dinitz_dfs()
            total_flow += current_flow
            total_cost += current_flow*self.sink_potential
        return total_flow, total_cost


def solve(notes, verbose=1):

    graph, edges = build_graph(notes)
    source = len(graph)

    if verbose >= 3:
        print("graph built")

    graph, edges, duplicates = prepare_network(edges, graph, source, source+1)
    sinks_idx = source+len(duplicates)+1
    fst_sink, scn_sink, trd_sink, fth_sink = sinks_idx, sinks_idx + \
        1, sinks_idx+2, sinks_idx+3

    graph[fst_sink] = []
    graph[scn_sink] = []
    graph[trd_sink] = []
    graph[fth_sink] = []

    if verbose >= 3:
        print("creating sinks")

    for i in duplicates:
        e1 = Edge(i, fst_sink, 0, 1)
        e2 = Edge(i, scn_sink, 0, 1)
        e3 = Edge(i, trd_sink, 0, 1)
        e4 = Edge(i, fth_sink, 0, 1)

        graph[i].extend([e1, e2, e3, e4])
        edges.extend([e1, e2, e3, e4])

        graph[fst_sink].append(e1)
        graph[scn_sink].append(e2)
        graph[trd_sink].append(e3)
        graph[fth_sink].append(e4)

    final_sink = sinks_idx + 4
    graph[final_sink] = []

    edges.append(Edge(fst_sink, final_sink, 0, 1))
    edges.append(Edge(scn_sink, final_sink, 0, 1))
    edges.append(Edge(trd_sink, final_sink, 0, 1))
    edges.append(Edge(fth_sink, final_sink, 0, 1))

    graph[fst_sink].append(edges[-4])
    graph[scn_sink].append(edges[-3])
    graph[trd_sink].append(edges[-2])
    graph[fth_sink].append(edges[-1])

    graph[final_sink].extend([edges[-4], edges[-3], edges[-2], edges[-1]])

    mcmf = MinCostMaxFlow(len(graph), source, final_sink, graph, edges)

    if verbose >= 2:
        print("Solving")

    max_flow, min_cost = mcmf.calculate()

    if verbose >= 1:
        print(f"max_flow: {max_flow}, min_cost: {min_cost}")

    return max_flow, abs(min_cost)


# solve([1, 2, 3, 4, 5], 3)

solve([9, 37, 31, 17, 9], 3)
