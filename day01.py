with open("input/day01.txt") as f:
    text = f.read()

chunks = text.split("\n\n")
inventories = [chunk.split("\n") for chunk in chunks]
totals = [sum([int(v) for v in values]) for values in inventories]
max_elf = totals.index(max(totals))

print(f"Elf {max_elf} is carrying the most calories.")
print(f"  Total calories: {max(totals)}")
print(f"  Carrying: {inventories[max_elf]}")

sorted_totals = sorted(totals, key=lambda x: -x)
top3_total = sum(sorted_totals[:3])

print(f"The top 3 elves are carrying {top3_total} calories in total.")
print(f"  Individual totals: {sorted_totals[:3]}")
