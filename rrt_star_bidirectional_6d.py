import numpy as np

from rrt_star_bid import RRTStarBidirectional
from search_space import SearchSpace
from plotit import Plot
import math

import cv2
import os
import random

random.seed(103)

side = 6
b1 = 100
b2 = 125
otol = 4
p = math.pi
X_dimensions = np.array([(0, 200), (0, 100), (0, 100), (0, p), (0, p), (0, p)])  # dimensions of Search Space
# obstacles
p = math.pi

Obstacles_gen = np.array(
    [(b1-side, 0, 0, 0, 0, 0, b1+side, 100, 72.5+otol, p, p, p), (b1-side, 0, 72.5+otol, 0, 0, 0, b1+side, 42.5+otol, 87.5-otol, p, p, p), (b1-side, 57.5-otol, 72.5+otol, 0, 0, 0, b1+side, 100, 87.5-otol, p, p, p), (b1-side, 0, 87.5-otol, 0, 0, 0, b1+side, 100, 100, p, p, p),
     (b2-side, 0, 0, 0, 0, 0, b2+side, 100, 12.5+otol, p, p, p), (b2-side, 0, 12.5+otol, 0, 0, 0, b2+side, 42.5+otol, 27.5-otol, p, p, p), (b2-side, 57.5-otol, 12.5+otol, 0, 0, 0, b2+side, 100, 27.5-otol, p, p, p), (b2-side, 0, 27.5-otol, 0, 0, 0, b2+side, 100, 100, p, p, p)])

Obstacles = np.array(
    [(b1-side, 0, 0, b1+side, 100, 72.5+otol), (b1-side, 0, 72.5+otol, b1+side, 42.5+otol, 87.5-otol), (b1-side, 57.5-otol, 72.5+otol, b1+side, 100, 87.5-otol), (b1-side, 0, 87.5-otol, b1+side, 100, 100),
     (b2-side, 0, 0, b2+side, 100, 12.5+otol), (b2-side, 0, 12.5+otol, b2+side, 42.5+otol, 27.5-otol), (b2-side, 57.5-otol, 12.5+otol, b2+side, 100, 27.5-otol), (b2-side, 0, 27.5-otol, b2+side, 100, 100)])

side = 0.5
otol = 0
Obstacles_dis = np.array(
    [(b1-side, 0, 0, b1+side, 100, 72.5+otol), (b1-side, 0, 72.5+otol, b1+side, 42.5+otol, 87.5-otol), (b1-side, 57.5-otol, 72.5+otol, b1+side, 100, 87.5-otol), (b1-side, 0, 87.5-otol, b1+side, 100, 100),
     (b2-side, 0, 0, b2+side, 100, 12.5+otol), (b2-side, 0, 12.5+otol, b2+side, 42.5+otol, 27.5-otol), (b2-side, 57.5-otol, 12.5+otol, b2+side, 100, 27.5-otol), (b2-side, 0, 27.5-otol, b2+side, 100, 100)])


x_init = (20, 50, 2.5, 0, p/2, 0)  # starting location
x_goal = (175, 50, 6, 0, 0, 0)  # goal location

Q = np.array([(8, 4)])  # length of tree edges
r = 1  # length of smallest edge to check for intersection with obstacles
max_samples = 100000  # max number of samples to take before timing out
rewire_count = 1  # optional, number of nearby branches to rewire
prc = 0.01  # probability of checking for a connection to goal

# create Search Space
X = SearchSpace(X_dimensions, Obstacles_gen)

# create rrt_search
rrt = RRTStarBidirectional(X, Q, x_init, x_goal, max_samples, r, prc, rewire_count)
path = rrt.rrt_star_bidirectional()

# plot Static
plot = Plot("rrt_star_bid_3d")
plot.plot_tree(X, rrt.trees)            # Comment out if you dont want trees
if path is not None:                    #Comment out if you dont want path
    plot.plot_path(X, path)
plot.plot_obstacles(X, Obstacles_dis[:4])
plot.plot_obstacles_y(X, Obstacles_dis[4:8])
plot.plot_start(X, x_init)
plot.plot_goal(X, x_goal)
for i in range(len(path)):            #Comment out if you dont want cans
    x0, y0, z0, psi, fi, theta = path[i]
    plot.r_cylinder(x0, y0, z0, psi, fi, theta)
plot.draw2(auto_open=True)

# Saving each frame of the plot in a folder defined in plot.draw(i) with name i.jpeg
for i in range(len(path)):
    plot = Plot("rrt_star_bid_3d")

    plot.plot_obstacles(X, Obstacles_dis[:4])
    plot.plot_obstacles_y(X, Obstacles_dis[4:8])
    plot.plot_start(X, x_init)
    plot.plot_goal(X, x_goal)
    x0, y0, z0, psi, fi, theta = path[i]
    plot.r_cylinder(x0, y0, z0, psi, fi, theta)
    plot.draw(i)

# Parsing the image folder to generate a video from all the frames available

image_folder = r"frames_try"  #change path here
video_name = r"video3.avi"  ##change path here 

images = [img for img in os.listdir(image_folder)]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 4, (width,height))
print(len(images))
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

