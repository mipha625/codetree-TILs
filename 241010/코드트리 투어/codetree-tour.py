#코드트리 랜드 건설
def c1(arr):
    n = arr.popleft()
    m = arr.popleft()
    graph = [[] * n for _ in range(n)]
    for i in range(0, 3 * m, 3):
        s, e, c = arr[i], arr[i+1], arr[i+2]
        graph[s].append((e, c))
        if s != e:
            graph[e].append((s, c))
    return n, m, graph

#최단거리 알고리즘: 다익스트라
## 최단거리 구하는 경우: 1) 명령어 100 2) 명령어 500
def dijkstra(start):
    global n, graph, distance
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

#(4) 최적의 여행 상품 판매
class node:
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        
    def __lt__(self, other):
        if self.A > other.A:
            return True
        elif self.A == other.A:
            if self.B < other.B:
                return self.B < other.B
            elif self.B == other.B:
                return self.C < other.C
            else:
                return False
        else:
            return False
    
    def __str__(self):
        return '{} {} {} {}'.format(self.A, self.B, self.C, self.D)



from collections import deque
import heapq
INF = int(1e9)
Q = int(input())

commands = deque()
tripq = []
result = []

for _ in range(Q):
    commands = deque(map(int, input().split()))
    com = commands.popleft() #명령어 번호 확인
    
    if com == 100: #코드트리 랜드 건설
        n, m, graph = c1(commands)
        distance = [INF] * n #다익스트라 돌릴 때마다 새로 필요
        dijkstra(0)
    elif com == 200: #(2) 여행 상품 생성
        _id, _revenue, _dest = commands
        heapq.heappush(tripq, (-_revenue + distance[_dest], _id, _revenue, distance[_dest], _dest))
    elif com == 300: #(3) 여행 상품 취소
        tempq = []
        while tripq:
            q = heapq.heappop(tripq)
            if q[1] != commands[0]: #삭제하지 않을 id
                heapq.heappush(tempq, q)
        tripq = [items[:] for items in tempq] #다시 돌려놓기
    elif com == 400: #(4) 최적의 여행 상품 판매
        length = len(tripq)
        tempq = []
        while tripq:
            q = heapq.heappop(tripq)
            if q[3] >= INF or q[0] > 0: #출발지로부터 dest에 도달하는 것 불가 or cost > revenue여서 이득 X
                heapq.heappush(tempq, q)
                continue
            else:
                result.append(q[1])
                break
        if len(tempq) == length: #하나도 빠진 게 없다면
            result.append(-1)
            tripq = [items[:] for items in tempq]
        else:
            while tempq:
                heapq.heappush(tripq, heapq.heappop(tempq))
    elif com == 500: #(5) 여행 상품의 출발지 변경
        distance = [INF] * n #다익스트라 돌릴 때마다 새로 필요
        dijkstra(commands[0]) #새로운 출발지로 distance 다시 구함
        tempq = []
        while tripq:
            q = heapq.heappop(tripq) #q[1]: _id, q[2]: _revenue, q[4]: _dest
            heapq.heappush(tempq, (-q[2] + distance[q[4]], q[1], q[2], distance[q[4]], q[4]))
        tripq = [items[:] for items in tempq]                       


for i in result:
    print(i)