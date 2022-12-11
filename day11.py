# Advent of Code 2022 - Day 11 solution
import copy
import math

import numpy as np


def main():
    with open("input/day11.txt") as f:
        chunks = f.read().split("\n\n")
        monkeys = [parse_monkey_info(chunk) for chunk in chunks]

        # Calculate Part One solution
        mb_part_one = monkey_business_part_one(monkeys)
        print(f"Monkey business (Part One): {mb_part_one}")

        # Calculate Part Two solution
        mb_part_two = monkey_business_part_two(monkeys)
        print(f"Monkey business (Part Two): {mb_part_two}")


def monkey_business_part_one(monkeys):
    # Keep a list of past states
    # Each state is a list of the list of items for each monkey
    # So `states` is a list of lists of lists
    # Initial state is the starting items for each monkey
    states = [[m["starting_items"] for m in monkeys]]

    # Do 20 rounds
    for _ in range(20):
        states = do_round(monkeys, states)

    # Now, find out how many items each monkey inspected
    totals = compute_monkey_totals(states)

    # Calculate monkey business
    totals = sorted(totals, key=lambda x: -x)
    monkey_business = totals[0] * totals[1]
    return monkey_business


def monkey_business_part_two(monkeys):
    # Keep a list of past states
    # Each state is a list of the list of items for each monkey
    # So `states` is a list of lists of lists
    # Initial state is the starting items for each monkey
    states = [[m["starting_items"] for m in monkeys]]

    # Instead of dividing by 3 to relax, we mod by the monkey factor,
    # which is  the product of all the divisors for the division tests
    # of each monkey.
    # This reduces the values without affecting the result.
    monkey_factor = np.product([m["test"]["divisor"] for m in monkeys])

    # Do 10,000 rounds
    for i in range(10_000):
        states = do_round(monkeys, states, monkey_factor=monkey_factor)

    # Now, find out how many items each monkey inspected
    totals = compute_monkey_totals(states)

    # Calculate monkey business
    totals = sorted(totals, key=lambda x: -x)
    monkey_business = totals[0] * totals[1]
    return monkey_business


def compute_monkey_totals(states):
    totals = []
    for i in range(len(states[0])):
        monkey_items = [state[i] for state in states]
        monkey_total_thrown = 0
        for j in range(len(monkey_items) - 1):
            if len(monkey_items[j + 1]) == 0:
                monkey_total_thrown += len(monkey_items[j])
        totals.append(monkey_total_thrown)
    return totals


def print_monkey_totals(totals):
    for i, t in enumerate(totals):
        print(f"  Monkey {i} has thrown {t} items")


def do_round(monkeys, states, monkey_factor=None):
    for m, monkey in enumerate(monkeys):
        states = monkey_turn(monkey, states, monkey_factor=monkey_factor)
    return states


def monkey_turn(monkey, states, monkey_factor):
    new_state = copy.deepcopy(states[-1])

    monkey_index = monkey["index"]

    for item in new_state[monkey_index]:
        # Inspect item (apply monkey operator)
        inspected = operate(
            item,
            monkey["operation"]["op"],
            monkey["operation"]["value"],
        )
        # Relax (divide by 3), if relax is True
        if not monkey_factor:
            relaxed = math.floor(inspected / 3)
        # Otherwise, we keep values down by modding
        # This doesn't affect the result (I think)
        else:
            relaxed = inspected % monkey_factor
        # Perform division test
        if relaxed % monkey["test"]["divisor"] == 0:
            throw_to_index = monkey["test"]["if_true"]
        else:
            throw_to_index = monkey["test"]["if_false"]
        # Append to list of new monkey
        new_state[throw_to_index].append(relaxed)
    # Remove all items from current monkey
    new_state[monkey_index] = []

    # Return states list with new state added
    return states + [new_state]


def parse_monkey_info(chunk):
    lines = [line.strip() for line in chunk.split("\n")]
    monkey_info = {
        "index": int(lines[0].split("Monkey ")[1][:-1]),
        "starting_items": [
            int(x) for x in lines[1].split("Starting items: ")[1].split(", ")
        ],
        "operation": parse_operation(lines[2]),
        "test": parse_test(lines[3:]),
    }
    return monkey_info


def parse_test(lines):
    divisor = int(lines[0].split("Test: divisible by ")[1])
    if_true = int(lines[1].split("If true: throw to monkey ")[1])
    if_false = int(lines[2].split("If false: throw to monkey ")[1])
    return {
        "divisor": divisor,
        "if_true": if_true,
        "if_false": if_false,
    }


def parse_operation(line):
    line = line.split("Operation: new = old ")[1]
    operator, value_str = line.split(" ")

    if value_str == "old":
        operator = "**"
        value = 2

    else:
        value = int(value_str)

    return {"op": operator, "value": value}


def operate(value1, op, value2):
    if op == "+":
        return value1 + value2
    elif op == "*":
        return value1 * value2
    elif op == "**":
        return value1**value2
    else:
        raise ValueError(f"Invalid operator `{op}`")


def print_state(state):
    for i, items in enumerate(state):
        print(f"  Monkey {i}: {items}")
    print("")


if __name__ == "__main__":
    main()
