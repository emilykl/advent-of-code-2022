# Advent of Code 2022 - Day 13 solution

from functools import cmp_to_key

import json

verbose = True


def log(msg):
    if verbose:
        print(msg)


def main():
    with open("input/day13.txt") as f:

        # Part One
        chunks = f.read().split("\n\n")
        pairs = [chunk.split("\n") for chunk in chunks]
        packet_pairs = [(json.loads(p[0]), json.loads(p[1])) for p in pairs]

        correct = []
        for i, (p1, p2) in enumerate(packet_pairs):
            log(f"============ Pair {i+1} ============")
            if correct_order(p1, p2) == 1:
                log(f"* Pair {i+1} is in the right order *")
                correct.append(i + 1)
            elif correct_order(p1, p2) == -1:
                log(f"* Pair {i+1} is NOT in the right order *")
            else:
                # Will this ever happen? I hope not. Alg is not defined for this case.
                raise ValueError(f"Impossible to determine order of {p1} and {p2}.")
            log("====================================")

        print(f"Sum (Part One answer): {sum(correct)}")

    # Part Two
    with open("input/day13.txt") as f:
        packets = [json.loads(line) for line in f.read().split("\n") if line]

        # Add divider packets
        divider_packets = [[[2]], [[6]]]
        packets.extend(divider_packets)

        # Sort
        packets.sort(key=cmp_to_key(correct_order))

        # For some reason the list is in reverse order, so reverse it
        packets.reverse()

        indices = [packets.index(d) + 1 for d in divider_packets]
        log(f"Indices of divider packets: {indices}")
        print(f"Decoder key (Part Two answer): {indices[0] * indices[1]}")


# Returns 1 if the two are in the correct order, -1 if they are not, and 0
# if the correct order is indeterminate (i.e. they are equal)
def correct_order(left, right):

    # Case: Both are ints
    if type(left) == int and type(right) == int:
        log(f"{left} and {right} are both ints")
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0

    # Case: Left is int, right is list
    elif type(left) == int and type(right) == list:
        log(f"{left} is an int, {right} is a list")
        # Wrap left inside a list and recurse
        return correct_order([left], right)

    # Case: Left is list, right is int
    elif type(left) == list and type(right) == int:
        log(f"{left} is a list, {right} is an int")
        # Wrap right inside a list and recurse
        return correct_order(left, [right])

    # Case: Both are lists
    if type(left) == list and type(right) == list:
        log(f"{left} and {right} are both lists")
        for idx in range(max(len(left), len(right))):

            # If we've gone past the end of one list, we know the ordering
            if idx == len(left):
                return 1
            elif idx == len(right):
                return -1

            # Otherwise, recurse and return correct_order if conclusive
            if correct_order(left[idx], right[idx]) in [-1, 1]:
                return correct_order(left[idx], right[idx])

        # If we've reached the end of the lists without an answer, return 0
        return 0


# Logically equivalent to the above function (I think), but with more comments and print statments
def correct_order_verbose(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            # Both are ints
            if left < right:
                log(f"{left} and {right} are both ints, and {left} < {right}. Returning 1.")  # fmt: skip
                return 1
            elif left > right:
                log(f"{left} and {right} are both ints, and {left} > {right}. Returning -1.")  # fmt: skip
                return -1
            else:
                log(f"{left} and {right} are both ints, and {left} = {right}. Returning 0. (Indeterminate)")  # fmt: skip
                return 0
        else:
            # Left is int, right is list
            log(f"{left} is an int and {right} is a list. Comparing {[left]} and {right}.")  # fmt: skip
            return correct_order([left], right)
    else:
        if isinstance(right, int):
            # Left is list, right is int
            log(f"{left} is a list and {right} is an int. Comparing {left} and {[right]}.")  # fmt: skip
            return correct_order(left, [right])
        else:
            # Both are lists
            log(f"Comparing corresponding items in {left} and {right}...")
            for idx in range(max(len(left), len(right))):

                if idx == len(left):
                    if idx < len(right):
                        log("...End of left list reached, but right list still has items. Returning 1.")  # fmt: skip
                        return 1
                    else:
                        break
                elif idx == len(right):
                    if idx < len(left):
                        log("...End of right list reached, but left list still has items. Returning -1.")  # fmt: skip
                        return -1
                    else:
                        break

                result = correct_order(left[idx], right[idx])
                if result == 1:
                    log(f"...{left[idx]} and {right[idx]} are in the correct order, so returning 1.")  # fmt: skip
                    return 1
                elif result == -1:
                    log(f"...{left[idx]} and {right[idx]} are not in the correct order, so returning -1.")  # fmt: skip
                    return -1
                else:
                    log(f"...{left[idx]} = {right[idx]}, so continuing on to look at the next item in the list.")  # fmt: skip

            # What happens if we reach the end of the list and haven't made a decision?
            log(f"...{left} and {right} have indetermine ordering, so returning 0.")
            return 0


if __name__ == "__main__":
    main()
