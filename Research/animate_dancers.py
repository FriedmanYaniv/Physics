import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import dancers

def init():
    room = dancers.Room(n_dancers=200, width=100, height=100, num_iters=20, speed_noise=0)
    return room


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

# room = dancers.Room(n_dancers=100, width=100, height=100, num_iters=100, speed_noise=0, dancers_speed=1)
# room = dancers.Room(n_dancers=200, width=100, height=100, num_iters=300, speed_noise=0)
# room = dancers.Room(n_dancers=5, width=300, height=300, num_iters=300, speed_noise=0, dancers_speed=1)
# room = dancers.Room(n_dancers=200, width=300, height=300, num_iters=50, speed_noise=0)

num_frames = 200
room = dancers.Room(n_dancers=150, width=300, height=300, num_iters=500, speed_noise=1)
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

anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
