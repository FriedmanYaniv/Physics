import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import dancers
import os
from shutil import copyfile
import pickle as p
from dancers import Room, Dancer

room = p.load(open(r'C:\Users\yaniv\PycharmProjects\Physics\Research\old_room.p', "rb"))

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

num_frames = 20  # number of frames to save in animation
# room = dancers.Room(n_dancers=150, width=300, height=200, num_iters=15000, speed_noise=0)

# room.num_iters = 40

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=num_frames, repeat=False)


# save code and animation
curr_path = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(curr_path, 'animation')
if not os.path.exists(directory):
    os.makedirs(directory)
files = ['animate_dancers.py', 'dancers.py']
for file in files:
    copyfile(os.path.join(curr_path, file), os.path.join(directory, file))

anim.save(os.path.join(directory, 'basic_animation.mp4'), fps=20, extra_args=['-vcodec', 'libx264'])


if __name__ == '__main__':
    pass

