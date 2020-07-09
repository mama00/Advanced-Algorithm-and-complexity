# python3
import itertools
n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

# This solution prints a simple satisfiable formula
# and passes about half of the tests.
# Change this function to solve the problem.
clauses=[]
def num_var(vertex,color):
    return (vertex-1)*3+color

def only_one_is_true(variables):
    clauses.append(variables+[0])
    for var1,var2 in itertools.combinations(variables,2):
        clauses.append([-var1,-var2,0])
#each vertex has to have a color
def each_vertex_have_color():
    for vertex in range(1,n+1):
        clauses.append([num_var(vertex,k) for k in range(1,4)]+[0])

# vertices connected by an edge have different color
def each_neighbor_must_have_different_color():
    for edge in edges:
        for k in range(1,4):
            clauses.append([-num_var(edge[0],k),-num_var(edge[1],k),0])
def printEquisatisfiableSatFormula():
    each_vertex_have_color()
    each_neighbor_must_have_different_color()
    print(len(clauses),' ',n*3)
    for clause in clauses:
        for var in clause:
            print(var,end=" ")
        print('')

printEquisatisfiableSatFormula()
