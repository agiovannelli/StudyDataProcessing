import csv, os

outputDir = "Output"
updatedRows = []

# Determines shift amount based on pid mod 4 result
def determineLabel(str):
    num = int(str)
    if num == 1:
        return "Most preferred"
    elif num == 2:
        return "More preferred"
    elif num == 3:
        return "Less preferred"
    elif num == 4:
        return "Least preferred"

with(open('Input/interview_rankings.csv', 'r')) as sqcsv:
    # Remove column headers line
    sqcsv.readline()

    # Read .csv content
    reader = csv.reader(sqcsv)
    
    for row in reader:
        updatedRow = []
        for col in row:
            # updatedRow.append(determineLabel(col))
            updatedRow.append(col)
        updatedRows.append(updatedRow)


with open(os.path.join(outputDir, "Rankings_Per_Participant.csv"), 'w') as f:
    # Create the csv writer
    writer = csv.writer(f)
    header = ["Condition", "Ranking"]
    writer.writerow(header)

    totalRows = len(updatedRows)

    i = 0
    while i < totalRows:
        writer.writerow(["None", updatedRows[i][0]])
        i += 1

    i = 0
    while i < totalRows:
        writer.writerow(["Keyboard", updatedRows[i][1]])
        i += 1

    i = 0
    while i < totalRows:
        writer.writerow(["KeyboardHands", updatedRows[i][2]])
        i += 1

    i = 0
    while i < totalRows:
        writer.writerow(["Passthrough", updatedRows[i][3]])
        i += 1

    # for row in updatedRows:
    #     writer.writerow(row)