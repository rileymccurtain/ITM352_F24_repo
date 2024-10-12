# Student ID = 27770625
# 1. Write the history of scores out to a file. 
# 2. Notify the user when they get a new high score.

# A dictionary with questions accompanied by the corresponding answers.

QUESTIONS = {
    "Which is the largest island of Japan?": {
        "options": ["a) Hokkaido", "b) Kyushu", "c) Honshu", "d) Shikoku"],
        "correct": "c"
    },
    "What is the tallest mountain in Japan?": {
        "options": ["a) Mount Fuji", "b) Mount Kita", "c) Mount Haku", "d) Mount Asama"],
        "correct": "a"
    },
    "Which sea lies to the east of Japan?": {
        "options": ["a) Sea of Japan", "b) Pacific Ocean", "c) Bering Sea", "d) East China Sea"],
        "correct": "b"
    },
    "Which river is the longest in Japan?": {
        "options": ["a) Tone River", "b) Kiso River", "c) Yamato River", "d) Shinano River"],
        "correct": "d"
    },
    "What is the name of the famous volcano located near Tokyo?": {
        "options": ["a) Mount Fuji", "b) Mount Aso", "c) Mount Sakurajima", "d) Mount Unzen"],
        "correct": "a"
    },
    "What type of natural disaster is Japan most famous for experiencing?": {
        "options": ["a) Earthquakes", "b) Tsunamis", "c) Volcanoes", "d) Typhoons"],
        "correct": "a"
    },
    "Which Japanese island is known for its hot springs (onsen)?": {
        "options": ["a) Hokkaido", "b) Kyushu", "c) Okinawa", "d) Honshu"],
        "correct": "b"
    },
    "What is the name of the traditional Japanese architecture characterized by wooden structures?": {
        "options": ["a) Pagoda", "b) Castle", "c) Shrine", "d) Teahouse"],
        "correct": "a"
    },
    "What is the predominant language spoken in Japan?": {
        "options": ["a) Chinese", "b) Korean", "c) English", "d) Japanese"],
        "correct": "d"
    },
    "Which city is known as the 'Gateway to Japan'?": {
        "options": ["a) Tokyo", "b) Osaka", "c) Yokohama", "d) Nagoya"],
        "correct": "c"
    }
}

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
    quiz(QUESTIONS)