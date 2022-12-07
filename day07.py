# Advent of Code 2022 - Day 7 solution

import json
import os

def main():

    state = "", {}

    with open("input/day07.txt") as f:

        # Process input text to get file structure with sizes
        chunks = split_into_chunks(f.read())
        for chunk in chunks:
            state = update_state(state, chunk)

        # Use file structure info to get sizes of all directories
        all_dir_sizes = calculate_all_dir_sizes(state[1])

        # Filter out directories with size > 100000
        filtered_dir_sizes = [item for item in all_dir_sizes if item[1] <= 100000]

        # Sum sizes of filtered directories
        sizes_sum = sum([item[1] for item in filtered_dir_sizes])

        # Print answer to Part One
        print(f"Sum: {sizes_sum}")

        # Calculate available disk space
        root_dir_size = [item[1] for item in all_dir_sizes if item[0] == "/"][0]
        available_space = 70000000 - root_dir_size
        print(f"Root dir size: {root_dir_size}")
        print(f"Available space: {available_space}")

        # Calculate additional space needed to run upgrade
        addl_space_needed = 30000000 - available_space
        print(f"Additional space needed: {addl_space_needed}")

        # Find size of smallest directory larger than `addl_space_needed`
        filtered_dir_sizes_pt_2 = [
            item for item in all_dir_sizes 
            if item[1] >= addl_space_needed
        ]
        size_of_dir_to_delete = min([item[1] for item in filtered_dir_sizes_pt_2])

        # Print answer to Part Two
        print(f"Size of dir to delete: {size_of_dir_to_delete}")

def print_state(state):
    curr_path, curr_size_info = state

    print(f"path: {curr_path}\n")
    print(f"size_info:")
    print(
        json.dumps(curr_size_info,sort_keys=True, indent=4)
    )
    print("")


def split_into_chunks(text):
    lines = text.split("\n")

    # Get lines starting with `$`, representing user input
    # Append index of the line following the last line, to make logic work
    user_input_lines = [i for i, line in enumerate(lines) if line.startswith("$")]
    user_input_lines.append(len(lines))
    
    # Split into chunks, where each chunk consists of a user input
    # followed by the terminal output
    return [
        lines[start:end] for start, end 
        in zip(user_input_lines, user_input_lines[1:])
    ]

# Update the current state based on the info in `chunk`
def update_state(state, chunk):

    curr_path, curr_size_info = state

    chunk_type = get_chunk_type(chunk)

    # Process `cd` command
    if chunk_type == "cd":

        # Size info doesn't change
        new_size_info = curr_size_info.copy()

        # Change current directory state
        new_dirname = chunk[0].split(" ")[2]
        if new_dirname == "..":
            new_path = curr_path[:-1]
        elif new_dirname == "/":
            new_path = ["/"]
        else:
            new_path = curr_path + [new_dirname]
    
    # Process `ls` command
    elif chunk_type == "ls":

        # Current path doesn't change
        new_path = curr_path.copy()

        # Copy sizes dictionary, then drill down until 
        # you get to current path
        new_size_info = curr_size_info.copy()
        dir_pointer = new_size_info
        for item in curr_path:
            if not item in dir_pointer:
                dir_pointer[item] = {}
            dir_pointer = dir_pointer[item]

        # Add size info for every line of the `ls` output
        for line in chunk[1:]:
            size, filename = line.split(" ")
            if not size == "dir":
                dir_pointer[filename] = int(size)

    return new_path, new_size_info


# Check what user command we're processing
def get_chunk_type(chunk):
    return chunk[0].split(" ")[1]

# Calculate all dir sizes, given structured dict of all file sizes
def calculate_all_dir_sizes(size_info, curr_path="", dir_sizes=[]):
    _, dir_size_master_list = dir_size("/", size_info["/"], [])
    return dir_size_master_list

# Recursive function for calculating total size of directory given contents
def dir_size(dir_path, contents, dir_size_master_list):
    size = 0
    dir_size_master_list = dir_size_master_list.copy()

    for filename, size_or_contents in contents.items():
        if isinstance(size_or_contents, int):
            size += size_or_contents
        else:
            # This is ugly, but I don't feel like fixing it right now
            if dir_path in ["", "/"]:
                subdir_path = dir_path + filename
            else:
                subdir_path = f"{dir_path}/{filename}" if dir_path else filename

            subdir_size, dir_size_master_list = dir_size(
                subdir_path, 
                size_or_contents,
                dir_size_master_list
            )
            size += subdir_size
    dir_size_master_list.append((dir_path, size))
    return size, dir_size_master_list

if __name__ == "__main__":
    main()       
