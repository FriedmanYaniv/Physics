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


def new_animate(ii):
    # global room
    # fig.clear()
    if ii % 10 == 0:
        print('iteration {} / {}'.format(ii, room.num_iters))
    fig = plt.figure()
    width = 100
    height = 100
    ax = plt.axes(xlim=(0, width), ylim=(0, height))
    xy = np.array([[dancer.x[ii], dancer.y[ii]] for dancer in room.dancers])
    color = [1 - room.iter / room.num_iters, room.iter / room.num_iters, 0.5]
    colors = color * np.ones((room.n_dancers, 1))
    plt.scatter(xy[:, 0], xy[:, 1], s=15, c=colors)
    return 0


fig = plt.figure()
width = 100
height = 100
ax = plt.axes(xlim=(0, width), ylim=(0, height))


num_frames = 150
room = dancers.Room(n_dancers=150, width=250, height=300, num_iters=num_frames, speed_noise=1)
while room.iter < room.num_iters:
    room.iter += 1
    if room.iter % 10 == 0:
        print('iteration {} / {}'.format(room.iter, room.num_iters))
    room.update_dancers()
    room.calc_sparsity()
    # room.draw_room()


anim = animation.FuncAnimation(fig, new_animate, init_func=init,
                               frames=num_frames)


# save code and animation
curr_path = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(curr_path, 'animation')
if not os.path.exists(directory):
    os.makedirs(directory)
files = ['animate_dancers.py', 'dancers.py']
for file in files:
    copyfile(os.path.join(curr_path, file), os.path.join(directory, file))

anim.save(os.path.join(directory, 'basic_animation.mp4'), fps=20, extra_args=['-vcodec', 'libx264'])



# class AnimatedScatter(object):
#     """An animated scatter plot using matplotlib.animations.FuncAnimation."""
#     def __init__(self, numpoints=50):
#         self.numpoints = numpoints
#         self.stream = self.data_stream()
#
#         # Setup the figure and axes...
#         self.fig, self.ax = plt.subplots()
#         # Then setup FuncAnimation.
#         self.ani = animation.FuncAnimation(self.fig, self.update, interval=5,
#                                           init_func=self.setup_plot, blit=True)
#
#     def setup_plot(self):
#         """Initial drawing of the scatter plot."""
#         x, y, s, c = next(self.stream).T
#         self.scat = self.ax.scatter(x, y, c=c, s=s, vmin=0, vmax=1,
#                                     cmap="jet", edgecolor="k")
#         self.ax.axis([-10, 10, -10, 10])
#         # For FuncAnimation's sake, we need to return the artist we'll be using
#         # Note that it expects a sequence of artists, thus the trailing comma.
#         return self.scat,
#
#     def data_stream(self):
#         """Generate a random walk (brownian motion). Data is scaled to produce
#         a soft "flickering" effect."""
#         xy = (np.random.random((self.numpoints, 2))-0.5)*10
#         s, c = np.random.random((self.numpoints, 2)).T
#         while True:
#             xy += 0.03 * (np.random.random((self.numpoints, 2)) - 0.5)
#             s += 0.05 * (np.random.random(self.numpoints) - 0.5)
#             c += 0.02 * (np.random.random(self.numpoints) - 0.5)
#             yield np.c_[xy[:,0], xy[:,1], s, c]
#
#     def update(self, i):
#         """Update the scatter plot."""
#         data = next(self.stream)
#
#         # Set x and y data...
#         self.scat.set_offsets(data[:, :2])
#         # Set sizes...
#         self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
#         # Set colors..
#         self.scat.set_array(data[:, 3])
#
#         # We need to return the updated artist for FuncAnimation to draw..
#         # Note that it expects a sequence of artists, thus the trailing comma.
#         return self.scat,
#
#
# if __name__ == '__main__':
#     a = AnimatedScatter()
#     plt.show()