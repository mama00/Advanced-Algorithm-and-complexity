# python3
import subprocess
n, m = list(map(int, input().split()))
A = []
for i in range(n):
  A += [list(map(int, input().split()))]
b = list(map(int, input().split()))
clauses=[]

def get_not_null(expression):
      not_null_variables=[]
      index_not_null_variables=[]
      for i in range(len(expression)):
            if expression[i]!=0:
                  not_null_variables.append(expression[i])
                  index_not_null_variables.append(i)
      return not_null_variables,index_not_null_variables
    
def get_values_variables(n):
      result=[]
      for i in range(2**n):
            st='{0:0'+str(n)+'b}'
            result.append([int(char) for char in st.format(i)])
      return result

def add_clauses(index_not_null_variables,value):
      clause=[]
      for i in range(len(value)):
            if value[i]==0:
                  clause.append((index_not_null_variables[i]+1))
            else:
                  clause.append(-(index_not_null_variables[i]+1))
      clause.append(0)
      clauses.append(clause)
      
def printEquisatisfiableSatFormula():
    for i in range(n):
          not_null_variables,index_not_null_variables=get_not_null(A[i])
          if len(not_null_variables)>0:
            for value in get_values_variables(len(not_null_variables)):
                    result=0
                    for j in range(len(not_null_variables)):
                        result+=not_null_variables[j]*value[j]
                    if not result<=b[i]:
                        add_clauses(index_not_null_variables,value)
          elif b[i]<0:
              clauses.append([1,0])
              clauses.append([-1,0])
              break

    if len(clauses)==0:
        print('1 1')
        print('1 -1 0')
    else:
        print(len(clauses),m)
        for clause in clauses:
            for var in clause:
                    print(var,end=' ')
            print()
    # with open('temp.sat','w') as file:
    #     if len(clauses)==0:
    #         file.write('1 1\n')
    #         file.write('1 -1 0')
    #     else:
    #         file.write('p cnf '+ str(m)+' ' +str(len(clauses))+' '+'\n')
    #         for clause in clauses:
    #             for var in clause:
    #                 file.write(str(var)+' ')
    #             file.write('\n')
    # subprocess.run(['minisat','temp.sat','res.sat'])

printEquisatisfiableSatFormula()
