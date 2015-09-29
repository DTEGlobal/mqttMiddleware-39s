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
import logging
import logging.handlers
import _39s

# logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
#                     filename='/home/ec2-user/logs/mqtt.log',
#                     level=logging.INFO)
logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
                    filename='/Users/Cesar/logs/mqtt.log',
                    level=logging.DEBUG)

_39sDaemon = threading.Thread(target=_39s.apiClientDaemon)
_39sDaemon.daemon = True
_39sDaemon.start()


while True:
    a = 0  # Do nothing
