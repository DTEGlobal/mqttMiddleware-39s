from _elementtree import Element

__author__ = 'Cesar'

import xml.etree.ElementTree as myXML
import xml.etree.ElementTree as test
import xml.etree.ElementTree as test2

import urllib2

GraphData = myXML.parse('GraphData.xml')
points = GraphData.getroot().find("Points")

for child in points:
    point = child
    points.remove(child)

dyna = [(1424, 1777), (1313, 1779), (1265, 1777), (1277, 1764), (1230, 1749), (1148, 1706), (1108, 1679), (1132, 1650), (1169, 1597), (1216, 1529), (1289, 1463), (1386, 1391), (1397, 1351), (1410, 1325), (1472, 1325), (1446, 1338), (1495, 1366), (1530, 1391), (1578, 1435), (1637, 1461), (1674, 1530), (1638, 1585), (1578, 1611), (1494, 1678), (1422, 1719), (1374, 1750), (1339, 1778), (1375, 1777), (1414, 1791)]

if dyna != '':
    #dyna = ''

    for p in dyna:
        points.append(
            test.fromstring(
                '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays">'
                + str(p[0])+','+str(p[1])+'</string>'))

    #a = GraphData.getroot().find('Points')
    try:
        print GraphData.getroot().find('Points')[0].text
    except IndexError as e:
        print "vacio"


# ----------- Commands -------------
#req = urllib2.Request(url='http://petrologtest.intelectix.com/api/command',
#                              headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
#resp = urllib2.urlopen(req)
#s = resp.read()
#respuesta = test2.ElementTree(test2.fromstring(s))
#
#command = respuesta.iter(tag='Command').next()
#print command.text
#
#commandId = respuesta.iter(tag='ConsoleCommandId').next()
#print commandId.text
#
#root = respuesta.getroot()
#ns = root[0]
#print 'vacio!!!! --> '+str(ns)
#
#namespaces = {'ns':'http://schemas.datacontract.org/2004/07/Ifx.Api.Model'}
#
#r = root.find('ns:Response', namespaces=namespaces)
##print 'r.attrib = '+str(r.attrib)
#
##print test2.tostring(root)
#print root[2].tag
#print r.find('Command').text