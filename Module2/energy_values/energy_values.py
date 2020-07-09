# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)

def SelectPivotElement(a, used_rows, used_columns,b):

    pivot_element = Position(0, 0)
    while used_columns[pivot_element.column]:
        pivot_element.column += 1
        
    while pivot_element.row<len(a) and (used_rows[pivot_element.row]  or a[pivot_element.row][pivot_element.column]==0):
        pivot_element.row += 1
        
    if pivot_element.row==len(a):
        pivot_element.row=0
        while used_columns[pivot_element.row]:
            pivot_element.row += 1
        return pivot_element

            
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
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])

if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)
