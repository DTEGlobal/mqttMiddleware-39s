__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      Cesar
#
# Created:     02/12/2014
# Copyright:   (c) Petrolog 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import threading
import mqttPetrolog
import apiClient
import logging

logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
                    filename='/home/ec2-user/logs/mqtt.log',
                    level=logging.INFO)

mqttPetrologDaemon = threading.Thread(target=mqttPetrolog.mqttPetrologDaemon)
mqttPetrologDaemon.daemon = True
mqttPetrologDaemon.start()

apiClientDaemon = threading.Thread(target=apiClient.apiClientDaemon)
apiClientDaemon.daemon = True
apiClientDaemon.start()

while True:
    a = 0  # Do nothing
