def fully_contains(a1, a2):

    a1_start, a1_end = a1.split("-")
    a2_start, a2_end = a2.split("-")

    if (int(a1_start) <= int(a2_start) and int(a1_end) >= int(a2_end)) or (
        int(a2_start) <= int(a1_start) and int(a2_end) >= int(a1_end)
    ):
        print(f"Pairing {a1} : {a2} is fully contained!")
        return True
    return False


def has_overlap(a1, a2):

    a1_start, a1_end = a1.split("-")
    a2_start, a2_end = a2.split("-")

    overlap = set(range(int(a1_start), int(a1_end) + 1)).intersection(
        range(int(a2_start), int(a2_end) + 1)
    )

    if len(overlap) > 0:
        print(f"Pairing {a1} : {a2} has overlap!")
        return True
    return False


# Part One solution
with open("input/day04.txt") as f:

    lines = f.read().split("\n")

    # Part One solution
    results = [fully_contains(*line.strip().split(",")) for line in lines]
    total = len([1 for r in results if r])
    print(f"Total number of fully contained: {total}")

    # Part Two solution
    results = [has_overlap(*line.strip().split(",")) for line in lines]
    total = len([1 for r in results if r])
    print(f"Total number with overlap: {total}")

    print(f"Total number of pairings: {len(results)}")
