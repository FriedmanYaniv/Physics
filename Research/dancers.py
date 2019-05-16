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
        not_allowed.extend([3, 4, 5, 2, 6])
    if x > cur_room.width - ignore_r:
        not_allowed.extend([0, 1, 7 , 2, 6])
    if y < ignore_r:
        not_allowed.extend([5, 6, 7, 4, 0])
    if y > cur_room.height - ignore_r:
        not_allowed.extend([1, 2, 3, 4, 0])

    return not_allowed


def calc_new_theta(dancer, dir_noise):
    global room
    # interaction_r = 1
    # nn_dancers = find_nn_dancers(dancer.location_x, dancer.location_y, room)
    block_arg = find_new_theta_with_blocks(dancer.location_x, dancer.location_y, room)
    new_theta = (np.random.uniform()-0.5) * dir_noise + block_arg * np.pi / 4
    return new_theta


def find_new_theta_with_blocks(x, y, room):
    # all_locations = np.array([[dancer.location_x, dancer.location_y] for dancer in room.dancers])
    ignore_r = 0.5
    b_half_r = 15
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
    def __init__(self, n_dancers, width, height, num_iters, speed_noise, dancers_speed):
        self.width = width
        self.height = height
        self.n_dancers = n_dancers
        self.num_iters = num_iters
        self.noise = speed_noise
        self.dancers = []
        self.create_dancers(dancers_speed)

    def update_dancers(self):
        for dancer in self.dancers:
            dancer.update_speed(self.noise)
        for dancer in self.dancers:
            dancer.make_step()
            if dancer.out_of_bounds:
                a = 1

    def create_dancers(self, dancers_speed):
            for n in range(self.n_dancers):
                self.dancers.append(Dancer(self.width, self.height, dancers_speed))

    def draw_room(self, iter):
        # plt.figure()
        color = [1-iter/self.num_iters, iter/self.num_iters, 0.5]
        locs = np.array([[dancer.location_x, dancer.location_y] for dancer in self.dancers])
        plt.scatter(locs[:, 0], locs[:, 1], c=color)


class Dancer:
    # dancer in room
    def __init__(self, width, height, speed):
        self.location_x = random.uniform(0, width)
        self.location_y = random.uniform(0, height)
        self.speed = speed
        self.direction = random.uniform(0, 2 * np.pi)
        self.room_height = height
        self.room_width = width

    def update_speed(self, dir_noise):
        # y = self.location_y
        # if 95<y<105:
        #     a = 1
        new_theta = calc_new_theta(self, dir_noise)
        self.direction = (self.direction + new_theta) / 2

    def make_step(self):
        global room
        self.location_x = make_step(self, 'x')
        self.location_y = make_step(self, 'y')

    def out_of_bounds(self):
        out_of_bounds = False
        if (self.location_y > self.room_height) or (self.location_y < 0):
            out_of_bounds = True
        if (self.location_x > self.room_width) or (self.location_x < 0):
            out_of_bounds = True
        return out_of_bounds


noise = 1
# room = Room(n_dancers=200, width=100, height=100, num_iters=100, speed_noise=0, dancers_speed=2)
room = Room(n_dancers=1, width=10, height=10, num_iters=100, speed_noise=0, dancers_speed=1)
room.draw_room(iter=0)
for iter in range(room.num_iters):
    room.update_dancers()
    room.draw_room(iter)


