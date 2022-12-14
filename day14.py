# Advent of Code 2022 - Day 14 solution

import time

import numpy as np


def main():
    with open("input/day14.txt") as f:
        scan = f.read()

        # Part One
        board = make_board(scan)
        grains = 0
        while board.add_sand():
            grains += 1
        # board.display(path="board_viz_pt1.txt")
        print(f"Part One: Added {grains} grains before sand flows off board")

        # Part Two
        board = make_board(scan, with_floor=True)
        grains = 0
        while board.add_sand():
            grains += 1
        # board.display(path="board_viz_pt2.txt")
        print(f"Part Two: Added {grains} grains before sand doesn't fit")


def make_board(scan, with_floor=False):
    lines = scan.split("\n")

    # Each wall is a tuple of 2 coorinates,
    # representing its start and end point
    walls = []

    for line in lines:
        points = line.split(" -> ")
        points = [p.split(",") for p in points]
        points = [(int(p[0]), int(p[1])) for p in points]
        point_pairs = [(points[i], points[i + 1]) for i in range(len(points) - 1)]
        walls.extend(point_pairs)

    return Board(walls, with_floor)


class Board:

    # Initialize the board with a list of walls
    # Each wall consists of a start point and end point
    def __init__(self, walls, with_floor=False, sand_start=(500, 0)):

        self._wall_locs = set()
        self._sand_locs = set()
        self._floor = None

        self._sand_start = sand_start

        # Internally, we will represent a Board as several sets of (x, y) coordinates
        # representing the positions of walls and sand, as well as a single coordinate
        # value representing the sand production location.

        # Add wall locations
        for wall in walls:

            # Sort coordinates, so that first coordinate will always be smaller
            wall = sorted(wall)

            # Case: X is constant (vertical wall)
            if wall[0][0] == wall[1][0]:
                wall_locs = [(wall[0][0], y) for y in range(wall[0][1], wall[1][1] + 1)]

            # Case: Y is constant (horizontal wall)
            elif wall[0][1] == wall[1][1]:
                wall_locs = [(x, wall[0][1]) for x in range(wall[0][0], wall[1][0] + 1)]

            # Case: Neither (Error)
            else:
                raise ValueError(f"Error: Walls must be vertical or horizontal, not diagonal. The given coordinates were: {wall}")  # fmt: skip

            self._wall_locs.update(wall_locs)

        # If with_floor is True, set floor y-value to be 2 + the max y value of all walls
        if with_floor:
            max_y = max([y for _, y in self._wall_locs])
            self._floor = max_y + 2

    # Drop a grain of sand from the sand starting location and iterate the board
    # until the sand has come to rest or fallen off the board.
    # Returns True if the sand comes to rest on the board, and False if it falls off.
    # If _floor is True, may also return False if the sand cannot be added due to the pile
    # reaching the sand start location.
    def add_sand(self):
        prev_sand_pos = None
        sand_pos = self._sand_start

        if sand_pos in self._sand_locs:
            return False

        self._sand_locs.add(sand_pos)

        while sand_pos and not sand_pos == prev_sand_pos:
            prev_sand_pos = sand_pos
            sand_pos = self._move_sand(sand_pos)

        if not sand_pos:
            # Sand has flown off board
            return False

        # Otherwise it has come to rest on the board
        return True

    # Move the grain of sand located at sand_pos one step, update sand locations, and return
    # the new sand position.
    def _move_sand(self, sand_pos):

        # Delete sand from current position
        self._sand_locs.remove(sand_pos)

        # First, try to move down (y-value increases)
        new_pos = (sand_pos[0], sand_pos[1] + 1)
        if self._out_of_bounds(new_pos):
            return None
        if self._is_empty(new_pos):
            self._sand_locs.add(new_pos)
            return new_pos

        # Then, try to move diagonally left & down
        new_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
        if self._out_of_bounds(new_pos):
            return None
        if self._is_empty(new_pos):
            self._sand_locs.add(new_pos)
            return new_pos

        # Then, try to move diagonally right & down
        new_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
        if self._out_of_bounds(new_pos):
            return None
        if self._is_empty(new_pos):
            self._sand_locs.add(new_pos)
            return new_pos

        # If we've gotten all the way here, sand can't move
        # Put it back in original position
        self._sand_locs.add(sand_pos)
        return sand_pos

    # Returns True if the given location is empty (i.e. not wall or sand or floor),
    # False otherwise
    def _is_empty(self, coords):
        if self._floor is not None and coords[1] >= self._floor:
            return False
        return coords not in self._wall_locs and coords not in self._sand_locs

    def _out_of_bounds(self, coords):
        # Cannot be out of bounds if there is a floor
        if self._floor is not None:
            return False
        # Otherwise, return True if y value is >= than max y-value of any wall
        else:
            max_y = max([y for _, y in self._wall_locs])
            return coords[1] > max_y

    def display(self, path=None):

        # Find min x and y coordinates of all items
        min_x = min([x for x, _ in self._wall_locs.union(self._sand_locs)])
        min_y = min([y for _, y in self._wall_locs.union(self._sand_locs)])

        # Add min_x and min_y to all coordinates, so that all coordinates are nonnegative
        display_wall_locs = {(x + min_x, y + min_y) for x, y in self._wall_locs}
        display_sand_locs = {(x + min_x, y + min_y) for x, y in self._sand_locs}

        # Now, find max x and y coordinates so we know how big to make the board
        max_x = max([x for x, _ in display_wall_locs.union(display_sand_locs)])
        max_y = max([y for _, y in display_wall_locs.union(display_sand_locs)])

        # Construct numpy array
        board = np.full(shape=(max_x + 1, max_y + 1), fill_value=".")

        # Draw items
        for coords in display_wall_locs:
            board[coords] = "#"
        for coords in display_sand_locs:
            board[coords] = "o"

        # We must transpose to get the correct display
        board_T = board.T

        lines = ["".join(board_T[r, :]) for r in range(board_T.shape[0])]

        text = "\n".join(lines)

        if path:
            with open(path, "w") as f:
                f.write(text)

        return text


if __name__ == "__main__":
    main()
