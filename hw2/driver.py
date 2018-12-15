import sys
import copy


__author__ = 'Zmarak N. Tarakai'
__course__ = 'CS5001: Experimental Methods -- Deep Learning'
__assign__ = 'HW02: The Values of Tinny Tim'

discount_gamma = 0.8

# Populate board
Q_prev = [[[0 for a in range(4)] for b in range(10)] for c in range(10)]
Q_next = [[[0 for d in range(4)] for e in range(10)] for f in range(10)]

# Populate obstacles
wall = [(3, 2), (3, 3), (4, 5), (4, 6), (5, 5), (6, 3), (6, 4), (6, 5), (6, 7), (2, 5), (4, 2), (7, 3)]
for edge_cell in range(10):
    wall.append((0, edge_cell))
    wall.append((9, edge_cell))
    wall.append((edge_cell, 0))
    wall.append((edge_cell, 9))

cake = [(6, 7)]
donut = [(2, 5)]
fire = [(4, 2)]
demon = [(7, 3)]

action_set = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

bad_action = {
    '^': 'v',
    'v': '^',
    '<': '>',
    '>': '<'
}


def probability(action, action_at_bat):
    if action == action_at_bat:
        p = 0.82
    else:
        p = 0.09
    return p


def value(row, col):
    v = -10000
    for depth in range(4):
        v = max(v, Q_prev[row][col][depth])
    return v


def reward(row, col):
    if (row, col) in cake:
        r = 10.0
    elif (row, col) in donut:
        r = 3.0
    elif (row, col) in fire:
        r = -5.0
    elif (row, col) in demon:
        r = -10.0
    elif (row, col) in wall:
        r = -1.0
    else:
        r = 0.0
    return r


def reward_calc(row, col, action, possible_actions):
    expected_reward = 0.0
    for p_action, p_effect in possible_actions.items():
        p_row = row + p_effect[0]
        p_col = col + p_effect[1]
        expected_reward += probability(action, p_action) * reward(p_row, p_col)
    return expected_reward


# convert Morales pseudo-code to Python
def value_iterate(N):
    global Q_prev
    global action_set

    for iteration in range(N):
        for row in range(10):
            for col in range(10):
                if (row, col) in wall or (row, col) in fire or (row, col) in cake or (row, col) in donut or (row, col) in demon:
                    continue

                for action, effect in action_set.items():
                    depth = 0
                    temp_val = 0.0
                    possible_actions = {action: effect}
                    if action == '^' or action == 'v':
                        possible_actions['<'] = action_set['<']
                        possible_actions['>'] = action_set['>']
                    else:
                        possible_actions['v'] = action_set['v']
                        possible_actions['^'] = action_set['^']

                    for p_action, p_effect in possible_actions.items():
                        prob = probability(action, p_action)
                        val = value(row + p_effect[0], col + p_effect[1])
                        temp_val = prob * val
                    depth += 1
                    Q_next[row][col][depth] = reward_calc(row, col, action, possible_actions) + discount_gamma * temp_val
            Q_prev = copy.deepcopy(Q_next)
        return Q_prev


def policy(row, col):
    global Q_prev
    v = -10000
    for r in range(1, 9):
        for c in range(1, 9):
            for depth in range(4):
                if Q_prev[row][col][depth] > v:
                    policy_val = v
                    v = Q_prev[row][col][depth]
    return policy_val


def border_print(env):
    print('+-------+-------+-------+-------+-------+-------+-------+-------+')
    for col in env:
        print('|{}\t|{}\t|{}\t|{}\t|{}\t|{}\t|{}\t|{}\t|'.format(col[0], col[1], col[2], col[3], col[4], col[5], col[6], col[7]))
    print('+-------+-------+-------+-------+-------+-------+-------+-------+\n')
    return


def format_correct(env, vp):
    rows = []
    for row in range(1, 9):
        current_row = []
        for col in range(1, 9):
            if (row, col) in cake:
                current_row.append('CAKE')
            elif (row, col) in donut:
                current_row.append('DONUT')
            elif (row, col) in demon:
                current_row.append('DEMON')
            elif (row, col) in wall:
                current_row.append('XXX')
            elif (row, col) in fire:
                current_row.append('FIRE')
            elif vp == 'v':
                current_row.append(round(max(env[row][col]), 3))
            elif vp == 'p':
                i = env[row][col].index(max(env[row][col]))
                current_row.append(action_set.keys()[i])
        rows.append(current_row)
    border_print(rows)


def main():
    global Q_prev
    count = 0
    iterations = 1
    # capture input
    while iterations > 0:
        iterations = int(input('Enter No. of Iterations: '))
        if iterations == 0:
            break
        count = count + iterations
        print('Value after {} iterations:\n'.format(count))
        value_iterate(iterations)
        format_correct(Q_prev, 'v')
    # print the policy
    print('Policy:\n')
    format_correct(Q_prev, 'p')
    return


if __name__ == '__main__':
    print(__course__ + ' | ' + __assign__)
    print('Programmer: ' + __author__)
    print('Discount (Gamma): ' + str(discount_gamma))

    main()