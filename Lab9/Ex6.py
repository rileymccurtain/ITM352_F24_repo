# Read a file of questions and answers and save it as a dictionary

import json

# Open the JSON file and load its content
with open('quiz.json', 'r') as DictFile:
    data = json.load(DictFile)
    
# The "data" variable now holds the dictionary of questions
print("The question dictionary is:")
print(data)