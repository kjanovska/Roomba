import copy
import heapq
import math
import sys


class Square:
    sign = ' '
    state = 'FRESH'
    x_pos = 0
    y_pos = 0
    len_from_start = sys.maxsize
    heuristics = 0

    def __lt__(self, other):
        return (self.len_from_start + self.heuristics/2) < (other.len_from_start + other.heuristics/2)


def agent_function(env, agent_pos):  # A*
    squares = fill_state(env)
    goal = nearest_trash(squares, agent_pos)
    open_squares = []
    predecessor_tab = [[Square() for i in range(len(env[0]))] for j in range(len(env))]
    working_square = copy.deepcopy(squares[agent_pos[0]][agent_pos[1]])
    squares[agent_pos[0]][agent_pos[1]].state = 'OPEN'
    working_square.state = 'OPEN'
    working_square.x_pos = agent_pos[0]
    working_square.y_pos = agent_pos[1]
    working_square.len_from_start = 0
    working_square.heuristics = heuristics([working_square.x_pos, working_square.y_pos], goal)

    heapq.heapify(open_squares)
    heapq.heappush(open_squares, working_square)
    while not len(open_squares) == 0:
        working_square = heapq.heappop(open_squares)  # pop and return smallest item from heap
        if working_square.x_pos == goal[0] and working_square.y_pos == goal[1]:
            return copy.deepcopy(first_predecessor(predecessor_tab, agent_pos, goal))
        search_left_neighbour(working_square, squares, open_squares, predecessor_tab, goal)
        search_right_neighbour(working_square, squares, open_squares, predecessor_tab, goal)
        search_top_neighbour(working_square, squares, open_squares, predecessor_tab, goal)
        search_bottom_neighbour(working_square, squares, open_squares, predecessor_tab, goal)
        squares[working_square.x_pos][working_square.y_pos].state = 'CLOSED'
    return copy.deepcopy(first_predecessor(predecessor_tab, agent_pos, goal))


def search_neighbour_common(working_square, squares, open_squares, predecessor_tab, new_position, goal):
    new_distance = working_square.len_from_start + 1
    if squares[new_position[0]][new_position[1]].sign == '@':
        return
    if squares[new_position[0]][new_position[1]].len_from_start > new_distance or squares[new_position[0]][new_position[1]].state == 'FRESH':
        squares[new_position[0]][new_position[1]].len_from_start = new_distance
        square_movement(squares, open_squares, working_square, new_position, predecessor_tab, goal)


def search_bottom_neighbour(working_square, squares, open_squares, predecessor_tab, goal):
    bottom_x = working_square.x_pos + 1
    bottom_y = working_square.y_pos
    search_neighbour_common(working_square, squares, open_squares, predecessor_tab, [bottom_x, bottom_y], goal)


def search_left_neighbour(working_square, squares, open_squares, predecessor_tab, goal):
    left_x = working_square.x_pos
    left_y = working_square.y_pos - 1
    search_neighbour_common(working_square, squares, open_squares, predecessor_tab, [left_x, left_y], goal)


def search_right_neighbour(working_square, squares, open_squares, predecessor_tab, goal):
    right_x = working_square.x_pos
    right_y = working_square.y_pos + 1
    search_neighbour_common(working_square, squares, open_squares, predecessor_tab, [right_x, right_y], goal)


def search_top_neighbour(working_square, squares, open_squares, predecessor_tab, goal):
    top_x = working_square.x_pos - 1
    top_y = working_square.y_pos
    search_neighbour_common(working_square, squares, open_squares, predecessor_tab, [top_x, top_y], goal)


def square_movement(squares, open_squares, working_square, new_position, predecessor_tab, goal):
    if squares[new_position[0]][new_position[1]].state == 'OPEN':
        squares[new_position[0]][new_position[1]].len_from_start = working_square.len_from_start + 1
        predecessor_tab[new_position[0]][new_position[1]] = working_square
        return
    if squares[new_position[0]][new_position[1]].state != 'FRESH' or squares[new_position[0]][new_position[1]].sign == '@':
        return

    squares[new_position[0]][new_position[1]].state = 'OPEN'
    neighbour_square = Square()
    neighbour_square.x_pos = new_position[0]
    neighbour_square.y_pos = new_position[1]
    neighbour_square.len_from_start = working_square.len_from_start + 1
    neighbour_square.heuristics = heuristics([neighbour_square.x_pos, neighbour_square.y_pos], goal)
    predecessor_tab[neighbour_square.x_pos][neighbour_square.y_pos] = working_square
    heapq.heappush(open_squares, neighbour_square)
    if new_position[0] == goal[0] and new_position[1] == goal[1]:
        squares[new_position[0]][new_position[1]].state = 'END'


def heuristics(square, goal):
    return math.sqrt(pow(goal[0] - square[0], 2) + pow(goal[1] - square[1], 2))


def first_predecessor(predecessor_tab, agent_pos, goal):
    result_coordinates = []
    actual_x = goal[0]
    actual_y = goal[1]
    path_len = 0
    while not (actual_x == agent_pos[0] and actual_y == agent_pos[1]):
        predecessor_x = predecessor_tab[actual_x][actual_y].x_pos
        predecessor_y = predecessor_tab[actual_x][actual_y].y_pos

        if predecessor_x == agent_pos[0] and predecessor_y == agent_pos[1]:
            result_coordinates.append(actual_x)
            result_coordinates.append(actual_y)
            return result_coordinates

        actual_x = predecessor_x
        actual_y = predecessor_y
        path_len += 1


def nearest_trash(state, agent):
    trash = [sys.maxsize, sys.maxsize]
    for row in range(0, len(state)):
        for column in range(0, len(state[0])):
            if state[row][column].sign == 'X':
                if heuristics(agent, [row, column]) <= heuristics(agent, trash):
                    trash = [row, column]
    return trash


def fill_state(state):
    squares = [[Square() for i in range(len(state[0]))] for j in range(len(state))]
    for row in range(0, len(state)):
        for column in range(0, len(state[0])):
            squares[row][column].sign = copy.deepcopy(state[row][column])
            squares[row][column].state = 'FRESH'
            if state[row][column] == '@':
                squares[row][column].state = 'CLOSED'
            squares[row][column].x_pos = row
            squares[row][column].y_pos = column
    return squares
