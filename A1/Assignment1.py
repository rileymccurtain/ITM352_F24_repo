import json

# Load questions from a JSON file.
def load_questions(filename):
    try:
        with open('japanquiz.json', 'r') as f:
            questions = json.load(f)
            return questions
    except FileNotFoundError:
        print(f"Error: The file '{'japanquiz.json'}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file '{'japanquiz.json'}' contains invalid JSON.")
        return {}

# Keep track of each score.
def log_score(score, total_questions):
    with open("quiz_scores.txt", "a") as f:
        f.write(f"Score: {score}/{total_questions}\n")

# Get the highest score.
def get_high_score():
    try:
        with open("quiz_scores.txt", "r") as f:
            scores = [line.split(": ")[1].strip().split("/")[0] for line in f.readlines()]
            return max(map(int, scores)) if scores else 0
    except FileNotFoundError:
        return 0

# Maintain a current record of the quiz’s high scores.
def quiz(questions):
    score = 0
    total_questions = len(questions)
    high_score = get_high_score()

    print(f"Current High Score: {high_score}\n")

    for question, data in questions.items():
        print(f"\n{question}")
        for option in data["options"]:
            print(option)

        # Verify the user’s input to ensure that it is within the set limits.
        while True:
            answer = input("Select the letter of your answer (a-d): ").lower()
            if answer in ['a', 'b', 'c', 'd']:
                break
            else:
                print("Invalid input. Please enter a letter between a and d.")

        # Indicate whether the user’s input is correct.
        if answer == data["correct"]:
            print("Correct!")
            score += 1
        else:
            print("Incorrect!")

    # Obtain and reveal the final score. 
    print(f"\nQuiz completed! Your final score is {score} out of {total_questions}.")
    
    # Record the score to a file.
    log_score(score, total_questions)

    # Inform the user when a new high score is reached. 
    if score > high_score:
        print("Well done! A new high score has been set!")

if __name__ == "__main__":
    # Retrieve queries based on a JSON file. 
    questions = load_questions('japanquiz.json')
    if questions:
        quiz(questions)