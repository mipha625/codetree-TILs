from collections import deque

#회전 함수
class rotate:  
    def rotate_degree(self, arr, sx, sy, degree):
        self.arr = arr #회전이 일어날 객체
        self.sx = sx #회전 시작되는 row 위치
        self.sy = sy #회전 시작되는 col 위치
        
        N = len(arr)
        new_arr = [[0] * N for _ in range(N)]
        for x in range(sx, sx + 3):
            for y in range(sy, sy + 3):
                ox, oy = x - sx, y - sy #(0,0) 초기화
                if degree == 90:
                    rx, ry = oy, 3 - 1 - ox
                elif degree == 180:
                    rx, ry = 3 - 1 - ox, 3 - 1 - oy
                elif degree == 270:
                    rx, ry = 3 - 1 - oy, ox
                new_arr[sx + rx][sy + ry] = arr[x][y]
        
        for x in range(sx, sx + 3):
            for y in range(sy, sy + 3):
                arr[x][y] = new_arr[x][y]
        
        new_arr = [[0] * N for _ in range(N)]
        
        return arr


class search:

    def dfs(self, arr, x, y, num):
        if x <= -1 or x >= 5 or y <= -1 or y >= 5:
            return False
        if arr[x][y] == num:
            arr[x][y] = 0
            self.cnt += 1
            self.temp.append([x, y])
            self.dfs(arr, x - 1, y, num)
            self.dfs(arr, x + 1 , y, num)
            self.dfs(arr, x, y - 1, num)
            self.dfs(arr, x, y + 1, num)
            return True
        return False
        
    def find(self, arr):
        self.total = 0
        self.cnt = 0
        self.num = 0
        self.idx = 0
        self.temp = []
        
        for i in range(5):
            for j in range(5):
                if arr[i][j] != 0:
                    self.num = arr[i][j]
                if self.dfs(arr, i, j, self.num) == True:
                    if self.cnt >= 3:
                        self.total += self.cnt
                        self.cnt = 0 #초기화
                    else: #cnt < 3
                        while self.cnt > 0:
                            self.temp.pop()
                            self.cnt -= 1
        return self.total, self.temp
        
def main():
    K, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(5)]
    wall = deque(map(int , input().split()))
    rotator = rotate()     
    searcher = search()

    while K > 0: #턴이 0보다 클 때까지
        #탐사 진행 (회전 시도)

        result = 0
        rotate_li = []
        total_li = []
        temp_li = []  

        for d in range(90, 271, 90):
            for j in range(3):
                for i in range(3):
                    arr1 = [items[:] for items in arr]
                    rotate_li.append(rotator.rotate_degree(arr1, i, j, d))
                    
        for i in range(27):
            total, temp = searcher.find([items[:] for items in rotate_li[i]])
            total_li.append(total)
            temp_li.append(temp)
            
        max_idx = total_li.index(max(total_li))
        max_total = total_li[max_idx]
        
        if max_total == 0: #발견된 유물이 없다면 다음 턴으로 이동
            K -= 1
            continue
        
        #발견된 유물이 있다면
        result += max_total #한 턴 내에서 발굴한 유물 개수 계속 업데이트
        max_arr = rotate_li[max_idx]
        max_temp = sorted(temp_li[max_idx], key = lambda x: (x[1], -x[0]))

        #선정된 matrix 내에서 계속 시도
        while True:
            arr = max_arr
            
            if max_total == 0: #3개 연속으로 붙어있는 유적이 없을 때까지
                break

            for i, j in max_temp:
                new_val = wall.popleft() #새로운 값 채워넣기
                arr[i][j] = new_val
                
            #유물 연쇄 획득 확인
            max_total, max_temp = searcher.find([items[:] for items in arr])
            result += max_total
            max_temp.sort(key = lambda x: (x[1], -x[0]))
        
        if result != 0:       
            print(result, end = ' ')
        K -= 1

if __name__ == '__main__':
    main()