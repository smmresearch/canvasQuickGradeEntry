import pandas as pd
import numpy as np
import re
import sys
canvas_file="canvasBaseS24.csv"
grade_name = input("Assignment name:\n")
points = float(input("\nPoints possible: \n"))
canvas_df = pd.read_csv(canvas_file)
# Cut out the first row for later
canvas_df = canvas_df[['Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Section']]
canvas_df[grade_name] = np.nan
canvas_df.loc[0,grade_name] = points
#print(canvas_df)
nameMatches = dict()
options = ["finish", "undoit", "viewit", "restZero"]

#0th row is Points possible
#re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
for i in range(1,len(canvas_df)):
    #Groups Last name 1 last name 2, first name 1 first name 2 first name 3
    r = re.match(r"([A-Z][A-Za-z]*)(?:[- ]([A-Z][A-Za-z]*))?, ?([A-Z][A-Za-z]*)(?:[- ]([A-Z][A-Za-z]*))?(?:[- ]([A-Z][A_Za-z]*))?",canvas_df['Student'][i])
    orderedNames = [r.group(3),r.group(4),r.group(5),r.group(1),r.group(2)]
    for nameI in range(5):
        if orderedNames[nameI] is not None:
            orderedNames[nameI] = str.lower(orderedNames[nameI])
    #lasts = [r.group(i) for i in range(1,5) if r.group(i) is not None]
    #firsts = [r.group(i) for i in range(2,6) if r.group(i) is not None]
    for fIdx in range(0,4):
        f = orderedNames[fIdx]
        if f is None:
            continue
        for lIdx in range(fIdx+1,5):
            l = orderedNames[lIdx]
            if l is None:
                continue
            for firstL in range(1,6):
                for lastL in range(1,6):
                    nameShort = f[0:firstL] + l[0:lastL]
                    if nameShort in options:
                        continue
                    if nameShort not in nameMatches or (nameMatches[nameShort]==i):
                        nameMatches[nameShort] = i
                    else:
                        if firstL+lastL>=3:
                            print("WARNING: name clash for "+nameShort)
                        nameMatches[nameShort] = -1
            nameShort = f+l
            if nameShort in options:
                continue
            if nameShort not in nameMatches or (nameMatches[nameShort]==i):
                nameMatches[nameShort] = i
            nameShort = f
            if nameShort in options:
                continue
            if nameShort not in nameMatches or (nameMatches[nameShort]==i):
                nameMatches[nameShort] = i
            else:
                nameMatches[nameShort] = -1

#print(canvas_df['Student'])
prevIdx = np.nan
prevScore = np.nan
while(True):
    inputS = input(f"\nNext student (1-4 letters of each first and last, no capitalization or space). Otherwise choose: {options}\n")
    split = str.split(inputS)
    if len(split)>1:
        print("no spaces")
    if split[0] == "finish":
        break
    if split[0] == "undoit":
        try:
            canvas_df.loc[prevIdx,grade_name]=prevScore
            continue
        except:
            print("undo failed")
            continue
    if split[0] == "restZero":
        canvas_df.loc[pd.isna(canvas_df[grade_name]),grade_name] = 0
        print("Set the rest zero")
        continue
        #print(canvas_df)
    if split[0] == "viewit":
        print(canvas_df)
        continue
    nameShort = str.lower(split[0])
    try:
        # print(nameShort)
        # print(nameMatches)
        idx = nameMatches[nameShort]
        if idx == -1:
            print("this has a name clash. Try: 1-4 letters of first and 1-4 letters of last, or firstlast")
            continue
        try:
            student = canvas_df['Student'][idx]
            studentSplit = re.match("(.*), (.*)",student)
            student =f"{studentSplit.group(2)} {studentSplit.group(1)}"
            score = float(input(f"\n{student}'s Score (supports \"nan\" to reset to blank; type a letter to go back)\n"))
        except:
            continue
        prevScore = canvas_df[grade_name][idx]
        prevIdx = idx
        canvas_df.loc[idx,grade_name] = score
        #print(canvas_df)
        print(f"Updated {student} to score {score}")
        if score>points*1.1:
            print("WARNING: grade better than 110%")
    except:
        print("name not found")
        continue


canvas_df.to_csv(grade_name+"final.csv", na_rep='',index=False)
