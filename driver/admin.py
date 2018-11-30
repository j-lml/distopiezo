#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging
import string

from logging.handlers import TimedRotatingFileHandler

from basedrv import *


class AdminDisto(BaseDriver):

    def __init__(self):
        self.PORT = "8007"
        self.TYPE_DRV = "ADMIN"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "A1"
        BaseDriver.__init__(self)

    def init(self):
        BaseDriver.init(self)

        self._pub_socket.connect("tcp://127.0.0.1:%s" % 9005 ) #para enviar ordenes a simul

        #subscribir a tema
        self._sub_socket.connect("tcp://localhost:%s" % 8001)   #compass
        self._sub_socket.connect("tcp://localhost:%s" % 8002)   #accel
        self._sub_socket.connect("tcp://localhost:%s" % 8003)   #disto
        self._sub_socket.connect("tcp://localhost:%s" % 8005)   #simul
        filter = "STS"
        if isinstance(filter, bytes):
            filter = filter.decode('ascii')
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, filter)

        filter = "COMMAND"
        if isinstance(filter, bytes):
            filter = filter.decode('ascii')
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, filter)

    #--------------------------------------
    #   COMANDOS PUB
    #--------------------------------------
    def help(self):
        BaseDriver.help(self)

    def recfile(self):

        cmd=None
        wait = True
        while wait == True:
            #solicita que comienze la transmision
            self.send_command("SENDFILE","")

            #lee datos
            topic,cmd,msg=self.read_sck_command()
            if cmd == "TRANSMISSION_STARTED":
                wait = False
            time.sleep(1)


        run = True
        while run==True:
            try:
                topic,cmd,msg=self.read_sck_command_sync()
                cmd=msg.split(';')[0]
                if cmd == "TRANSMISSION_STARTED":
                    self.logger.debug("comando rcv: " + msg)
                if cmd == "TRANSMISSION_ENDED":
                    self.logger.debug("comando rcv: " + msg)
                    self.logger.debug("" + msg)
                    run=False
                if cmd == "PCART":
                    self.logger.debug("" + msg)

            except zmq.Again as e:
                pass



if __name__ == "__main__":
    drv=AdminDisto()
    drv.init()

    #MAIN
    drv.exec_cmd_command()
