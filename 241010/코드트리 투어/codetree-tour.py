from collections import deque
import heapq
INF = int(1e9)

def c1(arr):
    n = arr.popleft()
    m = arr.popleft()
    graph = [[] for _ in range(n)]
    for i in range(0, 3 * m, 3):
        s, e, c = arr[i], arr[i+1], arr[i+2]
        graph[s].append((e, c))
        if s != e:
            graph[e].append((s, c))
    return n, m, graph

def dijkstra(start):
    global n, graph, distance
    if distance_cache[start] is not None:
        distance[:] = distance_cache[start][:]
        return
    q = []
    heapq.heappush(q, (0, start))
    distance[start] = 0
    while q:
        dist, now = heapq.heappop(q)
        if distance[now] < dist:
            continue
        for i in graph[now]:
            cost = dist + i[1]
            if cost < distance[i[0]]:
                distance[i[0]] = cost
                heapq.heappush(q, (cost, i[0]))
    distance_cache[start] = distance[:]

def lazy_delete_check():
    while tripq and deleted_trip[tripq[0][1]]:
        heapq.heappop(tripq)

Q = int(input())
commands = deque()
tripq = []
deleted_trip = {}
result = []

distance_cache = {}
for _ in range(Q):
    commands = deque(map(int, input().split()))
    com = commands.popleft()

    if com == 100: #코드트리 랜드 건설
        n, m, graph = c1(commands)
        distance = [INF] * n
        distance_cache = [None] * n
        deleted_trip = {}
        dijkstra(0)

    elif com == 200: #여행 상품 생성
        _id, _revenue, _dest = commands
        heapq.heappush(tripq, (-_revenue + distance[_dest], _id, _revenue, distance[_dest], _dest))
        deleted_trip[_id] = False

    elif com == 300: #여행 상품 취소
        deleted_trip[commands[0]] = True

    elif com == 400: #최적의 여행 상품 판매
        lazy_delete_check()
        if tripq and tripq[0][3] < INF and tripq[0][0] <= 0:
            result.append(heapq.heappop(tripq)[1])
        else:
            result.append(-1)

    elif com == 500: #여행 상품 출발지 변경
        new_start = commands[0]
        distance = [INF] * n
        dijkstra(new_start)
        new_tripq = []
        while tripq:
            q = heapq.heappop(tripq)
            if not deleted_trip[q[1]]:
                heapq.heappush(new_tripq, (-q[2] + distance[q[4]], q[1], q[2], distance[q[4]], q[4]))
        tripq = new_tripq

for i in result:
    print(i)