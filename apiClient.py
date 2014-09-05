__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        apiClient
# Purpose:
#
# Author:      Cesar
#
# Created:     02/14/2014
# Copyright:   (c) Cesar 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import mosquitto
import threading
import logging
import urllib2
from urllib2 import URLError


def httpPOST(msg):
    telemetryAddress = msg.topic.split('/')
    if telemetryAddress[2] == 'S':
        url = 'state'
    elif telemetryAddress[2] == 'D':
        url = 'graph'

    req = urllib2.Request(url='http://petrolog.intelectix.com/api/{0}'.format(url),
                          data=msg.payload,
                          headers={'Content-Type': 'text/xml',
                                   'Authorization': 'DeviceNumber={0},ApiKey=UGV0cm9sb2dDbGllbnRl'.format(telemetryAddress[1])})
    try:
        urllib2.urlopen(req)
    except URLError as e:
        logging.warning('Failed to open connection to server! Error = %s', e.reason)


# Define event callbacks
def on_connect(mosq, obj, rc):
    logging.info("Connected, rc: " + str(rc))
    # Subscribe to Command
    mqttc.subscribe('XML/#', 0)


def on_message(mosq, obj, msg):
    logging.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    t = threading.Thread(target=httpPOST, args=(msg,))
    t.daemon = True
    t.start()


def on_publish(mosq, obj, mid):
    logging.debug("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    logging.debug(string)


# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("apiClient")

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect('localhost', 1883)


def apiClientDaemon():
    mqttc.loop_forever()
