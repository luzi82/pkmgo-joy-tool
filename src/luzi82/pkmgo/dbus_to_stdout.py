'''
Created on Jul 23, 2016

@author: luzi82
'''

import sys
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi.repository.GLib
from luzi82.pkmgo import common as vcommon

def signal_handler(message):
    try:
        vcommon.pout(message)
    except:
        loop.quit()

loop = None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        vcommon.perr ('{0} dbus_interface_name'.format(sys.argv[0]))
        exit()

    arg_dbus_interface_name = sys.argv[1]

    DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    bus.add_signal_receiver(signal_handler,dbus_interface=arg_dbus_interface_name)

    loop = gi.repository.GLib.MainLoop()
    loop.run()
