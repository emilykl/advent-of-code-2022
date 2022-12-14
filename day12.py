# Advent of Code 2022 - Day 12 solution
from heapq import heappush, heappop, heapify

import numpy as np


def main():
    with open("input/day12.txt") as f:
        maze = parse_maze(f.read())

        _, shortest_path_len = solve_maze(maze)
        print(f"!!! {shortest_path_len}")

        a_locations = zip(*np.where(maze == "a"))

        sols = [solve_maze(maze, custom_start=a_loc) for a_loc in a_locations]
        sols = [sol[1] for sol in sols if sol[1]]

        print(f"minimum = {min(sols)}")

        # visualize_visited(maze, visited)


def visualize_visited(maze, visited):
    viz = np.full(shape=maze.shape, fill_value="..")
    for node in visited:
        path_len, _, coords = node
        viz[coords] = str(path_len)

    viz[find_start(maze)] = "S"
    viz[find_end(maze)] = "E"

    # Pad for nice display
    max_str_len = np.vectorize(len)(viz).max()

    def left_pad(s):
        pad = " " * max(0, max_str_len - len(s))
        return pad + s

    viz = np.vectorize(left_pad)(viz)

    lines = [" ".join(viz[r, :]) for r in range(viz.shape[0])]
    text = "\n".join(lines)
    with open("maze_viz.txt", "w") as f:
        f.write(text)


def parse_maze(text):
    lines = text.split("\n")
    np_arrays = [np.array([c for c in line]) for line in lines]
    return np.stack(np_arrays)


def solve_maze(maze, custom_start=None):

    # If start not given, find E
    if custom_start:
        start_coords = custom_start
    else:
        start_coords = find_start(maze)

    # Initialize start node
    # Nodes are represented as a tuple of (path_length, coords)
    # Path length is first so sorting works properly
    end_coords = find_end(maze)
    start = (0, manhattan(start_coords, end_coords), start_coords)

    # Initialize visited nodes
    # Initially this is only the starting node
    visited = [start]

    # Initialize to-do list
    # We use a priority queue for this
    # Initially, the to-do list is all nodes reachable from the starting node
    to_do = get_neighbors(start, maze, end_coords)
    heapify(to_do)
    to_do_coords_set = {n[2] for n in to_do}

    counter = 0

    while len(to_do) > 0:

        # Pop highest-priority node off the queue
        curr_node = heappop(to_do)
        path_len, rem_dist, coords = curr_node

        counter += 1
        if False:  # counter % 50000 == 0:
            print("===")
            print(f"searching coord {coords}")
            print(
                f"counter = {counter} ; path_len = {path_len} ; rem_dist = {rem_dist}"
            )

        # Add it to the visited list
        visited.append(curr_node)

        # Check if it's the end
        if maze[coords] == "E":
            # print(f"Solution found! path_len = {path_len}")
            return visited, path_len

        # Add neighbors to to-do list, if not already there
        # neighbors = get_neighbors(curr_node, maze, end_coords)
        neighbors = get_neighbors(curr_node, maze, end_coords)
        neighbors_scoot = get_neighbors_scoot(curr_node, maze, end_coords)
        for n in neighbors + neighbors_scoot:
            if not n[2] in to_do_coords_set:
                heappush(to_do, n)
                to_do_coords_set.add(n[2])

    return visited, None


def find_start(maze):
    where = np.where(maze == "S")
    return (where[0][0], where[1][0])


def find_end(maze):
    where = np.where(maze == "E")
    return (where[0][0], where[1][0])


def get_neighbors_scoot(node, maze, end_coords):
    path_len, rem_dist, coords = node

    neighbors = []

    # Scoot left
    l_coords = (coords[0], coords[1] - 1)
    final_l_coords = None
    while (
        l_coords[1] >= 0
        and as_num(maze[l_coords]) < as_num(maze[(l_coords[0], l_coords[1] + 1)]) + 2
    ):
        final_l_coords = l_coords
        if final_l_coords[1] == end_coords[1]:
            break
        l_coords = (l_coords[0], l_coords[1] - 1)

    # Scoot right
    r_coords = (coords[0], coords[1] + 1)
    final_r_coords = None
    while (
        r_coords[1] < maze.shape[1]
        and as_num(maze[r_coords]) < as_num(maze[(r_coords[0], r_coords[1] - 1)]) + 2
    ):
        final_r_coords = r_coords
        if final_r_coords[1] == end_coords[1]:
            break
        r_coords = (r_coords[0], r_coords[1] + 1)

    # Scoot up
    u_coords = (coords[0] - 1, coords[1])
    final_u_coords = None
    while (
        u_coords[0] >= 0
        and as_num(maze[u_coords]) < as_num(maze[(u_coords[0] + 1, u_coords[1])]) + 2
    ):
        final_u_coords = u_coords
        if final_u_coords[0] == end_coords[0]:
            break
        u_coords = (u_coords[0] - 1, u_coords[1])

    # Scoot down
    d_coords = (coords[0] + 1, coords[1])
    final_d_coords = None
    while (
        d_coords[0] < maze.shape[0]
        and as_num(maze[d_coords]) < as_num(maze[(d_coords[0] - 1, d_coords[1])]) + 2
    ):
        final_d_coords = d_coords
        if final_d_coords[0] == end_coords[0]:
            break
        d_coords = (d_coords[0] + 1, d_coords[1])

    # Create nodes
    neighbors = [
        (path_len - manhattan(n, coords), manhattan(n, end_coords), n)
        for n in [
            final_l_coords,
            final_r_coords,
            final_u_coords,
            final_d_coords,
        ]
        if n
    ]
    # for n in neighbors:
    #     if n[2] == (20, 138):
    #         print(f"found the end! value = {maze[n[2]]}")
    # print(f"returning neighbors (scoot) of {coords}: {neighbors}")
    return neighbors


def get_neighbors(node, maze, end_coords):
    path_len, rem_dist, coords = node

    neighbors = [
        (coords[0], coords[1] - 1),
        (coords[0], coords[1] + 1),
        (coords[0] - 1, coords[1]),
        (coords[0] + 1, coords[1]),
    ]

    # Remove neighbors outside maze
    neighbors = [
        (r, c)
        for r, c in neighbors
        if r >= 0 and r < maze.shape[0] and c >= 0 and c < maze.shape[1]
    ]

    # Remove neighbors unreachable due to terrain
    neighbors = [n for n in neighbors if as_num(maze[n]) < as_num(maze[coords]) + 2]

    return [(path_len + 1, manhattan(n, end_coords), n) for n in neighbors]


def manhattan(coords_1, coords_2):
    # Negated, so sorting works correctly
    return -(abs(coords_2[0] - coords_1[0]) + abs(coords_2[1] - coords_1[1]))


def as_num(char):
    if char == "S":
        return 0
    elif char == "E":
        return 25
    return ord(char) - 97


if __name__ == "__main__":
    main()
