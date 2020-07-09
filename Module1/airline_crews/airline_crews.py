# python3
class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))
        
    def construct_graph(self,adj_matrix,n,m):
        graph = []*(m+n+2)
        for index in range(m+n+2):
            graph.append([(0,0)]*(m+n+2))
        for index in range(m):
            graph[0][index+1]=(1,0)
        for index in range(n):
            graph[m+1+index][m+n+1]=(1,0)
        for key_flight in range(n):
            for key_crew in range(m):
                if adj_matrix[key_flight][key_crew]==1:
                    graph[key_crew+1][key_flight+m+1]=(1,0)
        return graph    
    def BFS(self,graph,n,m):
        queue=[(0,-1)]
        viewed=[]
        list_edge_in_augmenting_path=[]
        parent={0:-1}
        while queue!=[]:
                vertex,id_e=queue.pop(0)
                viewed.append(vertex)
                for key,edge in enumerate(graph[vertex]):
                    capacity,flow=edge
                    if capacity-flow>0 and key not in viewed:
                        queue.append((key, vertex))
                        parent[key]=vertex
                        if key==m+n+1:                        
                            child=key
                            while(parent[child]!=-1):
                                list_edge_in_augmenting_path.insert(0,(parent[child],child))
                                child=parent[child]
                            return (list_edge_in_augmenting_path)
        return -1

    def DFS(self,graph,n,m):
        viewed=[]
        stack=[(-1,0)]
        list_edge_in_augmenting_path=[]
        parent={0:-1}
        while stack!=[]:
            id_e,vertex=stack.pop(0)
            viewed.append(vertex)
            for key,edge in enumerate(graph[vertex]):
                capacity,flow=edge
                if capacity-flow>0 and key not in viewed:
                    stack.insert(0, (vertex,key))
                    parent[key]=vertex
                    if key==m+n+1:
                        child=key
                        while(parent[child]!=-1):
                                list_edge_in_augmenting_path.insert(0,(parent[child],child))
                                child=parent[child]
                        return list_edge_in_augmenting_path
        return -1
                
    def construct_matching(self,graph,n,m):
        matching=[-1]*n
        for key_flight in range(n):
            for key_crew in range(m):
                if graph[key_crew+1][1+m+key_flight][1]==1:
                    matching[key_flight]=key_crew
                    break
        return matching
    
    def add_flow(self,graph,list_edge_in_augmenting_path):
        for value in list_edge_in_augmenting_path:
            i,j=value
            graph[i][j]=(graph[i][j][0],graph[i][j][1]+1)
            graph[j][i]=(graph[j][i][0],graph[j][i][1]-1)
    def find_matching(self, adj_matrix):
        # Replace this code with an algorithm that finds the maximum
        # matching correctly in all cases.
        n = len(adj_matrix)
        m = len(adj_matrix[0])
        list_edge_in_augmenting_path=[]
        graph = self.construct_graph(adj_matrix,n,m)
        while True:
            list_edge_in_augmenting_path=self.DFS(graph,n,m)
            if list_edge_in_augmenting_path==-1:
                break
            else:
                self.add_flow(graph,list_edge_in_augmenting_path)
                 
        return self.construct_matching(graph,n,m)

    def solve(self):
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()
