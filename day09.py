# Advent of Code 2022 - Day 9 solution
# Takes about 15 seconds to solve Part Two... lots of room for optimization,
# but it works.

import json
import numpy as np


def main():
    with open("input/day09.txt") as f:
        lines = f.read().split("\n")

        solve_part_one(lines)
        solve_part_two(lines)


# Logic for Part One
def solve_part_one(instructions):
    # Set up initial state
    # New states will be appended to end of `states` list
    # We represent each state as a list of (row, col) coordinates,
    # where the head is the first item and tail is the second
    states = [
        [(0, 0), (0, 0)],
    ]

    # For each instruction, update head then tail
    for instruction in instructions: #[:10]:

        direction, distance = parse_instruction(instruction)

        for _ in range(distance):
            states = move_head(direction, states)
            states = move_tail(states)

    # Extract set of unique tail locations from states list
    tail_positions = set([state[1] for state in states])
    
    # Answer to Part One
    print(f"Number of unique tail positions (Part One): {len(tail_positions)}")


# Logic for Part Two
def solve_part_two(instructions, n_tail_segments=9):
    # Set up initial state
    # New states will be appended to end of `states` list
    # This time, we represent rope segments by their numeric position
    # Head is 0, and tail segments are numbered 1 to n_segments
    states = [
        [(0, 0)] * (n_tail_segments + 1)
    ]

    # For each instruction, step-by-step, update head then tail segments
    for instruction in instructions: #[:10]:

        direction, distance = parse_instruction(instruction)

        for i in range(distance):
            states = move_head(direction, states)
            for i in range(n_tail_segments):
                states = move_tail(states, segment=i+1)

    # Extract set of unique tail locations from states list
    tail_positions = set([state[-1] for state in states])
    
    # Answer to Part Two
    print(f"Number of unique tail positions (Part Two): {len(tail_positions)}")


def parse_instruction(instruction):
    direction, dist_str = instruction.split(" ")
    return direction, int(dist_str)


def move_head(direction, states):

    new_state = states[-1].copy()
    head_pos = new_state[0]

    if direction == "L":
        new_state[0] = (head_pos[0], head_pos[1]-1)
    elif direction == "R":
        new_state[0] = (head_pos[0], head_pos[1]+1)
    elif direction == "U":
        new_state[0] = (head_pos[0]-1, head_pos[1])
    elif direction == "D":
        new_state[0] = (head_pos[0]+1, head_pos[1])
    else:
        raise ValueError(f"Unrecognized direction `{direction}`")

    return states + [new_state]


def move_tail(states, segment=1):

    new_state = states[-1].copy()
    # We use the term "head" to refer to the segment before the current segment,
    # even if it's not technically the head of the entire rope
    head_pos = new_state[segment-1]
    tail_pos = new_state[segment]

    # There are essentially 2 possible scenarios:

    # 1. Tail does not need to move because head and tail already adjacent. 
    if abs(head_pos[0]-tail_pos[0]) <= 1 and abs(head_pos[1]-tail_pos[1]) <= 1:
        pass

    # 2. Tail needs to move. Tail should move 1 space along each dimension
    # where movement is required. 
    else:
        row_move = np.sign(head_pos[0]-tail_pos[0])
        col_move = np.sign(head_pos[1]-tail_pos[1])
        new_state[segment] = (
            tail_pos[0] + row_move, tail_pos[1] + col_move
        )

    return states + [new_state]


if __name__ == "__main__":
    main()       
