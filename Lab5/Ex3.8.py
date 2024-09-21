# Define a list of survey response values (5, 7, 3, and 8) and store them in a
# variable. Next define a tuple of respondent ID values (1012, 1035, 1021, and 1053).


responseValues = [5, 7, 3, 8]
respondentIDs = (1012, 1035, 1021, 1053)


responseValues.append(respondentIDs)
print(responseValues)

# Create a dictionary with ID values as the keys and survey 
# responses as the values using zip().

responseValues = [5, 7, 3, 8]
respondentIDs = (1012, 1035, 1021, 1053)

survey = dict(zip(respondentIDs, responseValues))
print("Dict =", survey)