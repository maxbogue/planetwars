from math import sqrt

def euclidean_distance(x, y):
    return sqrt(x * x + y * y)

def dist(p1, p2):
    return euclidean_distance(p1.x - p2.x, p1.y - p2.y)

def partition(predicate, ls):
    yes = []
    no = []
    for e in ls:
        if predicate(e):
            yes.append(e)
        else:
            no.append(e)
    return yes, no
