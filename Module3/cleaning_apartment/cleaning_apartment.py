# python3
import itertools
import subprocess
n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

# This solution prints a simple satisfiable formula
# and passes about half of the tests.
# Change this function to solve the problem.


clauses=[]

def only_one_is_true(literals):
    clauses.append(literals+[0])
    for pair1,pair2 in itertools.combinations(literals, 2):
        clauses.append([-pair1,-pair2,0])

def num_var(vertex,position):
    return (vertex-1)*n+position

def exist_an_edge_between(i,j):
    if [i,j] in edges or [j,i] in edges:
        return True
    return False
        
#each vertex appear only one in a Hamilton Path
def each_vertex_appear_exactly_once_in_a_path():
    for vertex in range(1,n+1):
        only_one_is_true([num_var(vertex,pos) for pos in range(1,n+1)])
        
#vertices occupy only one position in Hamilton Path        
def vertices_occupy_exactly_one_position():
    for pos in range(1,n+1):
        only_one_is_true([num_var(vertex,pos) for vertex in range(1,n+1)])
        
#if not adjacent in graph than cant be adjacent in Hamilton path
def if_not_adjacent_in_graph_not_adjacent_in_path():
    for vertex1,vertex2 in itertools.product(range(1,n+1),repeat=2):
        if vertex1!=vertex2 and not exist_an_edge_between(vertex1,vertex2):
            for k in range(1,n):
                clauses.append([-num_var(vertex1,k),-num_var(vertex2,k+1),0])
        

def printEquisatisfiableSatFormula():
    each_vertex_appear_exactly_once_in_a_path()
    vertices_occupy_exactly_one_position()
    if_not_adjacent_in_graph_not_adjacent_in_path()    
    with open('temp.sat','w') as file:
        file.write(str(len(clauses))+' '+str(n*n)+'\n')
        for clause in clauses:
            for var in clause:
                file.write(str(var)+' ')
            file.write('\n')
    subprocess.run(['minisat','temp.sat','res.sat'])
printEquisatisfiableSatFormula()
