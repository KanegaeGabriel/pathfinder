import argparse
import os

from Maze import Maze
from Solver import Solver, Solution
import Animator

def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(prog="pathfinder.py", description="Solves a maze using Depth First Search, Breadth First Search, Best-first Search and A* Search, optionally outputting an animation.")

    requiredArgs = parser.add_argument_group("required arguments")
    requiredArgs.add_argument("-f", "--file", help="filename of the maze to be solved", type=str)

    parser.add_argument("-a", "--animate", help="outputs an animation showing all paths", action="store_true")
    parser.add_argument("-l", "--length", help="length of the animation, in seconds (only has effect with -a) | Default: 15", type=int, default=15)

    args = parser.parse_args()

    if not args.file:
        print("Please declare a filename as argument with '-f FILE'. Use '-h' for help.")
        return

    animate = args.animate
    filename = args.file
    videoLength = args.length

    try:
        maze = Maze(filename=filename)
    except:
        print("Couldn't find or read file '{}'. Please check if it exists and is in the right format.".format(filename))
        return

    solver = Solver(animate)

    # Show interpreted maze
    if animate:
        print("{}x{} Maze:".format(maze.w, maze.h))
        print(maze)

    # Run DFS algorithm
    try:
        dfsSolution = solver.dfs(maze)
        print("[DFS] Path Length: {:.2f} | Steps Taken: {}".format(dfsSolution.pathLength, dfsSolution.stepCounter))
        # print([(a, b) for a, b, _ in dfsSolution.path])
        if animate:
            print("".join(["".join(l)+"\n" for l in dfsSolution.frames[-1]]))
    except Exception as e:
        print("[DFS] Path Length: N/A | Steps Taken: {}".format(dfsSolution.stepCounter))

    # Run BFS algorithm
    try:
        bfsSolution = solver.bfs(maze)
        print("[BFS] Path Length: {:.2f} | Steps Taken: {}".format(bfsSolution.pathLength, bfsSolution.stepCounter))
        # print([(a, b) for a, b, _ in bfsSolution.path])
        if animate:
            print("".join(["".join(l)+"\n" for l in bfsSolution.frames[-1]]))
    except Exception as e:
        print("[BFS] Path Length: N/A | Steps Taken: {}".format(bfsSolution.stepCounter))

    # Run BestFS algorithm
    try:
        bestfsSolution = solver.bestfs(maze)
        print("[BestFS] Path Length: {:.2f} | Steps Taken: {}".format(bestfsSolution.pathLength, bestfsSolution.stepCounter))
        # print([(a, b) for a, b, _ in bestfsSolution.path])
        if animate:
            print("".join(["".join(l)+"\n" for l in bestfsSolution.frames[-1]]))
    except Exception as e:
        print("[BestFS] Path Length: N/A | Steps Taken: {}".format(bestfsSolution.stepCounter))

    # Run A* algorithm
    try:
        astarSolution = solver.astar(maze)
        print("[A*] Path Length: {:.2f} | Steps Taken: {}".format(astarSolution.pathLength, astarSolution.stepCounter))
        # print([(a, b) for a, b, _ in astarSolution.path])
        if animate:
            print("".join(["".join(l)+"\n" for l in astarSolution.frames[-1]]))
    except Exception as e:
        print("[A*] Path Length: N/A | Steps Taken: {}".format(astarSolution.stepCounter))

    # Generate animations
    if animate:
        filename = filename.split(".")[0]

        # if dfsSolution.path:
        #     Animator.animate(dfsSolution, str(filename) + "-dfs", videoLength)
        # if bfsSolution.path:
        #     Animator.animate(bfsSolution, str(filename) + "-bfs", videoLength)
        # if bestfsSolution.path:
        #     Animator.animate(bestfsSolution, str(filename) + "-best", videoLength)
        # if astarSolution.path:
        #     Animator.animate(astarSolution, str(filename) + "-astar", videoLength)

        if dfsSolution.path and bfsSolution.path and bestfsSolution.path and astarSolution.path:
            Animator.animateGrid(dfsSolution, bfsSolution, bestfsSolution, astarSolution, str(filename) + "-all", videoLength)
        else:
            print("One of the algorithms couldn't find a path. Can't animate.")

if __name__ == "__main__":
    main()