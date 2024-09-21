# Create a list of trip durations and fares

tripDuration = [1.1, 0.8, 2.5, 2.6]
tripFares = ("$6.25", "$5.25", "$10.50", "$8.05")

tripDict = {"miles": tripDuration, 
            "fares": tripFares}

print(tripDict)
print(tripDict["miles"][2], tripDict["fares"][2])

# Create a new dictionary by zipping together the duration list and the fares tuple
newDict = dict(zip(tripDuration, tripFares))
print("New dict=", newDict)
print(f"Trip duration={tripDuration[2]} cost={newDict[tripDuration[2]]}")