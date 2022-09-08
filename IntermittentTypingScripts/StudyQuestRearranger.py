import collections, csv, os

outputDir = "Output"
reorderedDict = {}

# Determines shift amount based on pid mod 4 result
def determineShiftAmount(startNum):
    modResult = int(startNum) % 4
    if modResult == 1:
        return 0
    elif modResult == 2:
        return 16
    elif modResult == 3:
        return 32
    elif modResult == 0:
        return 48

with(open('Input/Study Questionnaires.csv', 'r')) as sqcsv:
    # Remove column headers line
    sqcsv.readline()

    # Read .csv content
    reader = csv.reader(sqcsv)
    for row in reader:
        # Get pid, remove unnecessary columns
        pid = row[2]
        row = row[3:]
        
        # Create shiftable data structure instance, shift according to pid
        shiftableStruct = collections.deque(row)
        shiftAmount = determineShiftAmount(pid)
        shiftableStruct.rotate(shiftAmount)
        shiftedList = list(shiftableStruct)

        # Place shifted list into global dictionary
        reorderedDict[pid] = shiftedList

with open(os.path.join(outputDir, "study_quest_reorder.csv"), 'w') as f:
    # Create the csv writer
    writer = csv.writer(f)

    # Iterate participant identifiers for keyboard unlock mean value per condition
    for pid in reorderedDict:
        writer.writerow(reorderedDict[pid])