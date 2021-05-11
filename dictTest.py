from PyDictionary import PyDictionary

dictionary = PyDictionary()
mobileNetOptions = []

file1 = open('mobileNetObjects.txt', 'r')
count = 0
while True:
    line = file1.readline().replace("\n", "")
    if not line:
        break
    mobileNetOptions.append(line.split("  ")[1].split(", "))


availabilityStatus = False
returnObject = ""
objectAvailability = ""
yesNo = False
wantedObject = "ball"


for i in range(len(mobileNetOptions)):
    for j in range(len(mobileNetOptions[i])):
        if mobileNetOptions[i][j].lower() == wantedObject.lower():

            availabilityStatus = True
            yesNo = False
            if len(mobileNetOptions[i]) == 1:
                returnObject = mobileNetOptions[i][0]
                break
            else:

                for k in range(len(mobileNetOptions[i])):
                    print(mobileNetOptions[i][k])
                    if k == len(mobileNetOptions[i]) - 1:
                        returnObject += mobileNetOptions[i][k]
                    else:
                        returnObject += mobileNetOptions[i][k] + ", "
print(availabilityStatus)
if availabilityStatus == False:
    syns = dictionary.synonym(wantedObject)
    print(syns)
    for x in range(len(syns)):
        for i in range(len(mobileNetOptions)):
            for j in range(len(mobileNetOptions[i])):
                if mobileNetOptions[i][j].lower() == syns[x].lower():
                    print("yes")
                    yesNo = True
                    availabilityStatus = True
                    if len(mobileNetOptions[i]) == 1:
                        returnObject = mobileNetOptions[i][0]
                        break
                        #print(returnObject, availabilityStatus, yesNo)
                    else:
                        for k in range(len(mobileNetOptions[i])):
                            print(mobileNetOptions[i][k])
                            if k == len(mobileNetOptions[i]) - 1:
                                returnObject += mobileNetOptions[i][k]
                            else:
                                returnObject += mobileNetOptions[i][k] + ", "
                    print(returnObject, availabilityStatus, yesNo)

print(returnObject,availabilityStatus,yesNo)