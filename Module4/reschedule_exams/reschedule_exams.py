# python3

# Arguments:
#   * `n` - the number of vertices.
#   * `edges` - list of edges, each edge is a tuple (u, v), 1 <= u, v <= n.
#   * `colors` - list consisting of `n` characters, each belonging to the set {'R', 'G', 'B'}.
# Return value: 
#   * If there exists a proper recoloring, return value is a list containing new colors, similar to the `colors` argument.
#   * Otherwise, return value is None.

# python3
import sys
import threading
from collections import deque
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

def construct_graph(n,m,clauses):
    graph={}
    reversed_graph={}
    for i in range(1,(n*3+1)):
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
        

def get_colors_from_variables(variables):
    colors=''
    for i in range(0,len(variables)-2,3):
        for j in range(3):
            if variables[i+j]==1:
                if j==0:
                    colors+='R'
                elif j==1:
                    colors+='G'
                else:
                    colors+='B'
    return colors
            
    
    
def isSatisfiable(clauses,n,m):
    graph,reversed_graph=construct_graph(n,m,clauses)
    result=compute_strongly_connected_component(graph,reversed_graph)
    if result==-1:
        return None
    else:
        variables=[-1]*(n*3)
        while result:
            component = result.popleft()
            for var in component:
                if variables[abs(var)-1]==-1:
                    if var>0:
                        variables[abs(var)-1]=1
                    else:
                        variables[abs(var)-1]=0
        return get_colors_from_variables(variables)


def get_variable(vertice,color):
    if color=='R':
        return (vertice-1)*3+1
    elif color== 'G':
        return (vertice-1)*3+2
    else:
        return (vertice-1)*3+3
        
def construct_clauses(edges,colors):
    clauses=[]
    #all colors must change
    for key in range(len(colors[0])):
        clauses.append([-get_variable(key+1,colors[0][key]),-get_variable(key+1,colors[0][key])])
        #edge must have a color
        if colors[0][key]=='R':
            clauses.append([get_variable(key+1,'G'),get_variable(key+1,'B')])
        elif colors[0][key]=='G':
            clauses.append([get_variable(key+1,'R'),get_variable(key+1,'B')])
        else:
            clauses.append([get_variable(key+1,'G'),get_variable(key+1,'R')])
    #no friend are on same days
    for edge in edges:
        v1,v2=edge
        for color in 'RGB':
            clauses.append([-get_variable(v1,color),-get_variable(v2,color)])
    return clauses
     
    
def main():
    n, m = map(int, input().split())
    colors = input().split()
    edges = []
    for i in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))
    clauses=construct_clauses(edges,colors)
    new_colors = isSatisfiable(clauses,n,m)
    if new_colors is None:
        print("Impossible")
    else:
        print(''.join(new_colors))

main()
