# Advent of Code 2022 - Day 10 solution


def main():
    with open("input/day10.txt") as f:
        instructions = f.read().split("\n")

        # The value at index N in register_values
        # represents the value DURING the (N+1)th cycle.
        # For example, the value at index 0 represents
        # the value DURING the first cycle.
        # The value at index 1 represents the value
        # DURING the second cycle.
        register_values = [1]

        # Execute each instruction, and build a list of register values
        for instruction in instructions:
            command, arg = parse_instruction(instruction)
            register_values = execute_instruction(command, arg, register_values)

        # Compute answer to Part One
        interesting_values = list(
            [
                value_during_cycle(n, register_values) * n
                for n in [20, 60, 100, 140, 180, 220]
            ]
        )
        part_one_answer = sum(interesting_values)
        print(f"(Part One) The sum of the six signal strengths is: {part_one_answer}")

        # Compute answer to Part Two
        print(f"(Part Two) Rendered CRT display below:")
        render_crt(register_values)


def parse_instruction(instruction):
    pieces = instruction.split(" ")
    if pieces[0] == "addx":
        return pieces[0], int(pieces[1])
    elif pieces[0] == "noop":
        return pieces[0], None
    else:
        raise ValueError(f"Unrecognized command `{pieces[0]}`")


def execute_instruction(command, arg, register_values):
    new_register_values = register_values.copy()
    if command == "noop":
        new_register_values.append(register_values[-1])
    elif command == "addx":
        # First, one cycle where nothing happens
        new_register_values.append(register_values[-1])
        # Then, we add the arg value to the register value
        new_register_values.append(register_values[-1] + arg)
    return new_register_values


# Given a list of register values and a cycle number `n`,
# return the value of the register DURING cycle n.
def value_during_cycle(n, register_values):
    # As stated above, the value at index N in register_values
    # represents the value DURING the (N+1)th cycle.
    # Therefore, to get the value during cycle `n`, we must
    # return the value at index `n-1` in register_values.
    return register_values[n - 1]


def render_crt(register_values, width_px=40, height_px=6):
    rows = [
        "".join(
            [
                get_pixel(register_values, row=i, col=j, width_px=width_px)
                for j in range(width_px)
            ]
        )
        for i in range(height_px)
    ]
    print("\n".join(rows))


def get_pixel(register_values, row, col, width_px):

    # Calculate during what cycle the pixel at the given row and col is being drawn
    cycle_num = row * width_px + col + 1

    # Get the register value during that cycle
    register_value = value_during_cycle(cycle_num, register_values)

    # If the difference between the register value and the given col is 1 or less,
    # pixel is lit (`#`); otherwise it is dark (`.`).
    if abs(register_value - col) <= 1:
        return "#"
    else:
        return "."


if __name__ == "__main__":
    main()
