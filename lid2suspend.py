#!/usr/bin/python

import dbus, gobject, sys
from dbus.mainloop.glib import DBusGMainLoop

pow_prop_iface = None
pow_iface = None

def handle_lidclose(*args):
    closed = pow_prop_iface.Get('',
                                'LidIsClosed')
    if closed:
        print "lid is closed, suspending"
        pow_iface.Suspend()
    else:
        print "lid is open"

def main():
    global pow_prop_iface, pow_iface

    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    power_proxy = bus.get_object('org.freedesktop.UPower',
                                '/org/freedesktop/UPower')

    pow_prop_iface = dbus.Interface(power_proxy, 'org.freedesktop.DBus.Properties')
    pow_iface = dbus.Interface(power_proxy, 'org.freedesktop.UPower')

    print "Registering a signal receiver for upower events..."

    bus.add_signal_receiver(handle_lidclose,
                            dbus_interface="org.freedesktop.UPower",
                            signal_name="Changed")


    loop = gobject.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
