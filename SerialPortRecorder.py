## File created by Unnikrishnan
## Created on 2022-09-23
## Created at :
##    Kappa Lab 
##    Department of Mechanical and Aerospace Engineering 
##    Indian Institute of Technology Hyderabad

import time
import serial
from datetime import datetime
import csv
# from decimal import Decimal

recordingStatus = False
serialPort = serial.Serial(port="COM6", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
now = datetime.now()
nowDateTimeString = now.strftime("%Y-%m-%d_%H-%M-%S")
serialPort.flushInput()
serialPort.flushOutput()



def FormatSerialData(valueString):
    valueString = valueString.replace('\r', '')
    valueString = valueString.replace('\n', '')
    valueString = valueString.replace('g', '')
    valueString = valueString.replace(' ', '')
    # valueString.replace('-', '')
    return valueString


csvFilename = "17Hz-outlet-PressureHoneyWell-" + "Recording-" + nowDateTimeString + ".csv"
fields = ['Recording Set Number', 'Values']
rows = []
input("Press Enter to start recording...")

print("Press Ctrl + C to stop recording...")
print("---- Starting Recording ----")

i = 0
while i < 1:
    count = 0
    newRow = []
    # newRow.append('Recording ' + str(len(rows)))
    serialPort.flushInput()
    serialPort.flushOutput()

    try:
        while True:
            recordingStatus = True
            value = []
            serialString = serialPort.readline()
            # try:
            t = datetime.now().strftime('%M:%S.%f').split(':')
            seconds = float(t[0])*60 + float(t[1])
            
            dataRead = FormatSerialData(serialString.decode('Ascii'))
            try:
                dataRead = float(dataRead)
                value.append(seconds)
                value.append(dataRead)
            except ValueError:
                continue
            
            # except:
            # t = datetime.now().strftime('%M:%S.%f').split(':')
            # seconds = float(t[0])*60 + float(t[1])
            # value.append(seconds)
            # value.append(0.00)
            # continue
            newRow.append(value)
            # time.sleep(0.001)
            count += 1
            # if count > 11001:
            if count > 2000:
                break
            print(str(count) +' -> ' + str(dataRead)+ ' ,')
            # print(str(count) +' -> ' + str(dataRead)+ ' ,', end=" ")
    except KeyboardInterrupt:
        pass
    rows.append(newRow)
    i += 1

for row in rows[0]:
    z = row[0] - rows[0][0][0]
    row.append(z)

print("---- Writing CSV file ----")
# writing to csv file
with open(csvFilename, 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    # csvwriter.writerow(fields)

    # writing the data rows
    for row in rows:

        csvwriter.writerows(row)
message = "file " + csvFilename + " generated"
print("------- " + message + " -------")

sum = 0
count = 0
for item in rows[0]:
    try:
        v = float(item[1])
        sum = sum + v
    except:
        continue
    count += 1
print("---- Computing average----")

avg = sum/count
print('Average: ', avg)

with open(csvFilename, 'a') as f:
    f.write(',avg = ,')
    f.write(str(avg))





