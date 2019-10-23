import os
from multiprocessing import Pool
from math import ceil

try:
    import cv2
    import numpy as np
except ImportError:
    print("You don't seem to have OpenCV or numpy installed. Please check and try again.")
    exit()

RGB = {"-": 0x1A2A3A, # Wall
       "*": 0xAAAAAA, # Non-Visited Tile
       "@": 0x6699FF, # Visited Tile
       "!": 0xFF6666, # Final Path
       "#": 0xFFFF66, # Start Tile
       "$": 0x66FF99, # End Tile
       "?": 0xDDDDDD  # Grid Border
      }

def __BGR(h): return ((h&0xFF, (h&0xFF00)>>8, (h&0xFF0000)>>16))

def __createFolder(foldername):
    try:
        os.mkdir(foldername)
    except:
        for file in os.listdir(foldername):
            filepath = os.path.join(foldername, file)
            if os.path.isfile(filepath) and filepath.endswith(".png"):
                os.unlink(filepath)

def __generateVideo(filename, framerate):
    directory = None

    # If file in inside a folder, move to it
    if "/" in filename:
        directory, filename = filename.split("/")
        os.chdir(directory)
    if "\\" in filename:
        directory, filename = filename.split("\\")
        os.chdir(directory)

    print("Writing to '{}.mp4'...".format(filename))

    # Generate video file
    os.chdir(filename)
    os.system("ffmpeg -y -hide_banner -loglevel warning -framerate {} -i %d.png -c:v libx264 -pix_fmt yuv420p ../{}.mp4".format(framerate, filename))
    os.chdir("..")

    # Remove frames folder
    for file in os.listdir(filename):
        filepath = os.path.join(filename, file)
        if os.path.isfile(filepath) and filepath.endswith(".png"):
            os.unlink(filepath)
    os.rmdir(filename)

    # If file was inside a folder, move out of it
    if directory:
        os.chdir("..")

def __generateFrame(i, filename, solf, w, h, M):
    # Convert to pixels
    pixels = np.array([[__BGR(RGB[solf[i][j]]) for j in range(h)] for i in range(w)])

    # Save as image
    filepath = os.path.join("{}".format(filename), "{}.png".format(i))
    cv2.imwrite(filepath, cv2.resize(pixels, (w*M, h*M), interpolation=cv2.INTER_NEAREST))

def __generateGridFrame(i, filename, solTLf, solTRf, solBLf, solBRf, w, h, B, W, H, M):
    # Get every solution
    tl = np.array(solTLf)
    tr = np.array(solTRf)
    bl = np.array(solBLf)
    br = np.array(solBRf)

    # Join all four in a 2x2 grid
    all4 = np.full((W, H), "?")
    all4[B:w+B, B:h+B] = tl
    all4[B:w+B, h+B+B:-B] = tr
    all4[w+B+B:-B, B:h+B] = bl
    all4[w+B+B:-B, h+B+B:-B] = br

    # Generate frame
    __generateFrame(i, filename, all4, W, H, M)

def animate(sol, filename, length=15):
    print("Animating '{}'...".format(filename))

    # Solution res
    w, h = len(sol.frames[0]), len(sol.frames[0][0])

    # Max res of resulting image
    maxResW, maxResH = 1080, 1080
    M = min(maxResW//w, maxResH//h)

    # Amount of frames needed to reproduce the path
    duration = len(sol.frames)

    # Create (or empty) folder
    __createFolder(filename)

    # Maximum amount of frames to generate
    maxFrames = 3000

    print("Generating {} frames...".format(duration-1))

    # Prepare frames
    frames = []
    for i in range(1, duration):
        if i != 1 and i % (duration//min(maxFrames, duration)) != 0 and i != duration-1: continue
        frames.append((i, filename, sol.frames[i], w, h, M))

    # Generate frames (in parallel)
    pool = Pool()
    pool.starmap(__generateFrame, frames)
    pool.close()
    pool.join()

    # Set video framerate
    framerate = ceil(min(maxFrames, duration)/length)

    # Generate video and remove frames folder
    __generateVideo(filename, framerate)

def animateGrid(solTL, solTR, solBL, solBR, filename, length=15):
    print("Animating '{}'...".format(filename))

    # Assert every solution has the same res
    assert(len(solTL.frames[0]) == len(solTR.frames[0]) == len(solBL.frames[0]) == len(solBR.frames[0]))
    assert(len(solTL.frames[0][0]) == len(solTR.frames[0][0]) == len(solBL.frames[0][0]) == len(solBR.frames[0][0]))

    # Solution res
    w, h = len(solTL.frames[0]), len(solTL.frames[0][0])

    # Size of borders
    B = max(1, min(w//50, h//50))

    # 2x2 grid res
    W = w*2 + 3*B
    H = h*2 + 3*B

    # Max res of resulting image
    maxResW, maxResH = 1080, 1080
    M = min(maxResW//W, maxResH//H)

    # Amount of frames needed to reproduce all paths
    duration = max(len(solTL.frames), len(solTR.frames), len(solBL.frames), len(solBR.frames))

    # Create (or empty) folder
    __createFolder(filename)

    # Maximum amount of frames to generate
    maxFrames = 3000

    print("Generating {} frames...".format(duration-1))

    # Prepare frames
    frames = []
    for i in range(1, duration):
        if i != 1 and i % (duration//min(maxFrames, duration)) != 0 and i != duration-1: continue
        frames.append((i, filename,
                       solTL.frames[i if i < len(solTL.frames) else -1],
                       solTR.frames[i if i < len(solTR.frames) else -1],
                       solBL.frames[i if i < len(solBL.frames) else -1],
                       solBR.frames[i if i < len(solBR.frames) else -1],
                       w, h, B, W, H, M))

    # Generate frames (in parallel)
    pool = Pool()
    pool.starmap(__generateGridFrame, frames)
    pool.close()
    pool.join()

    # Set video framerate
    framerate = ceil(min(maxFrames, duration)/length)

    # Generate video and remove frames folder
    __generateVideo(filename, framerate)