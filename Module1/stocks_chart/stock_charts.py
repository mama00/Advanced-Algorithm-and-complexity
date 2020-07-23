# python3
graphs=[]
class StockCharts:
    def read_data(self):
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data

    def write_response(self, result):
        print(result)
    def construct_graph(self,stock_data,n):
        graph=[[]]*(2*n+2)
        for i in range(2*n+2):
            if i==0:
                graph[i]=[(0,0)]+[(1,0)]*(n) +[(0,0)]*(n+1) #adding edge from source to stocks except sink
            else:
                graph[i]=[(0,0)]*(2*n+2)
        for i in range(len(stock_data)):
            graph[i+n+1][2*n+1]=(1,0)#adding edge from stock to sink
            for j in range(len(stock_data)):
                if i!=j:
                    if self.is_smaller(i,j,stock_data):
                        graph[i+1][n+j+1]=(1,0)
        
        return graph
        
    def BFS(self,graph,n):
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
                        if key==2*+1:                        
                            child=key
                            while(parent[child]!=-1):
                                list_edge_in_augmenting_path.insert(0,(parent[child],child))
                                child=parent[child]
                            return (list_edge_in_augmenting_path)
        return -1

    def DFS(self,graph,n):
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
                    if key==2*n+1:
                        child=key
                        while(parent[child]!=-1):
                                list_edge_in_augmenting_path.insert(0,(parent[child],child))
                                child=parent[child]
                        return list_edge_in_augmenting_path
        return -1

        
    def is_smaller(self,stock,i,stock_data):
        result=True
        if stock_data[i][0]==stock_data[stock][0]:
            return False

        for j in range(len(stock_data[i])):
            if stock_data[i][j]<=stock_data[stock][j]:
                return False
        return True
    
    def add_flow(self,graph,list_edge_in_augmenting_path):
        for value in list_edge_in_augmenting_path:
            i,j=value
            graph[i][j]=(graph[i][j][0],graph[i][j][1]+1)
            graph[j][i]=(graph[j][i][0],graph[j][i][1]-1)
            
        
    def min_charts(self, stock_data):
        flow=0
        n=len(stock_data)        
        graph=self.construct_graph(stock_data,n)
        list_edge_in_augmenting_path=[]
        while True:
            list_edge_in_augmenting_path=self.DFS(graph,n)
            if list_edge_in_augmenting_path==-1:
                break
            else:
                self.add_flow(graph,list_edge_in_augmenting_path)
                flow+=1
        return n-flow
            
                 

    def solve(self):
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)
if __name__ == '__main__':
    stock_charts = StockCharts()
    stock_charts.solve()
