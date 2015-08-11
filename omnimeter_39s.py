"""
Listens for activity on OM/# topic and for each message spawns a thread to generate and send a 39 to
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
    :param msg: mqtt topic: OM/F/[id]/[data1, data2 ..]
    :return: N/A (thread)
    """
    telemetry_address_hex = hex(int(msg.topic.split('/')[2]))
    telemetry_address = telemetry_address_hex[2:].upper().zfill(6)
    logging.debug('omnimeter_39s: send_39 telemetry_address={0}'.format(telemetry_address))
    # Fill DI with 0s (not used in Omnimeter)
    data_packet = '00000000'
    # Get elements from mqtt:
    data = msg.payload.split(',')
    #   [0] omnimeter.total_kwh,
    #   X [1] omnimeter.t1_kwh,
    #   X [2] omnimeter.t2_kwh,
    #   X [3] omnimeter.t3_kwh,
    #   X [4] omnimeter.t4_kwh,
    #   [5]omnimeter.total_rev_kwh,
    #   X [6] omnimeter.t1_rev_kwh,
    #   X [7] omnimeter.t2_rev_kwh,
    #   X [8] omnimeter.t3_rev_kwh,
    #   X [9] omnimeter.t4_rev_kwh,
    #   [10] omnimeter.v1,
    #   [11] omnimeter.v2,
    #   [12] omnimeter.v3,
    #   [13] omnimeter.a1,
    #   [14] omnimeter.a2,
    #   [15] omnimeter.a3,
    #   X [16] omnimeter.p1,
    #   X [17] omnimeter.p2,
    #   x [18] omnimeter.p3,
    #   [19] omnimeter.p_total,
    #   [20] omnimeter.cos1,
    #   [21] omnimeter.cos2,
    #   [22] omnimeter.cos3,
    #   X [23] omnimeter.max_demand,
    #   x [24] omnimeter.date_time)
    del data[1:5]
    del data[2:6]
    del data[8:11]
    del data[-2:]
    for element in data:
        try:
            element_hex = hex(int(element))
        except ValueError:
            # for 'C000' in omnimeter.cos3
            element = element[1:]
            element_hex = hex(int(element))
        # Remove '0x'
        element_string = str(element_hex)[2:]
        if len(element_string) > 4:
            # Fix length to 4 chars
            logging.warning('omnimeter_39s: Element {0} longer than 4 chars, fixing!'.format(element_string))
            element_string = element_string[:4]
        element_string = element_string.rjust(4, '0')
        logging.debug('omnimeter_39s: send_39 element:, hex={0}, hex string={1}'.format(element_hex,
                                                                                        element_string))
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
    mqttc.subscribe('OM/F/#', 0)


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
mqttc = mosquitto.Mosquitto("Omnimeter_39s")

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect('54.85.197.66', 1883)
