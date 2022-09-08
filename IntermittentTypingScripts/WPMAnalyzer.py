import csv, os

inputDir = "Input/Studies"
outputDir = "Output"
task = "TYPE_TASK"
start = "START"
done = "DONE"

pidDataMap = {};

conditionMeanMap = {
    "None": [],
    "Keyboard": [],
    "KeyboardHands": [],
    "Passthrough": []
}

# Converts enum condition identifier to corresponding string
def convertCondition(conditionNum):
    match conditionNum:
        case "0":
            return "None"
        case "1":
            return "Keyboard"
        case "2":
            return "KeyboardHands"
        case _:
            return "Passthrough"

# Logs time taken per trial for keyboard unlock task per participant and condition under test
def extractCpmData(participantLogReader):
    participantConditionMap = {
        "None": [],
        "Keyboard": [],
        "KeyboardHands": [],
        "Passthrough": []
    }
    wordLength = 0
    for row in participantLogReader:
        if len(row) > 0 and row[1] == task:
            if row[3] == start:
                startTime = row[0]
            elif startTime != None and row[3] == done:
                diffTime = float(row[0]) - float(startTime)
                # Characters per minute formula
                cpm = ((wordLength)/diffTime) * 60
                participantConditionMap[convertCondition(row[2])].append(cpm)
                startTime = None
                wordLength = 0
            elif startTime != None and row[1] == task:
                wordLength += 1

    return participantConditionMap

def extractConditionMeanPerParticipant():
    for pid in pidDataMap:
        for condition in pidDataMap[pid]:
            mean = sum(pidDataMap[pid][condition])/len(pidDataMap[pid][condition])
            conditionMeanMap[condition].append(mean)

# Iterate through input directory .csv files
for file in os.listdir(inputDir):
    with(open(os.path.join(inputDir, file), 'r')) as log:
        # Determine participant id from file name
        pid = file.split('_')[0]

        # Remove column headers line
        log.readline()

        # Read .csv content
        reader = csv.reader(log)
        startTime = None 
        currCondition = None

        # Map keyboard unlock data per condition
        pidDataMap[pid] = extractCpmData(reader)

extractConditionMeanPerParticipant()
    
with open(os.path.join(outputDir, "CPM_Mean_Per_Participant.csv"), 'w') as f:
    writer = csv.writer(f)
    header = ["Condition", "Characters per Minute"]
    writer.writerow(header)

    res = []
    none = conditionMeanMap["None"]
    kb = conditionMeanMap["Keyboard"]
    kbh = conditionMeanMap["KeyboardHands"]
    pst = conditionMeanMap["Passthrough"]
    count = 0

    for val in none:
        writer.writerow(["None", val])

    for val in kb:
        writer.writerow(["Keyboard", val])

    for val in kbh:
        writer.writerow(["KeyboardHands", val])

    for val in pst:
        writer.writerow(["Passthrough", val])

    # while count < 20:
    #     writer.writerow([none[count], kb[count], kbh[count], pst[count]])
    #     count += 1

    for condition in conditionMeanMap:
        conditionMean = sum(conditionMeanMap[condition])/len(conditionMeanMap[condition])
        print(f"Condition: {condition}, Mean: {conditionMean}")
