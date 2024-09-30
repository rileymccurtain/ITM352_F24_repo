# Iterate through a list of fares and print out a message indicating
# whether the fare is high or low.

sample_fares = [8.60, 5.75, 13.25, 21.21] 

for x in sample_fares:
    if (x > 12):
        print(f"This fare {x} is high!")
    else: 
        print(f"This fare {x} is low")