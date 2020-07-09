#! python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph

def BFS(graph,from_,to):
    queue=[(from_,-1)]
    viewed=[]
    list_edge_in_augmenting_path=[]
    parent={}
    while queue!=[]:
            city,id_e=queue.pop(0)
            viewed.append(city)
            for edge_id in graph.get_ids(city):
                edge=graph.get_edge(edge_id)
                if edge.u==city and edge.v!=city and edge.v not in viewed and edge.capacity-edge.flow>0:
                    queue.append((edge.v,edge_id))
                    parent[edge_id]=id_e
                    if edge.v==to:                        
                        child=edge_id
                        list_edge_in_augmenting_path.append(child)
                        while(parent[child]!=-1):
                            list_edge_in_augmenting_path.append(parent[child])
                            child=parent[child]
                        return (viewed,list_edge_in_augmenting_path)
    return ([],[])

def max_flow(graph, from_, to):
    flow = 0
    while True:
        viewed,list_edge_in_augmenting_path=BFS(graph,from_,to)
        if viewed!=[]:
            min_capacity=float('inf')
            for edge in list_edge_in_augmenting_path:
                if graph.get_edge(edge).capacity-graph.get_edge(edge).flow<min_capacity:
                    min_capacity=graph.get_edge(edge).capacity-graph.get_edge(edge).flow
            for edge in list_edge_in_augmenting_path:
                graph.add_flow(edge,min_capacity)
            flow+=min_capacity
        else:
            break
    return flow


if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))
