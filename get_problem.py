import datetime
import os
import sys 

from bs4 import BeautifulSoup
import requests

def main():

    # If day is passed as command-line argument, get problem for that day,
    # otherwise get problem for current day
    if len(sys.argv) > 1:
        day = sys.argv[1]
    else:
        # Get the current day
        day = datetime.datetime.now().day

    # Get problem and save to file `problems/dayDD.txt`
    get_problem(day)

    # Create boilerplate file `dayDD.py` for solution
    make_solution_file(day)

    # Ideally, I want to also get the input file and save to `input/dayDD.txt`.
    # Haven't figured out how to do that yet though


# Get problem and save to file `problems/dayDD.txt`
def get_problem(day):

    # Parse the HTML
    response = requests.get(f"https://adventofcode.com/2022/day/{day}")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Get all elements with the class `day-desc`
    # This will get the problem for Part One, and also for Part Two
    # if already revealed
    elements = soup.find_all(class_="day-desc")

    # Get the text inside the elements
    problem_text = "\n".join([element.text for element in elements])

    # Fix up the formatting a little
    problem_text = problem_text.replace(" ---", " ---\n")
    problem_text = problem_text.replace("\n", "\n\n")
    problem_text = problem_text.replace("\n\n\n\n", "\n\n")

    # Write to file
    # Note: This will overwrite the existing problem file ONLY if
    # the new text is longer than the existing text 
    file_path = f"problems/day{day:0>2}.txt"

    if os.path.exists(file_path):
        with open(file_path) as f:
            if len(problem_text) >= len(f.read()):
                overwrite = True
            else:
                overwrite = False
    else:
        overwrite = True

    if overwrite:
        with open(file_path, "w") as f:
            f.write(problem_text)
        print(f"Day {day} problem statement written to {file_path}.")
    else:
        print(f"File {file_path} already exists with longer text content. Not overwriting.")

def make_solution_file(day):

    file_path = f"day{day:0>2}.py"

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(f"""# Advent of Code 2022 - Day {day} solution

def main():
    pass

if __name__ == "__main__":
    main()       
""")
        print(f"Created empty solution file at {file_path}.")
    else:
        print(f"Solution file already exists at {file_path}. Not overwriting.")



if __name__ == "__main__":
    main()