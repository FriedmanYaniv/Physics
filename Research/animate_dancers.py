import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import dancers
import os
from shutil import copyfile

def init():
    # room = dancers.Room(n_dancers=200, width=100, height=100, num_iters=20, speed_noise=0)
    return room


def animate(iter):
    global room
    fig.clear()
    room.iter += 1
    if room.iter % 10 == 0:
        print('iteration {} / {}'.format(room.iter, room.num_iters))
    room.update_dancers()
    room.draw_room()
    return 0


fig = plt.figure()
width = 100
height = 100
ax = plt.axes(xlim=(0, width), ylim=(0, height))

num_frames = 200
room = dancers.Room(n_dancers=150, width=200, height=200, num_iters=200, speed_noise=0)
# room = dancers.Room(n_dancers=10, width=50, height=50, num_iters=350, speed_noise=1.5)
# room.dancers[0].y = 50
# room.dancers[0].x = 50
# room.dancers[1].y = 50
# room.dancers[1].x = 250
# room.dancers[2].y = 200
# room.dancers[2].x = 200
# room.dancers[3].y = 200
# room.dancers[3].x = 100
# room.dancers[4].y = 150
# room.dancers[4].x = 150


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=num_frames)


# save code and animation
curr_path = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(curr_path, 'animation')
if not os.path.exists(directory):
    os.makedirs(directory)
files = ['animate_dancers.py', 'dancers.py']
for file in files:
    copyfile(os.path.join(curr_path, file), os.path.join(directory, file))

anim.save(os.path.join(directory, 'basic_animation.mp4'), fps=10, extra_args=['-vcodec', 'libx264'])
