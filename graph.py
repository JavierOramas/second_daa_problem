from utils import cond_compare
import numpy as np
import heapq


class Edge:
    def __init__(self, source, dest, cost, capacity):
        self.source = source
        self.dest = dest
        self.capacity = capacity
        self.cost = cost
        self.flow = 0

    def __eq__(self, o):
        return self.source == o.source and self.dest == o.dest

    def __hash__(self):
        return hash((self.source, self.dest))

    def push_flow(self, side, flow):
        if side == self.source:
            self.flow += flow
        else:
            self.flow -= flow

    def get_oposite_side(self, node):
        if self.source == node:
            return self.dest
        return self.source

    def get_capacity(self, side):
        if side == self.source:
            return self.capacity - self.flow
        else:
            return self.flow

    def get_cost(self, side):
        if side == self.source:
            return self.cost
        return -self.cost


def build_graph(notes, verbose=1):

    # dict with node: List of edges adjacent to node
    graph = {}
    # list of all edges
    edges = []

    for idx, note in enumerate(notes):
        graph[idx] = []
        for idx2, note2 in enumerate(notes):
            if idx2 > idx and cond_compare(note, note2):
                if verbose >= 1:
                    print(f"adding edge {note} -> {note2}")
                if not idx2 in graph:
                    graph[idx2] = []
                e = Edge(idx, idx2, -1, 1)
                graph[idx].append(e)
                graph[idx2].append(e)
                edges.append(e)
    return graph, edges


def Bellman_Ford(n, edges, source, sink):
    dist = [np.inf] * n
    dist[source] = 0

    for _ in range(n):
        for e in edges:
            dist[e.dest] = min(dist[e.dest], dist[e.source] + e.cost)

    if dist[sink] >= np.inf:
        return False, dist
    return True, dist


def prepare_network(edges, graph, source, index_dup):

    graph[source] = []
    duplicates = []

    for i in range(source):
        if i != source:
            dup_edge = Edge(i, index_dup, 0, 1)
            dest_dup = list(filter(lambda n: n.source == i, graph[i]))

            graph[index_dup] = [Edge(index_dup, k.dest, -1, 1)
                                for k in dest_dup] + [dup_edge]

            graph[i] = list(filter(lambda n: n.source !=
                            i, graph[i])) + [dup_edge]

            for j in edges:
                if j in dest_dup:
                    edges.remove(j)

            edges.append(dup_edge)
            edges.extend(graph[index_dup])

            duplicates.append(index_dup)
            index_dup += 1

            e = Edge(source, i, -1, 1)
            graph[source].append(e)
            graph[i].append(e)
            edges.append(e)

    return graph, edges, duplicates


def Dijkstra(n, graph, source, sink):
    # print(source, sink)
    dist = [np.inf] * n
    mark = [False] * n

    dist[source] = 0
    Q = []
    heapq.heappush(Q, (0, source))

    while (len(Q) > 0):
        _, node = heapq.heappop(Q)

        if mark[node]:
            continue

        mark[node] = True

        for e in graph[node]:
            if not e.get_capacity(node) != 0:
                continue

            n_node = e.get_oposite_side(node)

            if dist[n_node] > dist[node] + e.get_cost(node):
                dist[n_node] = dist[node] + e.get_cost(node)
                heapq.heappush(Q, (dist[n_node], n_node))

    if dist[sink] >= np.inf:
        return False, dist

    return True, dist
