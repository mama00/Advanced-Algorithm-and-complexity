#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def ReadTree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def maximum_fun_at_root(tree, root, parent,DP):
    if DP[root]==0:
        if len(tree[root].children)==1 and root!=0:
            DP[root] = tree[root].weight
        else:
            m1 = tree[root].weight
            for subordinate in tree[root].children:
                if subordinate != parent:
                    for sub_subordinate in tree[subordinate].children:
                        if sub_subordinate != root:
                            m1 += maximum_fun_at_root(tree, sub_subordinate,subordinate, DP)
            m0 = 0
            for subordinate in tree[root].children:
                if subordinate != parent:
                    m0 += maximum_fun_at_root(tree, subordinate, root, DP)
            DP[root] = max(m1, m0)
    return DP[root]



def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)
    DP=[0]*size
    if size == 0:
        return 0
    return maximum_fun_at_root(tree,0,-1,DP)
    


def main():
    tree = ReadTree();
    weight = MaxWeightIndependentTreeSubset(tree);
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
