"""
Listens for activity on M/# topic and for each message spawns a thread to generate and send a 39 to
NebulaLink.
"""
__author__ = 'Cesar'


import mosquitto
import threading
import logging
import socket


def send_39(msg):
    """
    Create and send a 39 based on the message from mqtt broker.
    nebula server: nebulalisten.com:3001
    :param msg: mqtt topic: M/F/[id]/[data1, data2 ..]
    :return: N/A (thread)
    """
    telemetry_address_hex = hex(int(msg.topic.split('/')[2]))
    telemetry_address = telemetry_address_hex[2:].upper().zfill(6)
    logging.debug('_39s: send_39 telemetry_address={0}'.format(telemetry_address))
    # Fill DI with 0s not used
    data_packet = '00000000'
    # Get elements from mqtt:
    data = msg.payload.split(',')
    for element in data:
        try:
            element_hex = hex(int(element))
        except ValueError:
            logging.warning('_39s: Not able to convert Element {0} to hex'.format(element))
        # Remove '0x'
        element_string = str(element_hex)[2:]
        if len(element_string) > 4:
            # Fix length to 4 chars
            logging.warning('_39s: Element {0} longer than 4 chars, fixing!'.format(element_string))
            element_string = element_string[:4]
        element_string = element_string.rjust(4, '0')
        logging.debug('_39s: send_39 element:, hex={0}, hex string={1}'.format(element_hex, element_string))
        data_packet += element_string
    data_packet = data_packet.ljust(64, '0')
    _39 = 'GET /A/B/7F26{0}39{1} HTTP/1.1'.format(telemetry_address, data_packet)

    try:
        s = socket.socket()
        s.connect(('nebulalisten.com', 3001))
        logging.debug('_39 to send: {0}'.format(_39))
        s.send(_39)
        r = s.recv(255)
        s.close()
        logging.debug('Rx from server: {0}'.format(r))
        if r == 'Respuesta=9':
            pass
        else:
            raise
    except Exception as e:
        logging.warning('Failed to open connection to server! Error = %s', e.__str__())


# Define event callbacks
def on_connect(mosq, obj, rc):
    logging.info("Connected, rc: " + str(rc))
    # Subscribe to Command
    mqttc.subscribe('M/F/#', 0)


def on_message(mosq, obj, msg):
    logging.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    logging.info(str(msg.payload))
    t = threading.Thread(target=send_39, args=[msg])
    t.daemon = True
    t.start()


def on_publish(mosq, obj, mid):
    logging.debug("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    logging.debug(string)


def apiClientDaemon():
    mqttc.loop_forever()


# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("_39s")

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect('54.85.197.66', 1883)
