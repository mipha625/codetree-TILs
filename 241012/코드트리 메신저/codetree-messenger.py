from collections import defaultdict
import sys
input = sys.stdin.readline

N, Q = map(int, input().split())
parents = [0]*(N+1)
children = [list() for _ in range(N+1)]
auth = [0]*(N+1)
surplus_auth = [[0]*21 for _ in range(N+1)]
alarms = [1]*(N+1)

def init() :
    global parents, auth
    q = list(map(int, input().split()))
    for i in range(N) :
        parents[i+1] = q[i+1]
        auth[i+1] = min(20, q[i+1+N])
    for i in range(1, N+1) :
        children[parents[i]].append(i)
        power, idx = auth[i], i
        while power > -1 :
            surplus_auth[idx][power] += 1
            power -= 1
            if idx == parents[idx] :
                break
            idx = parents[idx]

def update(idx) :
    cnt = 0
    surplus_auth[idx] = [0]*21
    surplus_auth[idx][auth[idx]] += 1
    for child in children[idx] :
        if not alarms[child] :
            continue
        for i, val in enumerate(surplus_auth[child][1:]) :
            surplus_auth[idx][i] += val
    if idx != parents[idx] :
        update(parents[idx])

def change_alam(c) :
    alarms[c] = 1 - alarms[c]
    update(parents[c])
    
def change_power(c, power) :
    auth[c] = min(20, power)
    update(c)


def change_parents(c1, c2) :
    p1, p2 = parents[c1], parents[c2]
    if p1 == p2 :
        return

    parents[c1], parents[c2] = parents[c2], parents[c1]
    children[p1].remove(c1)
    children[p1].append(c2)
    children[p2].remove(c2)
    children[p2].append(c1)

    update(p1)
    update(p2)


def check(c) :
    print(sum(surplus_auth[c]) - 1)

init()
for _ in range(Q-1) :
    query, *body = map(int, input().split())
    if query == 200 :
        c = body[0]
        change_alam(c)
    elif query == 300 :
        c, power = body
        change_power(c, power)
    elif query == 400 :
        c1, c2 = body
        change_parents(c1, c2)
    else :
        c = body[0]
        check(c)