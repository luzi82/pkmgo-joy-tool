'''
Created on Jul 23, 2016

@author: luzi82
'''

import sys
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from luzi82.pkmgo import common as vcommon

def create_sender(dbus_interface_name, object_path):
    class Sender(dbus.service.Object):
        def __init__(self):
            dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)
        @dbus.service.signal(dbus_interface=dbus_interface_name,signature='s')
        def message(self, message):
#             vcommon.perr('JGHDDWRV '+str(len(message)))
            pass
     
    return Sender()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        vcommon.perr ('{0} dbus_interface_name object_path'.format(sys.argv[0]))
        exit()
        
    arg_dbus_interface_name = sys.argv[1]
    arg_object_path = sys.argv[2]

    DBusGMainLoop(set_as_default=True)
      
    sender = create_sender(arg_dbus_interface_name,arg_object_path)
     
    for line in sys.stdin:
        if line == None:
            break
        l = line.rstrip('\n')
        sender.message(l)
        vcommon.pout(l)
