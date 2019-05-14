import numpy as np
import matplotlib.pyplot as plt
import random


def make_step(dancer, ax):
    if ax == 'x':
        return dancer.location_x + dancer.speed * np.cos(dancer.direction)
    if ax == 'y':
        return dancer.location_y + dancer.speed * np.sin(dancer.direction)


def create_blocks(x, y, ignore_r, b_half_r):
    blocks = [[x + ignore_r, x + ignore_r + 2 * b_half_r, y + b_half_r, y - b_half_r],  # east
              [x + ignore_r, x + ignore_r + 2 * b_half_r, y + ignore_r + 2 * b_half_r, y + ignore_r],  # north east
              [x - b_half_r, x + b_half_r, y + ignore_r + 2 * b_half_r, y + ignore_r],  # north
              [x - ignore_r - 2 * b_half_r, x - ignore_r, y + ignore_r + 2 * b_half_r, y + ignore_r],  # north west
              [x - ignore_r - 2 * b_half_r, x - ignore_r, y + b_half_r, y - b_half_r],  # west
              [x - ignore_r - 2 * b_half_r, x - ignore_r, y - ignore_r, y - ignore_r - 2 * b_half_r],  # south west
              [x - b_half_r, x + b_half_r, y - ignore_r, y - ignore_r - 2 * b_half_r],  # south
              [x + ignore_r, x + ignore_r + 2 * b_half_r, y - ignore_r, y - ignore_r - 2 * b_half_r]]  # south ease
    return blocks


def get_not_allowed_directions(x, y, cur_room, ignore_r):
    not_allowed = []
    if x < ignore_r:
        not_allowed.extend([3, 4, 5])
    if x > cur_room.width - ignore_r:
        not_allowed.extend([0, 1, 7])
    if y < ignore_r:
        not_allowed.extend([1, 2, 3])
    if y > cur_room.height - ignore_r:
        not_allowed.extend([5, 6, 7])

    return not_allowed

def calc_new_theta(dancer):
    global room
    # interaction_r = 1
    # nn_dancers = find_nn_dancers(dancer.location_x, dancer.location_y, room)
    block_arg = find_new_theta_with_blocks(dancer.location_x, dancer.location_y, room)
    new_theta = np.random.randn() * 1 + block_arg * np.pi / 4
    return new_theta


def find_new_theta_with_blocks(x, y, room):
    # all_locations = np.array([[dancer.location_x, dancer.location_y] for dancer in room.dancers])
    ignore_r = 5
    b_half_r = 20
    blocks = create_blocks(x, y, ignore_r, b_half_r)

    blocks_occupation = calc_block_occupancy(room, blocks)
    not_allowed = get_not_allowed_directions(x, y, room, ignore_r)
    for ind in not_allowed:
        blocks_occupation[ind] = 9999

    best_directions = np.where(blocks_occupation == blocks_occupation.min())

    new_direction = random.choice(best_directions[0])

    return new_direction


def calc_block_occupancy(cur_room, blocks):
    blocks_occupation = np.zeros(8)
    for dancer in cur_room.dancers:
        x, y = dancer.location_x, dancer.location_y
        for n, block in enumerate(blocks):
            if (x > block[0]) and (x < block[1]) and (y < block[2]) and (y > block[3]):
                blocks_occupation[n] += 1
    return blocks_occupation


def find_nn_dancers(location_x, location_y, room):
    all_locations = np.array([[dancer.location_x, dancer.location_y] for dancer in room.dancers])
    relative_locations = all_locations - np.array([location_x, location_y])
    dists = (relative_locations[:, 0]**2 + relative_locations[:, 1]**2)**0.5
    directions = np.arctan(relative_locations[:, 1]/relative_locations[:, 0])
    return 0


class Room:
    # object of all dancers and room
    def __init__(self, n_dancers, width, height, num_iters):
        self.width = width
        self.height = height
        self.n_dancers = n_dancers
        self.num_iters = num_iters
        self.dancers = []
        self.create_dancers()

    def update_dancers(self):
        for dancer in self.dancers:
            dancer.update_speed()
        for dancer in self.dancers:
            dancer.make_step()

    def create_dancers(self):
            for n in range(self.n_dancers):
                self.dancers.append(Dancer(self.width, self.height))

    def draw_room(self, iter):
        # plt.figure()
        color = [1-iter/self.num_iters, iter/self.num_iters, 0.5]
        locs = np.array([[dancer.location_x, dancer.location_y] for dancer in self.dancers])
        plt.scatter(locs[:, 0], locs[:, 1], color=color)


class Dancer:
    # dancer in room
    def __init__(self, width, height):
        self.location_x = random.uniform(0, width)
        self.location_y = random.uniform(0, height)
        self.speed = 3
        self.direction = random.uniform(0, 2 * np.pi)

    def update_speed(self):
        global room
        global noise
        new_theta = calc_new_theta(self)
        self.direction = new_theta

    def make_step(self):
        global room
        self.location_x = make_step(self, 'x')
        self.location_y = make_step(self, 'y')


noise = 1
room = Room(n_dancers=100, width=500, height=100, num_iters=100)
room.draw_room(iter=0)
for iter in range(room.num_iters):
    room.update_dancers()
    room.draw_room(iter)


