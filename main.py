'''
From Jason Li @2021

Dummy Code lmao

Real code incoming
'''
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

#Points to draw lines to/Scatterpoints
p = []
for point in range(int(input("How many points? In x y z format: "))):
	p.append([int(x) for x in input("Point? ").split(" ")])
#p = np.array([[-3,4,7],[2,2,2]])
p = np.array([[10,0,0],[0,10,0],[0,0,10],[-10,0,0],[0,-10,0],[0,0,-10],[10,10,10],[-10,-10,-10],[-10,10,10],[-10,-10,10],[-10,10,-10],[10,-10,-10],[10,10,-10],[10,-10,10]])
p = np.array(p)

#Generates "Frames"
def gen(n, xyz):
    xyzt = []
    x1 = 0
    y1 = 0
    z1 = 0
    if sum(xyz) == 0:
        return np.array([[0,0,0]])
    while abs(x1) <= abs(xyz[0]) and abs(y1) <= abs(xyz[1]) and abs(z1) <= abs(xyz[2]):
        xyzt.append([x1,y1,z1])
        x1 += xyz[0]/n
        y1 += xyz[1]/n
        z1 += xyz[2]/n
    return np.array(xyzt)

#This is called each frame
def update(num, data, lines):
    global F, sca
    if num == 99 and F == 0:
        F = 1
        sca = ax.scatter(p[:,0],p[:,1],p[:,2],color = '#ff3399')
    elif num == 99 and F == 1:
        F = 0
        sca.remove()
    if F == 0:
        for e in range(len(data)):
            lines[e][0].set_data(data[e][:2, :num])
            lines[e][0].set_3d_properties(data[e][2, :num])
    else:
        for e in range(len(data)):
            lines[e][0].set_data(data[e][:2, num:])
            lines[e][0].set_3d_properties(data[e][2, num:])

#Number of Updates/Frames
N = 100
F = 0

#Containers for the frames/data
data = np.zeros(len(p), dtype = object)
line = np.zeros(len(p), dtype = object)
for d in range(len(p)):
    data[d] = np.array(gen(N,p[d])).T
    line[d] = ax.plot(data[d][0, 0:1], data[d][1, 0:1], data[d][2, 0:1], color = '#ff3399')

#axis labels, currently set to off    
ax.set_xlim3d([-10.0, 10.0])
ax.set_xlabel('X')

ax.set_ylim3d([-10.0, 10.0])
ax.set_ylabel('Y')

ax.set_zlim3d([-10.0, 10.0])
ax.set_zlabel('Z')

#ax.set_axis_off()

#inits the animation, and calls update() N times spaced out every Interval millisecond
ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=N/50, repeat = True, blit=False)

#Saving the animation as a gif
#ani.save('matplot003.gif', writer='imagemagick')

#Displays the graph
plt.show()
