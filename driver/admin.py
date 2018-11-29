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

        self._pub_socket.bind("tcp://127.0.0.1:%s" % 9005 ) #para enviar ordenes a simul

        #subscribir a tema
        self._sub_socket.connect("tcp://localhost:%s" % 8001)   #compass
        self._sub_socket.connect("tcp://localhost:%s" % 8002)   #accel
        self._sub_socket.connect("tcp://localhost:%s" % 8003)   #disto
        self._sub_socket.connect("tcp://localhost:%s" % 8005)   #simul
        filter = "STS"
        if isinstance(filter, bytes):
            filter = filter.decode('ascii')
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, filter)

    #--------------------------------------
    #   COMANDOS PUB
    #--------------------------------------
    def help(self):
        BaseDriver.help(self)

    def recfile(self):
        #solicita que comienze la transmision
        self.send_msg("COMMAND","SENDFILE")

        run = True
        while run==True:
            try:
                #msg = self._sub_socket.recv_string()
                topic = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
                msg = self._sub_socket.recv_string(flags=zmq.NOBLOCK)

                cmd=msg.split(';')[0]
                if cmd == "START_TRANSMISSION":
                    self.logger.debug("comando rcv: " + msg)
                if cmd == "END_TRANSMISSION":
                    self.logger.debug("comando rcv: " + msg)
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
