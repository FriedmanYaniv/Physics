import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import dancers

def init():
    # room = dancers.Room(n_dancers=200, width=100, height=100, num_iters=100, speed_noise=1, dancers_speed=3)
    return 0


def animate(iter):
    global room
    fig.clear()
    room.iter += 1
    room.update_dancers()
    room.draw_room()
    return 0


fig = plt.figure()
width = 100
height = 100
ax = plt.axes(xlim=(0, width), ylim=(0, height))

room = dancers.Room(n_dancers=200, width=100, height=100, num_iters=500, speed_noise=0.0, dancers_speed=2)
# room = dancers.Room(n_dancers=2, width=width, height=height, num_iters=200, speed_noise=0.5, dancers_speed=1)
# room = dancers.Room(n_dancers=5, width=10, height=10, num_iters=400, speed_noise=0, dancers_speed=2)

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=1, blit=False)

anim.save('basic_animation.mp4', fps=10, extra_args=['-vcodec', 'libx264'])
