# Advent of Code 2022 - Day 23 solution

from collections import Counter


def main():
    with open("input/day23.txt") as f:
        elf_locs = parse_board(f.read())

    # Part One
    move_funcs = [check_north, check_south, check_west, check_east]
    n_rounds = 10
    for i in range(n_rounds):
        proposed_moves = propose_moves(elf_locs, move_funcs)
        move_counts = Counter(p[1] for p in proposed_moves)
        filtered_moves = [p for p in proposed_moves if move_counts[p[1]] < 2]
        elf_locs = move_elves(filtered_moves, elf_locs)
        # Move first move func to end of list
        move_funcs = move_funcs[1:] + [move_funcs[0]]

    rdim, cdim = find_bounding_dimensions(elf_locs)
    answer = rdim * cdim - len(elf_locs)
    print(f"Part One: Unoccupied ground squares: {answer}")

    # Part Two
    with open("input/day23.txt") as f:
        elf_locs = parse_board(f.read())
    move_funcs = [check_north, check_south, check_west, check_east]
    nmoves = 1
    rounds_finished = 0
    while nmoves:
        proposed_moves = propose_moves(elf_locs, move_funcs)
        move_counts = Counter(p[1] for p in proposed_moves)
        filtered_moves = [p for p in proposed_moves if move_counts[p[1]] < 2]
        elf_locs = move_elves(filtered_moves, elf_locs)
        move_funcs = move_funcs[1:] + [move_funcs[0]]
        nmoves = len(filtered_moves)
        rounds_finished += 1

    print(f"Part Two: In Round {rounds_finished}, no elves moved.")


def normalize(elf_locs):
    rvals, cvals = zip(*elf_locs)
    rmin, cmin = min(rvals), min(cvals)
    return [(r - rmin, c - cmin) for r, c in elf_locs], rmin, cmin


def board_str(elf_locs):
    normalized_elf_locs, rmin, cmin = normalize(elf_locs)
    rdim, cdim = find_bounding_dimensions(elf_locs)
    rows = [["."] * cdim for _ in range(rdim)]
    for r, c in normalized_elf_locs:
        rows[r][c] = "#"
    row_indices = range(rmin, rmin + rdim)
    col_indices = range(cmin, cmin + cdim)
    rows = [[str(ri).rjust(3, " ") + " "] + r for ri, r in zip(row_indices, rows)]
    rows = ["  ".join(row) for row in rows]
    rows = ["".join(["    "] + [str(ci).rjust(3, " ") for ci in col_indices])] + rows
    return "\n".join(rows)


def find_bounding_dimensions(elf_locs):
    rvals, cvals = zip(*elf_locs)
    return max(rvals) - min(rvals) + 1, max(cvals) - min(cvals) + 1


def move_elves(moves, current_elf_locs):
    new_elf_locs = current_elf_locs.copy()
    for curr_loc, new_loc in moves:
        new_elf_locs.remove(curr_loc)
        new_elf_locs.add(new_loc)
    return new_elf_locs


def propose_moves(elf_locs, move_funcs):
    positions = [
        (elf, propose_move_for_elf(elf, elf_locs, move_funcs)) for elf in elf_locs
    ]
    return [p for p in positions if p[1]]


def check_north(elf, elf_locs):
    r, c = elf
    # Check north
    if all(loc not in elf_locs for loc in [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)]):
        return (r - 1, c)
    return None


def check_south(elf, elf_locs):
    r, c = elf
    # Check south
    if all(loc not in elf_locs for loc in [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]):
        return (r + 1, c)
    return None


def check_west(elf, elf_locs):
    r, c = elf
    # Check west
    if all(loc not in elf_locs for loc in [(r - 1, c - 1), (r, c - 1), (r + 1, c - 1)]):
        return (r, c - 1)
    return None


def check_east(elf, elf_locs):
    r, c = elf
    # Check east
    if all(loc not in elf_locs for loc in [(r - 1, c + 1), (r, c + 1), (r + 1, c + 1)]):
        return (r, c + 1)
    return None


def propose_move_for_elf(elf, elf_locs, move_funcs):
    r, c = elf
    # If there are NO adjacent elves in any position, return None
    if all(loc not in elf_locs for loc in all_neighbors(r, c)):
        return None

    for mf in move_funcs:
        result = mf(elf, elf_locs)
        if result:
            return result

    # What happens in this case? No move, I guess
    return None


def all_neighbors(r, c):
    return [
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1),
        (r, c + 1),
        (r + 1, c + 1),
        (r + 1, c),
        (r + 1, c - 1),
        (r, c - 1),
    ]


def parse_board(text):
    elf_locs = set()
    for r, line in enumerate(text.split("\n")):
        for c, char in enumerate(line):
            if char == "#":
                elf_locs.add((r, c))
    return elf_locs


if __name__ == "__main__":
    main()
