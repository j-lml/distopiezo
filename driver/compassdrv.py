#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

from basedrv import *


class CompassDriver(BaseDriver):

    _angle=0;

    def __init__(self):
        self.TYPE_DRV = "COMPASS"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "COMPASS_DRV"
        BaseDriver.__init__(self)

    def get_angle(self):
        return self._angle

    def set_angle(self,angle):
        try:
            new_angle=float(angle)
        except:
            return

        new_angle = new_angle % 360
        if (new_angle != self._angle):
            self._angle=new_angle
            self.send_sts()




    def send_sts(self):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        cad="STS"  + ";" + self.HEADER + ";" + "ON" + ";" + str(self.get_angle()) + ";"
        self.send_msg( "STS" , cad)

    def compass(self):
        self.logger.debug("compass()")
        count=0
        HEARTBEAT=5
        while True:
            count=count+1
            if ( count % HEARTBEAT == 0):
                count=0
                a = random.randrange(0,36000)
                a = float(a) / float(100)
                self.set_angle(a)

            time.sleep(1)

    def help(self):
        BaseDriver.help(self)
        print("compass:     ejecuta programa principal")



if __name__ == "__main__":
    drv=CompassDriver()
    drv.init()

    #MAIN
    drv.exec_commands()
