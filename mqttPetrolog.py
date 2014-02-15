__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        mqttPetrolog
# Purpose:
#
# Author:      Cesar
#
# Created:     02/14/2014
# Copyright:   (c) Cesar 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import uuid
import time
import Feeder

import logging
import mosquitto
import xml.etree.ElementTree as myXML
import xml.etree.ElementTree as point
import threading

def createStateDataXML(msg):
    UpdateStateData = myXML.parse('XMLs/UpdateStateData.xml')
    S = msg.payload.split(',')
    root = UpdateStateData.getroot()
    del S[-1]
    try:
        i = 0
        for value in S:
            root[i].text = value
            i += 1
    except IndexError:
        logging.error('Rx message error')

    else:
        ID = msg.topic.split('/')
        mqttc.publish("XML/{0}/{1}".format(ID[1], ID[2]), myXML.tostring(root))


def createGraphDataXML(msg):
    GraphData = myXML.parse('XMLs/GraphData.xml')
    points = GraphData.getroot().find("Points")
    D = msg.payload.split(',')
    del D[-1]
    dyna = [(0, 0)]
    dyna.pop(0)
    j = 0
    try:
        for value in D:
            if j >= len(D):
                break
            pair = (D[j], D[j+1])
            dyna.append(pair)
            j += 2
        for p in dyna:
            points.append(
                point.fromstring(
                    '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays">' +
                    str(p[0])+','+str(p[1])+'</string>'))
    except IndexError:
        logging.error('Rx message error')
    else:
        ID = msg.topic.split('/')
        mqttc.publish("XML/{0}/{1}".format(ID[1], ID[2]), myXML.tostring(GraphData.getroot()))


#def createCommandXML(msg):




# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))


def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    msgID = msg.topic.split('/')
    if msgID[2] == 'S':
        t = threading.Thread(target=createStateDataXML, args=(msg,))
        t.daemon = True
        t.start()
    elif msgID[2] == 'D':
        t = threading.Thread(target=createGraphDataXML, args=(msg,))
        t.daemon = True
        t.start()
    # elif msgID[2] == 'PR':
    #     t = threading.Thread(target=createCommandXML, args=(msg,))
    #     t.start() TODO
    return


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    print(string)


# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("mqttPetrolog")

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect('54.84.2.71', 1883)

# Subscribe to Command
mqttc.subscribe('F/#', 0)




def mqttPetrologDaemon():

    # Continue the network loop, exit when an error occurs TODO loop_forever
    rc = 0
    while rc == 0:
        rc = mqttc.loop()
    print("rc: " + str(rc))

