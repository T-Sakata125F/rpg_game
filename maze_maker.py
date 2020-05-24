import random

class maze_maker:
    """
    ダンジョンを自動生成する
    """

    def __init__(self,MAZE_W,MAZE_H):
        self.MAZE_W = MAZE_W
        self.MAZE_H = MAZE_H
        self.maze = [[0]*self.MAZE_W for y in range(self.MAZE_H)]
        self.DUNGEON_W = MAZE_W*3
        self.DUNGEON_H = MAZE_H*3
        self.dungeon = [[0]*self.DUNGEON_W for y in range(self.DUNGEON_H)]

    def make_maze(self):
        """
        迷路を作る
        """
        XP = [ 0, 1, 0,-1]
        YP = [-1, 0, 1, 0]

        #周囲の柱
        for x in range(self.MAZE_W):
            self.maze[0][x] = 1
            self.maze[self.MAZE_H-1][x] = 1
        for y in range(self.MAZE_H):
            self.maze[y][0] = 1
            self.maze[y][self.MAZE_W-1] = 1

        #中を空っぽに
        for y in range(1,self.MAZE_H-1):
            for x in range(1,self.MAZE_W-1):
                self.maze[y][x] = 0

        #柱
        for y in range(2,self.MAZE_H-2,2):
            for x in range(2,self.MAZE_W-2,2):
                self.maze[y][x] = 1

        for y in range(2,self.MAZE_H-2,2):
            for x in range(2,self.MAZE_W-2,2):
                d = random.randint(0,3)
                if x > 2:
                    d = random.randint(0,2)
                self.maze[y+YP[d]][x+XP[d]] = 1

    def make_dungeon(self):
        """
        迷路からダンジョンを作る
        """
        self.make_maze()
        for y in range(self.DUNGEON_H):
            for x in range(self.DUNGEON_W):
                self.dungeon[y][x] = 9
        for y in range(1,self.MAZE_H-1):
            for x in range(1,self.MAZE_W-1):
                dx = x*3+1
                dy = y*3+1
                if self.maze[y][x] == 0:
                    if random.randint(0,99) < 20:
                        for ry in range(-1,2):
                            for rx in range(-1,2):
                                self.dungeon[dy+ry][dx+rx] = 0
                    else:
                        self.dungeon[dy][dx] = 0
                        if self.maze[y-1][x] == 0:
                            self.dungeon[dy-1][dx] = 0
                        if self.maze[y+1][x] == 0:
                            self.dungeon[dy+1][dx] = 0
                        if self.maze[y][x-1] == 0:
                            self.dungeon[dy][dx-1] = 0
                        if self.maze[y][x+1] == 0:
                            self.dungeon[dy][dx+1] = 0


    def put_event(self):
        while True:
            x = random.randint(3,self.DUNGEON_W-4)
            y = random.randint(3,self.DUNGEON_H-4)
            if(self.dungeon[y][x] == 0):
                for ry in range(-1,2):
                    for rx in range(-1,2):
                        self.dungeon[y+ry][x+rx] = 0
                self.dungeon[y][x] = 1
                break
        for i in range(60):
            x = random.randint(3,self.DUNGEON_W-4)
            y = random.randint(3,self.DUNGEON_H-4)
            if(self.dungeon[y][x] == 0):
                self.dungeon[y][x] = random.choice([2,3,3,3,4])
