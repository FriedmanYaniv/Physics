import numpy as np
import matplotlib.pyplot as plt
import random


def choose_best_slice(chosen_slices, num_slices):
    data = chosen_slices.tolist()
    extended_data = data + [num_slices]
    seqs = []
    curr_seq = []
    for n, i in enumerate(data):
        curr_seq.append(data[n])
        if extended_data[n + 1] == i + 1:
            pass
        else:
            seqs.append(curr_seq)
            curr_seq = []

    if len(seqs) == 0:
        seqs.append(curr_seq)
    longest = seqs[np.argmax([len(elem) for elem in seqs])]
    best_slice = longest[int(len(longest) / 2)]
    return best_slice


def get_average_angle(theta1, theta2, alpha):
    v1 = np.array([np.cos(theta1), np.sin(theta1)])
    v2 = np.array([np.cos(theta2), np.sin(theta2)])
    v = (alpha * v1 + (1 - alpha) * v2)
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

    nn = np.argsort(dists)[1:15]
    # nn = np.argsort(dists)[1:4]
    # nn = [nn[0]]

    v_tot = np.array([0, 0])
    # curr_dancer.step_size = np.min([50*1/(0.05+dists[nn[0]]), 3])
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


def find_new_theta_with_pizza_slice(curr_dancer, room):
    x, y = curr_dancer.x, curr_dancer.y

    dists = []
    vecs = []
    angles = []
    for n, dancer in enumerate(room.dancers):
        dx = dancer.x - x
        if abs(dx) > dancer.room_width/2:
            dx = -np.sign(dx) * (dancer.room_width - abs(dx))
        dy = dancer.y - y
        if abs(dy) > dancer.room_height/2:
            dy = -np.sign(dy) * (dancer.room_height - abs(dy))

        dists.append(np.linalg.norm(np.array([dx, dy])))
        vecs.append(np.array([dx, dy]))
        alpha = np.arctan2(dy, dx)
        alpha = (alpha + 2 * np.pi) % (2 * np.pi)
        angles.append(alpha)

    nn = np.argsort(dists)[1:5]

    chosen_angles = np.array(angles)[nn]
    chosen_vecs = np.array(vecs)[nn]
    chosen_dists = np.array(dists)[nn]

    num_slices = 8
    slices = np.zeros(num_slices)
    # d_theta = np.pi / num_slices
    d_theta = 2 * np.pi / num_slices
    for n, theta in enumerate(chosen_angles):
        if chosen_dists[n] < 20:
            slice = int(theta / d_theta)
            slices[slice] += 1 / chosen_dists[n]**2

    directions = np.linspace(0, 2*np.pi - d_theta, num_slices) + d_theta/2
    chosen_slices = np.where(slices == slices.min())[0]
    chosen_slice = random.choice(chosen_slices)
    # chosen_slice = chosen_slices[0]
    if len(chosen_slices) > 1:
        chosen_slice = chosen_slices[np.argmin(abs(chosen_slices - curr_dancer.slice))]

    best_slice = choose_best_slice(chosen_slices, num_slices)
    curr_dancer.slice = chosen_slice
    curr_dancer.slice = best_slice
    angle = directions[best_slice] + (room.noise * (np.random.uniform() - 0.5))
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
    def __init__(self, n_dancers, width, height, num_iters, speed_noise, show_ids=False):
        self.width = width
        self.height = height
        self.n_dancers = n_dancers
        self.num_iters = num_iters
        self.noise = speed_noise
        self.dancers = []
        self.create_dancers()
        self.iter = 0
        self.sparsity = []
        self.mean_direction = []
        self.show_ids = show_ids

    def update_dancers(self):
        for n, dancer in enumerate(self.dancers):
            dancer.update_speed(self)
            # dancer.make_step()
        for n, dancer in enumerate(self.dancers):
            dancer.make_step()


    def create_dancers(self):
            for n in range(self.n_dancers):
                self.dancers.append(Dancer(n, self.width, self.height))

    def draw_room(self):
        # plt.figure()
        # plt.subplot(2, 1, 1)
        axes = plt.gca()
        axes.set_xlim([0, self.width])
        axes.set_ylim([0, self.height])
        color = [1-self.iter/self.num_iters, self.iter/self.num_iters, 0.5]
        locs = np.array([[dancer.x, dancer.y] for dancer in self.dancers])
        colors = color * np.ones((self.n_dancers, 1))
        plt.scatter(locs[:, 0], locs[:, 1], s=15, c=colors)
        if self.show_ids:
            for dancer in room.dancers:
                plt.text(dancer.x + 1, dancer.y - 1, str(dancer.id))

        # plt.subplot(2, 1, 2)
        # axes = plt.gca()
        # axes.set_xlim([0, self.num_iters])
        # axes.set_ylim([0, 1.1])
        # if len(self.sparsity) > 0:
        #     plt.plot(np.array(self.sparsity)[:, 1])

    def calc_sparsity(self):
        num_grid_blocks = int(np.sqrt(self.n_dancers))
        dx, dy = int(self.width / num_grid_blocks), int(self.height / num_grid_blocks)
        occ_mat = np.zeros((num_grid_blocks, num_grid_blocks))
        for n, dancer in enumerate(self.dancers):
            x, y = dancer.x, dancer.y
            x_block = min(int(x / dx), num_grid_blocks-1)
            y_block = min(int(y / dy), num_grid_blocks-1)
            occ_mat[x_block, y_block] = occ_mat[x_block, y_block] + 1

        bol_occ = 1 * (occ_mat > 0)
        score = sum(bol_occ.ravel()) / len(bol_occ.ravel())

        self.sparsity.append([self.iter, score])

    def calc_mean_direction(self):
        v_tot_x = 0
        v_tot_y = 0
        for dancer in self.dancers:
            v_tot_x += np.cos(dancer.direction)
            v_tot_y += np.sin(dancer.direction)

        self.mean_direction.append([self.iter, np.arctan2(v_tot_y, v_tot_x)])



class Dancer:
    # dancer in room
    def __init__(self, id_num, width, height):
        self.x = random.uniform(0, width)  # (0, width)  random.uniform(width*1/5, width*4/5)
        self.y = random.uniform(0, height)  # (0, height)  random.uniform(height*1/5, height*4/5)
        # self.x = random.uniform(0, width/5)
        # self.y = random.uniform(0, height/5)
        self.direction = random.uniform(0, 2 * np.pi)
        self.room_height = height
        self.room_width = width
        self.slice = 0
        self.step_size = 2
        self.id = id_num

    def update_speed(self, curr_room):
        # self.direction = calc_new_theta(self, dir_noise)
        # new_direction = find_new_theta_with_dists_v2(self, curr_room)
        direction = find_new_theta_with_pizza_slice(self, curr_room)
        direction = get_average_angle(direction, self.direction, alpha=0.5)
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


if __name__ == '__main__':
#     a = 1

    # room = Room(n_dancers=20, width=50, height=50, num_iters=100, speed_noise=0, show_ids=True)
    room = Room(n_dancers=150, width=200, height=200, num_iters=200, speed_noise=0)


    room.draw_room()
    # for iter in ra    nge(room.num_iters):
    while room.iter < room.num_iters:
        room.iter += 1
        if room.iter % 10 == 0:
            print('iteration {} / {}'.format(room.iter, room.num_iters))
        room.update_dancers()
        room.calc_sparsity()
        room.calc_mean_direction()
        room.draw_room()

    fig = plt.figure()
    plt.plot(np.array(room.sparsity)[:, 1])
    fig = plt.figure()
    plt.plot(np.array(room.mean_direction)[:, 1])
