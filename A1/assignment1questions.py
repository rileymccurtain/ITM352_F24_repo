import json

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

# Specify the name of the JSON file.
filename = "japanquiz.json"

# Open the file in write mode and save the dictionary as JSON.
with open(filename, "w") as DictFile:
    json.dump(QUESTIONS, DictFile, indent=4)

print(f"Data has been written to {filename}")

# Read a file of questions and answers and save it as a dictionary.

import json

# Open the JSON file and load its content.
with open('japanquiz.json', 'r') as DictFile:
    data = json.load(DictFile)
    
# The "data" variable now holds the dictionary of questions.
print("The question dictionary is:")
print(data)