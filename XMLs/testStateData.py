__author__ = 'Cesar'

import urllib2
from urllib2 import URLError
import xml.etree.ElementTree as myXML
import time

while True:
    time.sleep(2)
    UpdateStateData = myXML.parse('UpdateStateData.xml')
    req = urllib2.Request(url='http://petrolog.intelectix.com/api/state',
                          data=myXML.tostring(UpdateStateData.getroot()),
                          headers={'Content-Type':'text/xml',
                                   'Authorization':'DeviceNumber=3,ApiKey=UGV0cm9sb2dDbGllbnRl'})
    try:
        resp = urllib2.urlopen(req)
    except URLError as e:
        print('Watchdog: =(')
        print('State Data Update - Failed to open connection to server! Error = %s', e.reason)
    else:
        # Feed Watchdog Server only if request OK
        r = resp.read()
        respuesta = myXML.ElementTree(myXML.fromstring(r))
        if respuesta.getroot().getiterator()[3].text == 'true':
            print("Feeder! =)")
        else:
            print("Sucedio el error!!")
            print(r)
            break