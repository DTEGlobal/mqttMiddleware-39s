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
# import mqttPetrolog
# import apiClient
import logging
import logging.handlers
import omnimeter_39s

logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
                    filename='/home/ec2-user/logs/mqtt.log',
                    level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# add handler to the logger
handler = logging.handlers.SysLogHandler('/dev/log')

# add syslog format to the handler
formatter = logging.Formatter('%(name)s: %(message)s')
handler.formatter = formatter

logger.addHandler(handler)

# mqttPetrologDaemon = threading.Thread(target=mqttPetrolog.mqttPetrologDaemon)
# mqttPetrologDaemon.daemon = True
# mqttPetrologDaemon.start()

apiClientDaemon = threading.Thread(target=omnimeter_39s.apiClientDaemon)
apiClientDaemon.daemon = True
apiClientDaemon.start()


while True:
    a = 0  # Do nothing
