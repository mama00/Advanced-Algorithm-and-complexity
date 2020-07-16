# python3
import itertools
INF = 10 ** 9

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph


def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))
    
    
def get_subsets_of_size(s,n):
    return [x+(0,) for x in itertools.combinations(range(1,n),s-1)]

#get the numerical value of a subset exp:[1,2,4]=2^1 + 2^2 +2 ^4=22 corresponding to the subset
#where whe choose the first vertex ,the second one and the forth one
def get_numeric_value(subset):
    value=0
    for x in subset:
        value+=2**x
    return value
    
    
#handling the Dynamic programming logic    
def optimal_path(graph):
    n = len(graph)
    DP=[[INF]*n for _ in range(2**n)]# maxtrix where i is the subset and j the end of the path
    # starting from one and going to one viewing only one is cost 0
    DP[1][0]=0
    #looping trought all subset
    for s in range(2,n+1):
        for subset in get_subsets_of_size(s,n):
            numeric_subset=get_numeric_value(subset)#transforming subset in number
            DP[numeric_subset][0]=INF
            for i in subset:
                if i!=0:
                    minimum=INF
                    for j in subset:
                        if j!=i:
                            minimum=min(minimum,DP[numeric_subset^(1<<i)][j]+graph[i][j])
                    DP[numeric_subset][i]=minimum
    result=INF
    for i in range(0,n):
        if i!=0:
            result=min(result,DP[2**n-1][i]+graph[i][0])
    edges=[]
    if result==INF:
        return -1,edges
    backtrack(DP,edges,2**n-1,0,graph)#backtracking to see when vertices get choosed
    return result,edges

#this function construct the set of vertices corresponding to the binary value of subset
def construct_set(binary):
    r=[]
    for i in range(len(binary)):
        if binary[i]=='1':
            r.append(i)
    return r
#this function backtrack the result to get the vertices in order
def backtrack(DP,edges,numeric_subset,to,graph):
    subset=bin(numeric_subset).split('b')[1][::-1]
    subset=construct_set(subset)
    index=0
    mini=INF
    for i in subset:
        if i != to:
            if DP[numeric_subset][i]+graph[i][to]<mini:
                index=i
                mini=DP[numeric_subset][i]+graph[i][to]
    edges.insert(0,index+1)
    if len(DP[0])!=len(edges):
        backtrack(DP,edges,numeric_subset^(1<<index),index,graph)
    else:
        return

if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))
