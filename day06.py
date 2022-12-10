def is_valid_marker(marker):
    if len(set(marker)) == len(marker):
        print(f"{marker} is a valid marker!")
        return True
    else:
        # print(f"{marker} is not a valid marker")
        return False


with open("input/day06.txt") as f:
    text = f.read()

    # Solution to Part One
    for i in range(len(text) - 4):
        marker = text[i : i + 4]
        if is_valid_marker(marker):
            print(f"First start-of-packet marker is complete after {i+4} characters.")
            break

    # Solution to Part Two
    for i in range(len(text) - 14):
        marker = text[i : i + 14]
        if is_valid_marker(marker):
            print(f"First start-of-message marker is complete after {i+14} characters.")
            break
