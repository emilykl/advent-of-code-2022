
LOGGING_ENABLED = False

total_score = 0

def log(msg):
    global LOGGING_ENABLED
    if LOGGING_ENABLED:
        print(msg)

def score_round(their_move, my_move):

    score = 0

    if my_move == "X": # Rock
        score += 1
        if their_move == "C": # If they play scissors, I win
            score += 6
        elif their_move == "A": # If they play rock, it's a draw
            score += 3
        # Else, I lose (add 0 to score)
    elif my_move == "Y": # Paper
        score += 2
        if their_move == "A": # If they play rock, I win
            score += 6
        elif their_move == "B": # If they play paper, it's a draw
            score +=3
        # Else, I lose (add 0 to score)
    else: # Scissors
        score += 3
        if their_move == "B": # If they play paper, I win
            score += 6
        elif their_move == "C": # If they play scissors, it's a draw
            score += 3
        # Else, I lose (add 0 to score)
    log(f"{their_move} {my_move} : {score}", LOGGING_ENABLED)
    return score

def score_round_pt2(their_move, round_outcome):

    score = 0

    log(f"{their_move} {round_outcome}")


    if round_outcome == "X": # Lose
        log("  Outcome is X, so we must lose this round")
        if their_move == "A": # Them = rock -> me = scissors
            log("  Opponent played ROCK so we must play SCISSORS")
            score += 3
        elif their_move == "B": # Them = paper -> me = rock
            log("  Opponent played ROCK so we must play SCISSORS")
            score += 1
        else: # Them = scissors -> me = paper
            log("  Opponent played SCISSORS so we must play PAPER")
            score += 2
    elif round_outcome == "Y": # Draw
        log("  Outcome is Y, so we must draw this round")
        score += 3
        if their_move == "A": # Them = rock -> me = rock
            log("  Opponent played ROCK so we must play ROCK")
            score += 1
        elif their_move == "B": # Them = paper -> me = paper
            log("  Opponent played PAPER so we must play PAPER")
            score += 2
        else: # Them = scissors -> me = scissors
            log("  Opponent played SCISSORS so we must play SCISSORS")
            score += 3
    else: # Win
        log("  Outcome is Z, so we must win this round")
        score += 6
        if their_move == "A": # Them = rock -> me = paper
            log("  Opponent played ROCK so we must play PAPER")
            score += 2
        elif their_move == "B": # Them = paper -> me = scissors
            log("  Opponent played PAPER so we must play SCISSORS")
            score += 3
        else: # Them = scissors -> me = rock
            log("  Opponent played SCISSORS so we must play ROCK")
            score += 1

    log(f"  score = {score}")

    return score


with open("input/day02.txt") as f:
    for line in f:
        theirs, outcome = line.strip().split(" ")
        total_score += score_round_pt2(theirs, outcome)

print(f"My total score: {total_score}")