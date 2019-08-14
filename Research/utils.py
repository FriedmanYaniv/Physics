import numpy as np

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
        not_allowed.extend([0, 1, 7, 2, 6])
    if y < ignore_r:
        not_allowed.extend([5, 6, 7, 4, 0])
    if y > cur_room.height - ignore_r:
        not_allowed.extend([1, 2, 3, 4, 0])

    return not_allowed


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
