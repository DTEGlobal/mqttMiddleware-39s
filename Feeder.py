__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        Feeder
# Purpose:     This process needs to be included on the thread to be watched.
#              Connects to a Watchdog Server and sends updates based on a random
#              UUID generated at the start of the thread to be watched.
#
#
# Author:      Cesar, Jorge
#
# Created:     10/23/2013
# Copyright:   (c) Cesar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from socket import *
import time
import logging

def feeder(id, diagMsg):
    currentTime = str(time.time())

# 1. Send Keep Alive to Watchdog Server
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(.5)
    try:
        s.connect(('localhost', 8080))
        toSend = id+","+currentTime
        s.send(toSend.encode())
        s.close()
        logging.debug("Feeder - Keep Alive Message = %s", toSend)
    except error:
        logging.error("Feeder - No Watchdog Server available")

# 2. Send Diagnostic Message to Diagnostic Server (192.168.1.248)
    time.sleep(1)
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(.5)
    try:
        s.connect(('192.168.1.248', 8081))
        toSend = id+","+currentTime+","+diagMsg+"\n"
        s.send(toSend.encode())
        s.close()
        logging.debug("Feeder - Diagnostic Message = %s", toSend)
    except error:
        logging.debug("Feeder - No Diagnostic Server available")
