# Interactive quiz game where each question has four possible answers.
# Make QUESTIONS a dictionary.
# Allow the user to select the correct answer by its label.

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "11", "8", "14"],
    "What is the capital of Texas": ["Austin", "San Antonio", "Dallas", "Houston"],
    "The Last Supper was painted by which artist": ["Da Vinci", "Rembrandt", "Picasso", "Michelangelo"]
}

for question, alternatives in QUESTIONS.items():
    correct_answer = alternatives[0]
    sorted_alternatives = sorted(alternatives)
    for label, alternative in enumerate(sorted_alternatives):
        print(f"{label}: {alternative}")
    
    answer_label = int(input(f"{question}? "))
    answer = sorted_alternatives[answer_label]

    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The correct answer is {correct_answer!r}, not {answer!r}")