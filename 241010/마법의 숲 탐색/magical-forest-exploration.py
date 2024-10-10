from collections import deque

dx=[-1,0,1,0]
dy=[0,-1,0,1]

n,m,K=map(int,input().split())
a=[[0]*m for _ in range(n)]
ans=0

# 출구 위치
def getExit(x,y,d):
    if d==0:
        return [x-1,y]
    elif d==1:
        return [x,y+1]
    elif d==2:
        return [x+1,y]
    else:
        return [x,y-1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<m:
        return True
    return False

# 골렘이 어떤 좌표로 이동 가능한 상태인지 확인
def check(x,y):
    if not inBoard(x,y): # 좌표가 보드 밖에 위치하면
        if x<n and 0<=y<m: # 좌표가 위쪽이 뚫린 바구니 같은 공간에 있는지
            return True
    else: # 좌표가 보드 안에 위치하면
        if a[x][y]==0: # 다른 골렘이 없는지
            return True
    return False

# 골렘 이동
def move(c,d,no):
    global a

    x,y=-2,c # 골렘 내 중앙의 정령 위치. 보드 맨 위에서 두 칸 위인 x==-2 지점부터 내려온다.
    while True:
        # 골렘 수직 이동
        if check(x+2,y) and check(x+1,y-1) and check(x+1,y+1):
            x+=1
        # 골렘 왼쪽 이동
        elif check(x+1,y-1) and check(x-1,y-1) and check(x,y-2) and check(x+1,y-2) and check(x+2,y-1):
            x+=1
            y-=1
            d=(d-1)%4
        # 골렘 오른쪽 이동
        elif check(x+1,y+1) and check(x-1,y+1) and check(x,y+2) and check(x+1,y+2) and check(x+2,y+1):
            x+=1
            y+=1
            d=(d+1)%4
        else:
            break

    # 골렘 지도에 표시
    if not inBoard(x, y) or not inBoard(x + 1, y) or not inBoard(x-1,y) or not inBoard(x,y+1) or not inBoard(x,y-1):
        return [False, -1, -1]
    else:
        a[x][y]=a[x+1][y]=a[x-1][y]=a[x][y+1]=a[x][y-1]=no
        ex, ey = getExit(x, y, d)# 출구 위치
        a[ex][ey]=-no
        return [True,x,y]

# 정령 이동
def bfs(sx,sy,no):
    global ans

    cand=[]
    q=deque()
    q.append((sx,sy))
    visit=[[False]*m for _ in range(n)]
    visit[sx][sy]=True

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny] or a[nx][ny]==0:
                continue
            # 절댓값이 같은 칸으로 움직이거나, 출구 칸에서 다른 칸으로 이동 가능
            if abs(a[x][y])==abs(a[nx][ny]) or (a[x][y]<0 and abs(a[nx][ny])!=abs(a[x][y])):
                q.append((nx,ny))
                visit[nx][ny]=True
                cand.append(nx)

    cand.sort(reverse=True)
    point=cand[0]+1
    return point

for no in range(1,K+1):
    c,d=map(int,input().split())
    c-=1

    # 골렘 이동
    res=move(c,d,no)
    inBound,x,y=res

    # 골렘 몸 일부가 숲 벗어나있는지 확인
    if inBound:
        # 정령 이동
        ans+=bfs(x,y,no)
    else:
        # 숲 초기화
        a=[[0]*m for _ in range(n)]

print(ans)