# python3
from sys import stdin

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row


def SelectPivotElement(a, used_rows, used_columns,b):
    pivot_element = Position(0, 0)
    while used_columns[pivot_element.column]:
        pivot_element.column += 1
        
    while pivot_element.row<len(a) and (used_rows[pivot_element.row]  or a[pivot_element.row][pivot_element.column]==0):
        pivot_element.row += 1
        
    if pivot_element.row==len(a):
        return -1


    return pivot_element

def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def ProcessPivotElement(a, b, pivot_element):
    row_add=[]
    b_add=0
    DivideRowByValue(a,b,pivot_element.row,a[pivot_element.row][pivot_element.column])
    for row in range(len(a)):
        if row!=pivot_element.row:
            row_add=[x*(-a[row][pivot_element.column]) for x in a[pivot_element.row]]
            b_add=b[pivot_element.row]*(-a[row][pivot_element.column])
            AddRowToOtherRow(a,b,b_add,row_add,row)

def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

        
def DivideRowByValue(a,b,row,value):
    for key,v in enumerate(a[row]):
        a[row][key]/=value
    b[row]/=value
def AddRowToOtherRow(a,b,b_add,row_add,index_row_receive):
    for column,value in enumerate(row_add):
        a[index_row_receive][column]+=value
    b[index_row_receive]+=b_add
    
def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns,b)
        if pivot_element==-1:
              return -1
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b


def generate(base,size):
    list_subset=[]
    sub=[None]*len(base)
    generate_subset(list_subset,base,sub,0,size)
    return list_subset

def generate_subset(list_subset,base,subset,index,size):
    if index==len(base):
        tt=[x for x in subset if x != None]
        if len(tt)==size:
            list_subset.append(tt)
        return
    subset[index]=None
    generate_subset(list_subset, base,subset,index+1,size)
    subset[index]=base[index]
    generate_subset(list_subset,base,subset,index+1,size)
    
def construct_sub_matrix(rows,A,B,n,m):
      a=[]
      b=[]
      for row in rows:
            if row>n:
                  a.append([1 if k==row-n-1 else 0 for k in range(m)])
                  b.append(0)
            else:
                  a.append(A[row][:])
                  b.append(B[row])
      return (a,b)
    
def dotProduct(A,B):
      sum_v=0.0
      for index in range(len(A)):
            sum_v+=A[index]*B[index]
      return sum_v
    
def verifyResult(result,A,b):
      for key,rows in enumerate(A):
            if dotProduct(rows,result)>b[key]+1e-3:
                  return False
      for value in result:
            if value<-1e-3:
                  return False
      return True
      

def solve_diet_problem(n, m, A, b, c):  
  max_objective=float('-inf')
  result_final=[]
  is_bound=-1
  A.append([1]*m)
  b.append(1e9)
  list_subrows_size_m=generate(range(n+m+1),m)
  for subrows in list_subrows_size_m:
        selected_infinity=0
        if n in subrows:
              selected_infinity=1
        sub_A,sub_b=construct_sub_matrix(subrows,A,b,n,m)
        equation=Equation(sub_A,sub_b)
        result=SolveEquation(equation)
        if result!=-1:
          if verifyResult(result,A,b):
                if dotProduct(c,result)>max_objective:
                      result_final=result
                      max_objective=dotProduct(c,result)
                      if selected_infinity==1:
                        is_bound=1

                      else:
                        is_bound=0
  return (is_bound,result_final)

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, b, c)

if anst == -1:
  print("No solution")
if anst == 0:  
  print("Bounded solution")
  print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
  print("Infinity")
    
