from math import sqrt

class Maze:
    def __init__(self, filename=None, matrix=None):
        if matrix and filename:
            raise Exception("Please specify only a file OR a matrix.")

        if matrix:
            self.matrix = matrix
        elif filename:
            self.matrix = self.__loadFromFile(filename)
        else:
            raise Exception("Please specify a file or a matrix.")

        self.w = len(self.matrix)
        self.h = len(self.matrix[0])
        for i in range(self.w):
            for j in range(self.h):
                if self.matrix[i][j] == "#":
                    self.start = (i, j)
                elif self.matrix[i][j] == "$":
                    self.end = (i, j)

        assert(self.matrix and self.w and self.h and self.start and self.end)

    def __str__(self): return "".join(["".join(l)+"\n" for l in self.matrix])

    def __loadFromFile(self, filename):
        with open(filename) as f:
            content = [list(l.strip()) for l in f.readlines()]
        return content

    def getNeighbors(self, p):
        x, y = p

        # Enumerates possible moves clockwise:
        possible = [(x-1, y+1, sqrt(2)), (x, y+1, 1), # NE, E
                    (x+1, y+1, sqrt(2)), (x+1, y, 1), # SE, S
                    (x+1, y-1, sqrt(2)), (x, y-1, 1), # SW, W
                    (x-1, y-1, sqrt(2)), (x-1, y, 1)] # NW, N

        neighbors = [(i, j, c) for i, j, c in possible
                     if 0 <= i < self.w and
                        0 <= j < self.h and
                        self.matrix[i][j] != "-"]

        return neighbors