def create_stacks(start_state):
    start_state_lines = [s for s in start_state.split("\n") if s.strip()]
    stack_names = start_state_lines[-1].split()
    stacks = [[] for _ in stack_names]

    # Iterate through lines in reverse order, starting from
    # second-to-last line
    for i in range(len(start_state_lines) - 2, -1, -1):
        line = start_state_lines[i]
        crates = [line[j] for j in range(1, len(line), 4)]
        for k, crate in enumerate(crates):
            if crate.strip():
                stacks[k].append(crate)

    for stack_name, stack in zip(stack_names, stacks):
        print(f"{stack_name} : {stack}")

    return stacks


def parse_instruction(instruction):
    tokens = instruction.strip().split(" ")

    # Return:
    #  - number of crates to move
    #  - from which stack
    #  - to which stack
    return int(tokens[1]), int(tokens[3]), int(tokens[5])


def execute_instruction_9000(state, instruction):
    print(f"\n\n\nInstruction: {instruction}")
    crates_to_move, from_stack, to_stack = parse_instruction(instruction)

    for i in range(crates_to_move):
        crate = state[
            from_stack - 1
        ].pop()  # Subtract 1 because instructions are 1-indexed
        state[to_stack - 1].append(crate)
        print(f"New state:")
        for n, stack in enumerate(state):
            print(f"{n+1} : {stack}")

    print("")

    return state


def execute_instruction_9001(state, instruction):
    print(f"\n\n\nInstruction: {instruction}")
    crates_to_move, from_stack, to_stack = parse_instruction(instruction)

    # Identify the crates to be moved
    crates = state[from_stack - 1][-crates_to_move:]

    # Redefine the `from` stack to remove the crates
    state[from_stack - 1] = state[from_stack - 1][:-crates_to_move]

    # Append the crates to the `to` stack
    state[to_stack - 1].extend(crates)

    print(f"New state:")
    for n, stack in enumerate(state):
        print(f"{n+1} : {stack}")

    return state


def get_top_crates(state):
    top_crates = [stack[-1] for stack in state]
    return "".join(top_crates)


with open("input/day05.txt") as f:
    text = f.read()

    start_state, instructions = text.split("\n\n")

    print(start_state)

    start_state = create_stacks(start_state)
    instructions = instructions.split("\n")

    state = start_state
    for instruction in instructions:

        # Solution for Part One
        # state = execute_instruction_9000(state, instruction)

        # Solution for Part Two
        state = execute_instruction_9001(state, instruction)

    top_crates = get_top_crates(state)

    print(f"Top crates: {top_crates}")
