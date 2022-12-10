# Advent of Code 2022 - Day 8 solution

import numpy as np


def main():
    with open("input/day08.txt") as f:
        lines = f.read().split("\n")
        np_arrays = [np.array([int(c) for c in line]) for line in lines]

        tree_grid = np.stack(np_arrays)

        all_visible_trees = set()
        all_visible_trees.update(visible_trees(tree_grid, direction="left"))
        all_visible_trees.update(visible_trees(tree_grid, direction="right"))

        all_visible_trees.update(visible_trees(tree_grid, direction="top"))
        all_visible_trees.update(visible_trees(tree_grid, direction="bottom"))

        # Answer to Part One
        print(f"Total number of visible trees: {len(all_visible_trees)}")

        # Answer to Part Two
        max_scenic_score = find_max_scenic_score(tree_grid)
        print(f"Maximum scenic score in grid: {max_scenic_score}")


def visualize_grid(tree_grid, visible):

    row_strs = []

    for i in range(tree_grid.shape[0]):
        row_str = ""
        for j in range(tree_grid.shape[1]):
            if (i, j) in visible:
                row_str = row_str + f"({tree_grid[i,j]})"
            else:
                row_str = row_str + f" {tree_grid[i,j]} "
        row_strs.append(row_str)

    with open("output.txt", "w") as f:
        f.write("\n".join(row_strs))


def visible_trees(tree_grid, direction):

    # Set the order we will traverse the trees, based on direction param
    if direction == "left":
        indices_outer = list(range(tree_grid.shape[0]))
        indices_inner = list(range(tree_grid.shape[1]))
    elif direction == "right":
        indices_outer = list(range(tree_grid.shape[0]))
        indices_inner = list(reversed(range(tree_grid.shape[1])))
    elif direction == "top":
        indices_outer = list(range(tree_grid.shape[1]))
        indices_inner = list(range(tree_grid.shape[0]))
    elif direction == "bottom":
        indices_outer = list(range(tree_grid.shape[1]))
        indices_inner = list(reversed(range(tree_grid.shape[0])))
    else:
        raise ValueError(
            f"Invalid direction '{direction}'."
            + "Direction must be one of: 'left', 'right', 'top', 'bottom' "
        )

    visible_trees = set()

    for i in indices_outer:
        tallest = -1
        for j in indices_inner:
            coords = (i, j) if direction in ["left", "right"] else (j, i)
            tree_height = tree_grid[coords]
            if tree_height > tallest:
                visible_trees.add(coords)
                tallest = tree_height

    return visible_trees


def calculate_scenic_score(tree_grid, coords):

    # Look left, right, up, down
    dist_left = tree_dist_for_direction(tree_grid, coords, "left")
    dist_right = tree_dist_for_direction(tree_grid, coords, "right")
    dist_up = tree_dist_for_direction(tree_grid, coords, "up")
    dist_down = tree_dist_for_direction(tree_grid, coords, "down")

    # Calculate scenic score by multiplying them all together
    score = dist_left * dist_right * dist_up * dist_down

    return score


def tree_dist_for_direction(tree_grid, coords, direction):

    r, c = coords

    if direction == "left":
        return 0 if c == 0 else tree_dist(tree_grid[coords], np.flip(tree_grid[r, :c]))
    elif direction == "right":
        return (
            0
            if c == tree_grid.shape[1] - 1
            else tree_dist(tree_grid[coords], tree_grid[r, c + 1 :])
        )
    elif direction == "up":
        return 0 if r == 0 else tree_dist(tree_grid[coords], np.flip(tree_grid[:r, c]))
    elif direction == "down":
        return (
            0
            if r == tree_grid.shape[0] - 1
            else tree_dist(tree_grid[coords], tree_grid[r + 1 :, c])
        )


def tree_dist(center_tree_height, tree_array):
    if len(tree_array) == 0:
        return 0
    elif tree_array[0] >= center_tree_height:
        return 1
    else:
        return 1 + tree_dist(center_tree_height, tree_array[1:])


def find_max_scenic_score(tree_grid):

    max_score = 0

    for i in range(tree_grid.shape[0]):
        for j in range(tree_grid.shape[1]):
            score = calculate_scenic_score(tree_grid, (i, j))
            if score > max_score:
                # print(f"Found higher scenic score! Coords = {(i, j)} ; score = {score}")
                max_score = score

    return max_score


if __name__ == "__main__":
    main()
