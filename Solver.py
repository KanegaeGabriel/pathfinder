from collections import deque
from heapq import heappop, heappush

class Solver:
    def __init__(self, animate):
        self.animate = animate

    def dfs(self, maze):
        sol = Solution(maze.matrix, self.animate)

        stack = deque([([maze.start+(0,)], maze.start)])

        visited = set()
        while stack:
            path, current = stack.pop()

            if current == maze.end:
                sol.path = path
                break
            
            if current not in visited:
                sol.stepCounter += 1
                sol.addNewFrame(current)

                visited.add(current)
                for neighbor in maze.getNeighbors(current):
                    # if neighbor[2] == 1: # Ignore diagonal paths
                    newPath = path + [neighbor]
                    stack.append((newPath, neighbor[:2]))

        if not sol.path:
            raise Exception("Couldn't find a path.")

        sol.addLastFrame()
        return sol

    def bfs(self, maze):
        sol = Solution(maze.matrix, self.animate)

        queue = deque([([maze.start+(0,)], maze.start)])

        visited = set()
        while queue:
            path, current = queue.popleft()

            if current == maze.end:
                sol.path = path
                break
            
            if current not in visited:
                sol.stepCounter += 1
                sol.addNewFrame(current)

                visited.add(current)
                for neighbor in maze.getNeighbors(current):
                    # if neighbor[2] == 1: # Ignore diagonal paths
                    newPath = path + [neighbor]
                    queue.append((newPath, neighbor[:2]))

        if not sol.path:
            raise Exception("Couldn't find a path.")

        sol.addLastFrame()
        return sol

    def bestfs(self, maze):
        def __bestfsHeuristic(s, e): return abs(s[0]-e[0]) + abs(s[1]-e[1])

        sol = Solution(maze.matrix, self.animate)

        queue = []
        heappush(queue, (__bestfsHeuristic(maze.start, maze.end),
                         0, [maze.start+(0,)], maze.start))

        visited = set()
        while queue:
            _, cost, path, current = heappop(queue)

            if current == maze.end:
                sol.path = path
                break
            
            if current not in visited:
                sol.stepCounter += 1
                sol.addNewFrame(current)

                visited.add(current)
                for neighbor in maze.getNeighbors(current):
                    heappush(queue, (__bestfsHeuristic(neighbor[:2], maze.end),
                                     neighbor[2], path + [neighbor], neighbor[:2]))

        if not sol.path:
            raise Exception("Couldn't find a path.")

        sol.addLastFrame()
        return sol

    def astar(self, maze):
        def __astarHeuristic(s, e): return abs(s[0]-e[0]) + abs(s[1]-e[1])

        sol = Solution(maze.matrix, self.animate)

        queue = []
        heappush(queue, (__astarHeuristic(maze.start, maze.end),
                         0, [maze.start+(0,)], maze.start))

        visited = set()
        while queue:
            _, cost, path, current = heappop(queue)

            if current == maze.end:
                sol.path = path
                break

            if current not in visited:
                sol.stepCounter += 1
                sol.addNewFrame(current)

                visited.add(current)
                for neighbor in maze.getNeighbors(current):
                    heappush(queue, (cost + __astarHeuristic(neighbor[:2], maze.end),
                                     cost + neighbor[2], path + [neighbor], neighbor[:2]))

        if not sol.path:
            raise Exception("Couldn't find a path.")

        sol.addLastFrame()
        return sol

class Solution:
    def __init__(self, matrix, animate):
        self.stepCounter = 0
        self.frames = [self.__copy(matrix)]
        self.animate = animate
        self.path = []
        self.visited = []

    def __copy(self, m): return [r[:] for r in m]

    def addNewFrame(self, p):
        self.visited.append(p)
        
        if not self.animate: return

        x, y = p

        new = self.__copy(self.frames[-1])
        if new[x][y] == "*": new[x][y] = "@"

        self.frames.append(new)

    def addLastFrame(self):
        self.pathLength = sum([n[2] for n in self.path])

        if not self.animate: return

        new = self.__copy(self.frames[-1])
        for x, y, _ in self.path:
            if new[x][y] == "@": new[x][y] = "!"
        
        self.frames.append(new)