import numpy as np
import matplotlib.pyplot as plt
import random
import numpy.linalg as la


def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)


def get_average_angle(theta1, theta2):
    v1 = np.array([np.cos(theta1), np.sin(theta1)])
    v2 = np.array([np.cos(theta2), np.sin(theta2)])
    v = (v1 + v2)
    v = v/np.linalg.norm(v)
    return np.arctan2(v[1], v[0])


def calc_anlgle(xs, ys):
    vec = v1 - v2
    np.arctan2(vec[1], vec[0])
    return 0


def find_new_theta_with_dists_v2(curr_dancer, room):
    x, y = curr_dancer.x, curr_dancer.y

    dists = []
    vecs = []
    for n, dancer in enumerate(room.dancers):
        dx = dancer.x - x
        if abs(dx) > dancer.room_width/2:
            dx = -np.sign(dx) * (dancer.room_width - abs(dx))
        dy = dancer.y - y
        if abs(dy) > dancer.room_height/2:
            dy = -np.sign(dy) * (dancer.room_height - abs(dy))

        dists.append(np.linalg.norm(np.array([dx, dy])))
        vecs.append(np.array([dx, dy]))

    nn = np.argsort(dists)[1:10]
    # nn = np.argsort(dists)[1:4]
    # nn = [nn[0]]

    v_tot = np.array([0, 0])
    curr_dancer.step_size = np.min([50*1/(0.05+dists[nn[0]]), 3])
    if curr_dancer.step_size > 20:
        print('OMG!!!')
    for order, n in enumerate(nn):
        if True:  # dists[n] < 50:
            # dancer = room.dancers[n]
            v2 = vecs[n]  # v2 = np.array([dancer.x, dancer.y])
            v_tot = v_tot + (v2 / (dists[n]**2))   # ((v2 - v1) / (dists[n]**1))

    angle = np.arctan2(v_tot[1], v_tot[0]) - np.pi
    angle = angle + (room.noise * (np.random.uniform() - 0.5))
    return angle


def find_new_theta_with_dists(curr_dancer, room):
    x, y = curr_dancer.x, curr_dancer.y
    v1 = np.array([x, y])

    dists = []
    for n, dancer in enumerate(room.dancers):
        dists.append(np.linalg.norm(v1 - np.array([dancer.x, dancer.y])))
    # nn = np.argsort(dists)[1:10]
    nn = np.argsort(dists)[1:4]
    # nn = [nn[0]]

    v_tot = np.array([0, 0])
    curr_dancer.step_size = 50*1/(0.05+dists[nn[0]])
    if curr_dancer.step_size > 20:
        print('OMG!!!')
    for order, n in enumerate(nn):
        if True:  # dists[n] < 50:
            dancer = room.dancers[n]
            v2 = np.array([dancer.x, dancer.y])
            v_tot = v_tot + ((v2 - v1) / (dists[n]**1))

    angle = np.arctan2(v_tot[1], v_tot[0]) - np.pi
    return angle


def make_step(dancer, ax):
    if ax == 'x':
        # return (dancer.x + (dancer.step_size + np.random.uniform()-0.5) * np.cos(dancer.direction)) % dancer.room_width
        return (dancer.x + (dancer.step_size) * np.cos(dancer.direction)) % dancer.room_width
    if ax == 'y':
        # return (dancer.y + (dancer.step_size + np.random.uniform()-0.5) * np.sin(dancer.direction)) % dancer.room_height
        return (dancer.y + (dancer.step_size) * np.sin(dancer.direction)) % dancer.room_height


class Room:
    # object of all dancers and room
    def __init__(self, n_dancers, width, height, num_iters, speed_noise):
        self.width = width
        self.height = height
        self.n_dancers = n_dancers
        self.num_iters = num_iters
        self.noise = speed_noise
        self.dancers = []
        self.create_dancers()
        self.iter = 0

    def update_dancers(self):
        for n, dancer in enumerate(self.dancers):
            dancer.update_speed(self)
            # dancer.make_step()
        for n, dancer in enumerate(self.dancers):
            dancer.make_step()
        #     if dancer.out_of_bounds:
        #         a = 1
        # r = list(range(len(room.dancers)))
        # # random.shuffle(r)
        # for n in r:
        #     dancer = room.dancers[n]
        #     dancer.direction = dancer.update_speed(self.noise)
        #     # dancer.make_step()
        # for n in r:
        #     dancer = room.dancers[n]
        #     dancer.make_step()

    def create_dancers(self):
            for n in range(self.n_dancers):
                self.dancers.append(Dancer(self.width, self.height))

    def draw_room(self):
        # plt.figure()
        axes = plt.gca()
        axes.set_xlim([0, self.width])
        axes.set_ylim([0, self.height])
        color = [1-self.iter/self.num_iters, self.iter/self.num_iters, 0.5]
        locs = np.array([[dancer.x, dancer.y] for dancer in self.dancers])
        plt.scatter(locs[:, 0], locs[:, 1], s=15, c=color)


class Dancer:
    # dancer in room
    def __init__(self, width, height):
        # self.x = random.uniform(width*2/5, width*3/5)  # (0, width)
        # self.y = random.uniform(height*2/5, height*3/5)  # (0, height)
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.direction = random.uniform(0, 2 * np.pi)
        self.room_height = height
        self.room_width = width
        self.step_size = 1

    def update_speed(self, curr_room):
        # self.direction = calc_new_theta(self, dir_noise)
        new_direction = find_new_theta_with_dists_v2(self, curr_room)
        direction = get_average_angle(new_direction, self.direction)
        self.direction = direction

    def make_step(self):
        global room
        self.x = make_step(self, 'x')
        self.y = make_step(self, 'y')

    def out_of_bounds(self):
        out_of_bounds = False
        if (self.y > self.room_height) or (self.y < 0):
            out_of_bounds = True
        if (self.x > self.room_width) or (self.x < 0):
            out_of_bounds = True
        return out_of_bounds


# if __name__ == '__main__':
#     a = 1

    # room = Room(n_dancers=200, width=100, height=100, num_iters=100, speed_noise=0, dancers_speed=2)
room = Room(n_dancers=150, width=300, height=300, num_iters=100, speed_noise=0)
# room.dancers[0].y = 51
# room.dancers[0].x = 50
# room.dancers[1].y = 49
# room.dancers[1].x = 250
# room.dancers[2].y = 200
# room.dancers[2].x = 200
# room.dancers[3].y = 200
# room.dancers[3].x = 100
# room.dancers[4].y = 150
# room.dancers[4].x = 150

room.draw_room()
# for iter in range(room.num_iters):
while room.iter < room.num_iters:
    room.iter += 1
    room.update_dancers()
    room.draw_room()
