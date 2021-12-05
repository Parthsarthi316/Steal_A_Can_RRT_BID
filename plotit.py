# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import plotly as py
# import chart_studio.plotly as py2
import plotly.io as pio
import os
from plotly import graph_objs as go
# from plotly.offline import plot
import numpy as np
import math

colors = ['darkblue', 'teal']


class Plot(object):
    def __init__(self, filename):
        """
        Create a plot
        :param filename: filename
        """
        # camera = dict(eye=dict(x=0., y=2.5, z=0.))#Front View
        #camera = dict(eye=dict(x=2, y=2, z=0.1)) # kind of isometric View
        camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.25, y=1.25, z=1.25)
        )
        
        self.filename = "\frames_try" + filename + ".jpeg"
        self.data = []
        self.layout = {'title': 'Plot',
                       'showlegend': False,
                       'scene_camera':camera
                       }

        self.fig = {'data': self.data,
                    'layout': self.layout}

    def plot_tree(self, X, trees):
        """
        Plot tree
        :param X: Search Space
        :param trees: list of trees
        """
        if X.dimensions == 2:  # plot in 2D
            self.plot_tree_2d(trees)
        elif X.dimensions == 3 or X.dimensions == 6:  # plot in 3D
            self.plot_tree_3d(trees)
        else:  # can't plot in higher dimensions
            print("Cannot plot in > 3 dimensions sometimes")

    def plot_tree_2d(self, trees):
        """
        Plot 2D trees
        :param trees: trees to plot
        """
        for i, tree in enumerate(trees):
            for start, end in tree.E.items():
                if end is not None:
                    trace = go.Scatter(
                        x=[start[0][:3], end[0][:3]],
                        y=[start[1][:3], end[1][:3]],
                        line=dict(
                            color=colors[i]
                        ),
                        mode="lines"
                    )
                    self.data.append(trace)

    def plot_tree_3d(self, trees):
        """
        Plot 3D trees
        :param trees: trees to plot
        """
        for i, tree in enumerate(trees):
            for start, end in tree.E.items():
                if end is not None:
                    trace = go.Scatter3d(
                        x=[start[0], end[0]],
                        y=[start[1], end[1]],
                        z=[start[2], end[2]],
                        line=dict(
                            color=colors[i]
                        ),
                        mode="lines"
                    )
                    self.data.append(trace)

    def plot_obstacles(self, X, O):
        """
        Plot obstacles
        :param X: Search Space
        :param O: list of obstacles
        """
        if X.dimensions == 2:  # plot in 2D
            self.layout['shapes'] = []
            for O_i in O:
                # noinspection PyUnresolvedReferences
                self.layout['shapes'].append(
                    {
                        'type': 'rect',
                        'x0': O_i[0],
                        'y0': O_i[1],
                        'x1': O_i[2],
                        'y1': O_i[3],
                        'line': {
                            'color': 'purple',
                            'width': 4,
                        },
                        'fillcolor': 'purple',
                        'opacity': 0.70
                    },
                )
        elif X.dimensions == 3 or X.dimensions == 6:  # plot in 3D
            for O_i in O:
                obs = go.Mesh3d(
                    x=[O_i[0], O_i[0], O_i[3], O_i[3], O_i[0], O_i[0], O_i[3], O_i[3]],
                    y=[O_i[1], O_i[4], O_i[4], O_i[1], O_i[1], O_i[4], O_i[4], O_i[1]],
                    z=[O_i[2], O_i[2], O_i[2], O_i[2], O_i[5], O_i[5], O_i[5], O_i[5]],
                    i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                    k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                    color='purple',
                    opacity=0.20
                )
                self.data.append(obs)
        else:  # can't plot in higher dimensions
            print("Cannot plot in > 3 dimensions")

    def plot_obstacles_y(self, X, O):
        """
        Plot obstacles
        :param X: Search Space
        :param O: list of obstacles
        """
        if X.dimensions == 2:  # plot in 2D
            self.layout['shapes'] = []
            for O_i in O:
                # noinspection PyUnresolvedReferences
                self.layout['shapes'].append(
                    {
                        'type': 'rect',
                        'x0': O_i[0],
                        'y0': O_i[1],
                        'x1': O_i[2],
                        'y1': O_i[3],
                        'line': {
                            'color': 'yellow',
                            'width': 4,
                        },
                        'fillcolor': 'yellow',
                        'opacity': 0.70
                    },
                )
        elif X.dimensions == 3 or X.dimensions == 6:  # plot in 3D
            for O_i in O:
                obs = go.Mesh3d(
                    x=[O_i[0], O_i[0], O_i[3], O_i[3], O_i[0], O_i[0], O_i[3], O_i[3]],
                    y=[O_i[1], O_i[4], O_i[4], O_i[1], O_i[1], O_i[4], O_i[4], O_i[1]],
                    z=[O_i[2], O_i[2], O_i[2], O_i[2], O_i[5], O_i[5], O_i[5], O_i[5]],
                    i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                    k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                    color='yellow',
                    opacity=0.20
                )
                self.data.append(obs)
        else:  # can't plot in higher dimensions
            print("Cannot plot in > 3 dimensions")

    def plot_path(self, X, path):
        """
        Plot path through Search Space
        :param X: Search Space
        :param path: path through space given as a sequence of points
        """
        if X.dimensions == 2:  # plot in 2D
            x, y = [], []
            for i in path:
                x.append(i[0])
                y.append(i[1])
            trace = go.Scatter(
                x=x,
                y=y,
                line=dict(
                    color="red",
                    width=4
                ),
                mode="lines"
            )

            self.data.append(trace)
        elif X.dimensions == 3 or X.dimensions == 6:  # plot in 3D
            x, y, z = [], [], []
            for i in path:
                x.append(i[0])
                y.append(i[1])
                z.append(i[2])
            trace = go.Scatter3d(
                x=x,
                y=y,
                z=z,
                line=dict(
                    color="red",
                    width=4
                ),
                mode="lines"
            )

            self.data.append(trace)
        else:  # can't plot in higher dimensions
            print("Cannot plot in > 3 dimensions")

    def plot_start(self, X, x_init):
        """
        Plot starting point
        :param X: Search Space
        :param x_init: starting location
        """
        if X.dimensions == 2:  # plot in 2D
            trace = go.Scatter(
                x=[x_init[0]],
                y=[x_init[1]],
                line=dict(
                    color="orange",
                    width=10
                ),
                mode="markers"
            )

            self.data.append(trace)
        elif X.dimensions == 3 or X.dimensions == 6:  # plot in 3D
            trace = go.Scatter3d(
                x=[x_init[0]],
                y=[x_init[1]],
                z=[x_init[2]],
                line=dict(
                    color="orange",
                    width=10
                ),
                mode="markers"
            )

            self.data.append(trace)
        else:  # can't plot in higher dimensions
            print("Cannot plot in > 3 dimensions")
            
            
    def cylinder(self, r, h, x0, y0, z0, nt=100, nv =50):
        """
        parametrize the cylinder of radius r, height h, mid point a
        """
        theta = np.linspace(0, 2*np.pi, nt)
        a = z0
        v = np.linspace(a-h/2, a+h/2, nv )
        theta, v = np.meshgrid(theta, v)
        x1 = x0 + r*np.cos(theta)
        y1 = y0 + r*np.sin(theta)
        z1 = z0 + v
        
        colorscale = [[0, 'blue'],
             [1, 'blue']]
        
        trace = go.Surface(x=x1, y=y1, z=z1,
                 colorscale = colorscale,
                 showscale=False,
                 opacity=0.7)
        
        self.data.append(trace)
        
    def r_cylinder(self, x0, y0, z0, psi=0, fi=0, theta=0, n = 50, r = 2.5, h = 12):
        """
        parametrize the cylinder of radius r, height h, mid point a
        """
        angle = np.linspace(0, 2*np.pi, num=n)
        v = np.linspace(-h/2, +h/2, num=n)
        angle, v = np.meshgrid(angle, v)
        x1 = r*np.cos(angle)
        y1 = r*np.sin(angle)
        z1 = v
        c = np.stack((x1,y1,z1),axis=2)

        R = np.array([[math.cos(psi)*math.cos(theta)-math.sin(fi)*math.sin(psi)*math.sin(theta), 
                       -math.cos(fi)*math.sin(psi),
                       math.cos(psi)*math.sin(theta)+math.cos(theta)*math.sin(fi)*math.sin(psi)],
                      [math.cos(theta)*math.sin(psi)+math.cos(psi)*math.sin(fi)*math.sin(theta),
                       math.cos(fi)*math.cos(psi),
                       math.sin(psi)*math.sin(theta)-math.cos(theta)*math.sin(fi)*math.cos(psi)],
                      [-math.cos(fi)*math.sin(theta),math.sin(fi),math.cos(fi)*math.cos(theta)]])
        e = np.zeros((50,50,3))
        for i in range(50):
            d = R@(c[i].T)
            e[i] = d.T
            
        x2 = x0 + e[:,:,0]
        y2 = y0 + e[:,:,1]
        z2 = z0 + e[:,:,2]
        

        
        colorscale = [[0, 'orange'],
             [1, 'orange']]
        
        trace = go.Surface(x=x2, y=y2, z=z2,
                 colorscale = colorscale,
                 showscale=False,
                 opacity=0.7)
        
        self.data.append(trace)

    def plot_goal(self, X, x_goal):
        """
        Plot goal point
        :param X: Search Space
        :param x_goal: goal location
        """
        if X.dimensions == 2:  # plot in 2D
            trace = go.Scatter(
                x=[x_goal[0]],
                y=[x_goal[1]],
                line=dict(
                    color="green",
                    width=10
                ),
                mode="markers"
            )

            self.data.append(trace)
        elif X.dimensions == 3 or X.dimensions == 6:  # plot in 3D
            trace = go.Scatter3d(
                x=[x_goal[0]],
                y=[x_goal[1]],
                z=[x_goal[2]],
                line=dict(
                    color="green",
                    width=10
                ),
                mode="markers"
            )

            self.data.append(trace)
        else:  # can't plot in higher dimensions
            print("Cannot plot in > 3 dimensions")

    def rotation(psi, fi, theta):
        
        R = np.array([[math.cos(psi)*math.cos(theta)-math.sin(fi)*math.sin(psi)*math.sin(theta), 
                       -math.cos(fi)*math.sin(psi),
                       math.cos(psi)*math.sin(theta)+math.cos(theta)*math.sin(fi)*math.sin(psi)],
                      [math.cos(theta)*math.sin(psi)+math.cos(psi)*math.sin(fi)*math.sin(theta),
                       math.cos(fi)*math.cos(psi),
                       math.sin(psi)*math.sin(theta)-math.cos(theta)*math.sin(fi)*math.cos(psi)],
                      [-math.cos(fi)*math.sin(theta),math.sin(fi),math.cos(fi)*math.cos(theta)]])
        
        return R
        

    def draw(self, i):
        """
        Render the plot to a folder
        """
        directory = r"\frames_try"
        os.chdir(directory)
        if i<10:
            pio.write_image(self.fig,"0"+str(i)+".jpeg")
        else:
            pio.write_image(self.fig,str(i)+".jpeg")
        
    
    def draw2(self, auto_open=True):
        py.offline.plot(self.fig, auto_open=auto_open)
    
    
    
    