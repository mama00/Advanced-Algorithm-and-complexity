# python3
import sys
import threading
from collections import deque
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]

# This solution tries all possible 2^n variable assignments.
# It is too slow to pass the problem.
# Implement a more efficient algorithm here.
def construct_graph(n,m):
    graph={}
    reversed_graph={}
    for i in range(1,n+1):
        graph[i]=[]
        graph[-i]=[]
        reversed_graph[i]=[]
        reversed_graph[-i]=[]
    for clause in clauses:
        graph[-clause[0]]+=[clause[1]]
        graph[-clause[1]]+=[clause[0]]
        reversed_graph[clause[1]]+=[-clause[0]]
        reversed_graph[clause[0]]+=[-clause[1]]
    return graph,reversed_graph
    
    
#for the first dfs call
def dfs(graph,node,finished_order,viewed):
    viewed[node]=1
    for child_node in graph.get(node,[]):
        if viewed.get(child_node,None)==None:
            dfs(graph,child_node,finished_order,viewed)
    finished_order.append(node)

#for the second dfs call 
def dfs_sub(graph,node,connected,viewed):
    viewed[node]=1
    if -node in connected:
        return -1
    connected.add(node)
    for child_node in graph.get(node,[]):
        if viewed.get(child_node,None)==None:
            is_invalid=dfs_sub(graph,child_node,connected,viewed)
            if is_invalid==-1:
                return -1
    
#main function 
def compute_strongly_connected_component(graph,reversed_graph):
    viewed={}
    finished_order=deque()
    list_of_conencted_component=deque()
    for node in reversed_graph:
        if viewed.get(node,None)==None:
            dfs(reversed_graph,node,finished_order,viewed)
    viewed={}
    while finished_order:
        node=finished_order.pop()
        if viewed.get(node,None)==None:
            connected=set()
            is_invalid=dfs_sub(graph,node,connected,viewed)
            if is_invalid==-1:
                return -1
            list_of_conencted_component.append(connected)
    return list_of_conencted_component
        
    
    
def isSatisfiable():
    graph,reversed_graph=construct_graph(n,m)
    result=compute_strongly_connected_component(graph,reversed_graph)
    if result==-1:
        return None
    else:
        variables=[-1]*(n)
        while result:
            component = result.popleft()
            for var in component:
                if variables[abs(var)-1]==-1:
                    if var>0:
                        variables[abs(var)-1]=0
                    else:
                        variables[abs(var)-1]=1
        return variables

def cc():        
    result = isSatisfiable()
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE");
        print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
        
if __name__ == '__main__':
    threading.Thread(target=cc).start()

