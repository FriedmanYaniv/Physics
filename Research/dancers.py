import numpy as np
import matplotlib.pyplot as plt
import random


def make_step(dancer, ax):
    if ax == 'x':
        return dancer.x + dancer.speed * np.cos(dancer.direction)
    if ax == 'y':
        return dancer.y + dancer.speed * np.sin(dancer.direction)


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
    # nn_dancers = find_nn_dancers(dancer.x, dancer.y, room)
    block_arg = find_new_theta_with_blocks(dancer.x, dancer.y, room)
    new_theta = (np.random.uniform()-0.5) * dir_noise + block_arg * np.pi / 4
    return new_theta


def find_new_theta_with_blocks(x, y, room):
    # all_locations = np.array([[dancer.x, dancer.y] for dancer in room.dancers])
    ignore_r = 0.0
    b_half_r = room.height / 20
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
    for ii, dancer in enumerate(cur_room.dancers):
        x, y = dancer.x, dancer.y
        for n, block in enumerate(blocks):
            if (x > block[0]) and (x < block[1]) and (y < block[2]) and (y > block[3]):
                blocks_occupation[n] += 1
    return blocks_occupation


def find_nn_dancers(x, y, room):
    all_locations = np.array([[dancer.x, dancer.y] for dancer in room.dancers])
    relative_locations = all_locations - np.array([location_x, y])
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
        self.iter = 0

    def update_dancers(self):
        for n, dancer in enumerate(self.dancers):
            dancer.update_speed(self.noise)
        for n, dancer in enumerate(self.dancers):
            dancer.make_step()
            if dancer.out_of_bounds:
                a = 1

    def create_dancers(self, dancers_speed):
            for n in range(self.n_dancers):
                self.dancers.append(Dancer(self.width, self.height, dancers_speed))

    def draw_room(self):
        # plt.figure()
        axes = plt.gca()
        axes.set_xlim([0, self.width])
        axes.set_ylim([0, self.height])
        color = [1-self.iter/self.num_iters, self.iter/self.num_iters, 0.5]
        locs = np.array([[dancer.x, dancer.y] for dancer in self.dancers])
        plt.scatter(locs[:, 0], locs[:, 1], c=color)


class Dancer:
    # dancer in room
    def __init__(self, width, height, speed):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.speed = speed
        self.direction = random.uniform(0, 2 * np.pi)
        self.room_height = height
        self.room_width = width

    def update_speed(self, dir_noise):
        # y = self.y
        # if 95<y<105:
        #     a = 1
        new_theta = calc_new_theta(self, dir_noise)
        # self.direction = (self.direction + new_theta) / 2
        self.direction = new_theta

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


noise = 1
# room = Room(n_dancers=200, width=100, height=100, num_iters=100, speed_noise=0, dancers_speed=2)
room = Room(n_dancers=200, width=100, height=100, num_iters=100, speed_noise=0.5, dancers_speed=1)
room.draw_room()
# for iter in range(room.num_iters):
while room.iter < room.num_iters:
    room.iter += 1
    room.update_dancers()
    room.draw_room()


