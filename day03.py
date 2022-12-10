from itertools import islice

LOGGING_ENABLED = True

total_score = 0


def log(msg):
    global LOGGING_ENABLED
    if LOGGING_ENABLED:
        print(msg)


def find_error(contents):
    log(contents)
    log(len(contents))
    first_half = contents[: int(len(contents) / 2)]
    second_half = contents[int(len(contents) / 2) :]
    log(f"  First half: {first_half}")
    log(f"  Second half: {second_half}")

    for char in first_half:
        if char in second_half:
            print(f"  Error: {char}")
            return char

    raise ValueError(f"Contents string {contents} contains no error.")


def priority(char):
    if char.upper() == char:  # Character is uppercase
        p = ord(char) - 38
    else:  # Character is lowercase
        p = ord(char) - 96
    log(f"Priority of '{char}' is {p}")
    return p


def find_common_char(list_of_contents):
    for c in list_of_contents:
        log(c)
    for char in list_of_contents[0].strip():
        if all([char in c.strip() for c in list_of_contents[1:]]):
            print(f"  Common char is: {char}")
            return char
    raise ValueError(f"No common char in {list_of_contents}")


# Solution to Part One
# with open("input/day3.txt") as f:
#     errors = [find_error(line.strip()) for line in f]
#     priorities = [priority(error) for error in errors]
#     print(f"Sum of priorities: {sum(priorities)}")

# Solution to Part Two
with open("input/day03.txt") as f:

    lines = f.read().split("\n")
    log(f"Number of lines: {len(lines)}")
    chunks = [lines[i : i + 3] for i in range(0, len(lines), 3)]

    badge_chars = [find_common_char(chunk) for chunk in chunks]
    priorities = [priority(b) for b in badge_chars]
    print(f"Sum of priorities: {sum(priorities)}")
