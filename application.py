from datetime import datetime
import time
import base64
import os
import sys
import requests
import json
from PyDictionary import PyDictionary
import os
from logger import log
from flask import Flask, request, render_template

dictionary = PyDictionary()

log = log()
application = Flask(__name__)
log.startup()

from yolov5.detect import objectDetect
from voiceDetection.voice_detect import voiceDetect

# from chatbot.chatbot_class import chatBot
# from objectDetection.read_video import videoDetect

# Create Instance of Critical objecs
voice = voiceDetect()
# url = 'http://0.0.0.0:5001/chatbot'
url = 'http://ec2-3-139-160-148.us-east-2.compute.amazonaws.com:5000/chatbot'

mobileNetOptions = []
askOptions = []


@application.route('/')
def hello_world():
    log.endpointReached('hello_world', request.remote_addr)
    return "<h1>hello world iseek.</h1>"


@application.route('/time')
def send_time():
    log.endpointReached('time', request.remote_addr)
    print('hello world')
    return {'time': time.time()}


@application.route('/text', methods=['POST', 'GET'])
def recieveText():
    log.endpointReached('text', request.remote_addr)
    image = objectDetect()
    if request.method == 'POST':
        print("hello world")
        data = request.json

        pic_as_base64 = data['pictureString']
        with open("textToDetect.jpg", 'wb') as fh:
            fh.write(base64.b64decode(pic_as_base64))

        imagePath = "./textToDetect.jpg"
        text = image.readText(imagePath)

        os.remove("./textToDetect.jpg")

        log.success()
        return {
            "imageText": text,
        }
    else:
        log.fail(sys.exc_info()[0])
        return "failed check system log"


@application.route('/image', methods=['POST', 'GET'])
def receivePic():
    try:
        log.endpointReached('image', request.remote_addr)
        image = objectDetect()
        print('endpoint reached')
        if request.method == 'POST':
            print("hello world")
            data = request.json
            pic_as_base64 = data['pictureString']

            with open("imageToDetect.jpg", 'wb') as fh:
                fh.write(base64.b64decode(pic_as_base64))

            imagePath = "./imageToDetect.jpg"
            objectList = image.detect(source=imagePath)

            with open('result.jpg', 'rb') as image_file:
                imageDetected = base64.b64encode(image_file.read()).decode('utf-8')

            objects = ""
            for i in range(len(objectList)):
                objects += str(objectList[i])

            os.remove("./imageToDetect.jpg")
            os.remove("./result.jpg")
            log.success()
            return {
                "pictureResponse": imageDetected,
                "objects": objectList
            }
        if request.method == 'GET':
            return "<h1>Hello world iSeek</h1>"
    except Exception as e:
        log.fail(str(e))
        return "failed check system log"


@application.route('/recording', methods=['POST', 'GET'])
def receiveWav():
    log.endpointReached('recording', request.remote_addr)
    print('endpoint reached')
    if request.method == 'POST':
        #try:
        if 'file' not in request.files:
            log.write("ERROR:\nNo File Given")
            return "no file added"

        wavFile = request.files['file']

        if wavFile.filename != '':
            wavFile.save(wavFile.filename)
        else:
            return "no file name given"

        filePath = "./{}".format(wavFile.filename)

        # Android sends audio files in .m4a format
        if wavFile.filename[-4:] == ".m4a":
            voice.m4aToWav(filePath)
           #filePath = "./{}".format(wavFile.filename[:-4] + '.wav')
            filePath = os.getcwd() + "/{}".format(wavFile.filename[:-4] + '.wav')

        text = voice.wavToText(filePath)

        os.remove(filePath)

        jsonText = json.dumps(
            {'textString': text}
        )

        respond = requests.post(url, json=jsonText)

        log.success()

        return {
            "textResponse": respond.text
        }

        # except Exception as e:
        #     log.fail(str(e))
        #     return "failed check system log"

    if request.method == 'GET':
        # return "<h1>Hello world iSeek</h1>"
        return chatbot.chatbot_response('hello')


@application.route('/chatbot', methods=['POST', 'GET'])
def chatbot():
    log.endpointReached('chatbot', request.remote_addr)
    try:
        if request.method == 'POST':
            data = request.json
            message = data['textString']

            jsonText = json.dumps(
                {'textString': message}
            )

            respond = requests.post(url, json=jsonText)
            log.success()
            return {
                "textResponse": respond.text
            }

        if request.method == 'GET':
            return "<h1>Hello world iSeek</h1>"
    except Exception as e:
        log.fail(str(e))
        return "failed check system log"

@application.route('/objectRequest', methods=['POST', 'GET'])
def objectRequest():
    print("endpoint reached")
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        data = request.form

        objectRequest = data['message']
        filePath = 'resources/objectRequests.txt'
        with open(filePath, 'r+') as f:
            current = f.readlines()
            for i in current:
                if objectRequest.lower() == i.lower().rstrip():
                    return "Item already requested"

            f.write("{}\n".format(objectRequest))
        return "not an error... Success"
@application.route('/voiceStreamingCheck', methods=['POST', 'GET'])
def voiceMobileNetObjectCheck():
    print("hello there")
    print(os.getcwd())
    if request.method == 'GET':
        return "<h1>Hello world iSeek</h1>"
    if request.method == 'POST':

        try:
            if 'file' not in request.files:
                log.write("ERROR:\nNo File Given")
                return "no file added"

            wavFile = request.files['file']

            if wavFile.filename != '':
                print(wavFile.filename)
                wavFile.save(wavFile.filename)
                
            else:
                return "no file name given"

            filePath = "./{}".format(wavFile.filename)

	    # Android sends audio files in .m4a format
            if wavFile.filename[-4:] == ".m4a":
            
                voice.m4aToWav(filePath)
                #voice.m4aToWav("/home/iseekadmin/tempserverforaws/sample.m4a")
                filePath = os.getcwd() + "/{}".format(wavFile.filename[:-4] + '.wav')
                #filePath = "./sample.wav"
           
            print(filePath)

            #filPath = os.getcwd() + "/sample.wav"
            #print(filePath)
            text = voice.wavToText(filePath)

            print(text)

           # os.remove(filePath)

            keywordCheck = False
            amazonNeeded = False
            keywords = ""

            for i in range(len(askOptions)):
                if text.lower().startswith(askOptions[i].lower()):
                    keywords = askOptions[i]
                    keywordCheck = True

            print(text, keywordCheck)
            print(len(text.split()))

            if len(text.split()) == 1 or keywordCheck:
                availabilityStatus = False
                returnObject = ""
                objectAvailability = ""
                yesNo = False
                if keywordCheck:
                    wantedObject = text.split(keywords + " ")[1]
                else:
                    wantedObject = text

                print(wantedObject)
                for i in range(len(mobileNetOptions)):
                    for j in range(len(mobileNetOptions[i])):
                        if mobileNetOptions[i][j].lower() == wantedObject.lower():
                            availabilityStatus = True
                            yesNo = False
                            if len(mobileNetOptions[i]) == 1:
                                returnObject = mobileNetOptions[i][0]
                                print('x')
                                print(returnObject)
                                return {
                                    "amazonNeeded": amazonNeeded,
                                    "objectAvailability": availabilityStatus,
                                    "yesNoNeeded": yesNo,
                                    "objectChoice": returnObject
                                }
                            else:

                                for k in range(len(mobileNetOptions[i])):
                                    # print(mobileNetOptions[i][k])
                                    if k == len(mobileNetOptions[i]) - 1:
                                        returnObject += mobileNetOptions[i][k]
                                    else:
                                        returnObject += mobileNetOptions[i][k] + ", "
                                print('y')
                                print(returnObject)
                                return {
                                    "amazonNeeded": amazonNeeded,
                                    "objectAvailability": availabilityStatus,
                                    "yesNoNeeded": yesNo,
                                    "objectChoice": returnObject
                                }

                if not availabilityStatus:
                    print("here")
                    syns = dictionary.synonym(wantedObject)
                    print(syns)
                    for x in range(len(syns)):
                        for i in range(len(mobileNetOptions)):
                            for j in range(len(mobileNetOptions[i])):
                                if mobileNetOptions[i][j].lower() == syns[x].lower():

                                    yesNo = True
                                    availabilityStatus = True

                                    if len(mobileNetOptions[i]) == 1:

                                        returnObject = mobileNetOptions[i][0]
                                        print('i')
                                        print(returnObject)
                                        return {
                                            "amazonNeeded": amazonNeeded,
                                            "objectAvailability": availabilityStatus,
                                            "yesNoNeeded": yesNo,
                                            "objectChoice": returnObject
                                        }

                                    else:

                                        for k in range(len(mobileNetOptions[i])):
                                            print(mobileNetOptions[i][k])
                                            if k == len(mobileNetOptions[i]) - 1:
                                                returnObject += mobileNetOptions[i][k]
                                            else:
                                                returnObject += mobileNetOptions[i][k] + ", "
                                        print(returnObject)
                                        print('j')

                                        return {
                                            "amazonNeeded": amazonNeeded,
                                            "objectAvailability": availabilityStatus,
                                            "yesNoNeeded": yesNo,
                                            "objectChoice": returnObject
                                        }
                    print('k')

                    print(returnObject)

                    return {
                        "amazonNeeded": amazonNeeded,
                        "objectAvailability": availabilityStatus,
                        "yesNoNeeded": yesNo,
                        "objectChoice": returnObject

                    }



            else:
                amazonNeeded = True
                jsonText = json.dumps(
                    {'textString': text}
                )

                respond = requests.post(url, json=jsonText)

                log.success()

                return {
                    "amazonNeeded": amazonNeeded,
                    "textResponse": respond.text
                }





        except TypeError  as e:
            print(e)
            # log.fail(str(sys.exec_info()))
            return "failed, check system log"


@application.route('/streamingCheck', methods=['POST', 'GET'])
def mobileNetObjectCheck():
    print("reached")
    if request.method == 'GET':
        "<h1>Hello world iSeek</h1>"

    else:

        availabilityStatus = False
        returnObject = ""
        objectAvailability = ""
        yesNo = False
        data = request.json
        wantedObject = data['requestedObject']

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

        if not availabilityStatus:
            print("here")
            syns = dictionary.synonym(wantedObject)

            try:
                for x in range(len(syns)):
                    for i in range(len(mobileNetOptions)):
                        for j in range(len(mobileNetOptions[i])):
                            if mobileNetOptions[i][j].lower() == syns[x].lower():
                                yesNo = True
                                availabilityStatus = True
                                if len(mobileNetOptions[i]) == 1:
                                    returnObject = mobileNetOptions[i][0]
                                    return {
                                        "objectAvailability": availabilityStatus,
                                        "yesNoNeeded": yesNo,
                                        "objectChoice": returnObject
                                    }

                                else:

                                    for k in range(len(mobileNetOptions[i])):
                                        print(mobileNetOptions[i][k])
                                        if k == len(mobileNetOptions[i]) - 1:
                                            returnObject += mobileNetOptions[i][k]
                                        else:
                                            returnObject += mobileNetOptions[i][k] + ", "

                                    return {
                                        "objectAvailability": availabilityStatus,
                                        "yesNoNeeded": yesNo,
                                        "objectChoice": returnObject
                                    }
            except TypeError:
                print("jeelloo")
                return {
                    "objectAvailability": availabilityStatus,
                    "yesNoNeeded": yesNo,
                    "objectChoice": returnObject,
                    "noSyns": True
                }

        return {
            "objectAvailability": availabilityStatus,
            "yesNoNeeded": yesNo,
            "objectChoice": returnObject
        }


"""
This will be used to gather the possible streaming objects that can be found
using mobilenet
"""
file1 = open('resources/mobileNetObjects.txt', 'r')
while True:
    line = file1.readline().replace("\n", "")
    if not line:
        break
    mobileNetOptions.append(line.split("  ")[1].split(", "))
# print(mobileNetOptions)

file2 = open('resources/possibleAsks.txt', 'r')
while True:
    line = file2.readline().replace("\n", "")
    if not line:
        break
    askOptions.append(line)

# for i in range(len(mobileNetOptions)):
#    print(mobileNetOptions[i])
#    for j in range(len(mobileNetOptions[i])):
#        print(mobileNetOptions[i][j])
if __name__ == "__main__":
    application.run(host='0.0.0.0') # ,threaded=True)
