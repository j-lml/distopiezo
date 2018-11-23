#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

#pip install zmq
#pip install


class BaseDriver(object):

    logger=None

    _context=None
    _pub_socket=None
    _status="ON"

    PORT = "8000"
    TYPE_DRV = "GENERIC"
    MACHINE_NAME = "M1"
    APP_NAME = "GENERIC_DRV"
    HEADER = ""
    HEARTBEAT=3


    def __init__(self):
        self.HEADER= self.TYPE_DRV + ";" + self.MACHINE_NAME + ";" + self.APP_NAME
        pass

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------
    @property
    def status(self):
        return self._status;

    @status.setter
    def status(self, estado):
        if estado not in ["ON", "OFF", "ERR"]:
            self.logger.debug("estado ["+ estado +"] - no valido")
            return

        if (estado != self.status):
            self._status=estado
            self.send_sts()


    #--------------------------------------
    #   METODOS INIT
    #--------------------------------------
    def logger_init(self):
        #logger
        path = self.APP_NAME.lower() + ".log"

        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s", "%Y%m%d %H%M%S")
        self.logger = logging.getLogger(self.APP_NAME)
        self.logger.setLevel(logging.DEBUG)

        #to console
        consoleHandler=logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)

        #to file
        timehandler = TimedRotatingFileHandler(path,
                                           when="d",
                                           interval=1,
                                           backupCount=5)
        timehandler.setFormatter(logFormatter)
        self.logger.addHandler(timehandler)

        #init
        self.logger.debug( "logger_init()" )
        self.logger.info("machine name: " + self.MACHINE_NAME )
        self.logger.info("app name: " + self.APP_NAME )
        self.logger.info("driver: " + self.TYPE_DRV )
        self.logger.info("log file: " + path )


    def zmq_init(self):
        self.logger.debug( "zmq_init()" )
        self.logger.info( "zmq: " + zmq.pyzmq_version() )

    #    if len(sys.argv) > 1:
    #        PORT =  sys.argv[1]
    #        int(PORT)

        self._context = zmq.Context()
        self._pub_socket = self._context.socket(zmq.PUB)
        self._pub_socket.bind("tcp://*:%s" % self.PORT)

        self.logger.info( "bind: " + self.PORT )


    def send_msg(self,topic,message_data):
        self._pub_socket.send("%s %s" % (topic, message_data))
        self.logger.info("" + "["+ topic +"]," + message_data )

    #--------------------------------------
    #   COMANDOS
    #--------------------------------------
    def send_hello(self):
        # hi;type;machine_name;app_name;status;val1;val2;val3
        cad="HI"  + ";" + self.HEADER + ";"
        self.send_msg( "HI" , cad)

    def help(self):
        self.logger.debug("help()")
        print("drv - v0.1")
        print("help:    muestra ayuda")
        print("run:     ejecuta programa principal")

    def run(self):
        logger.debug("run()")
        while True:
            topic = random.randrange(9999,10005)
            messagedata = random.randrange(1,215) - 80
            print "%d %d" % (topic, messagedata)
            #socket.send("%d %d" % (topic, messagedata))
            self._pub_socket.send("%d %d" % (topic, messagedata))
            time.sleep(1)

    def run(self,mode):
        #modo   run:        consigue ejecutar la funcion de siguiete param
        #ej:    run:help
        #ej:    run:random,3
        self.logger.debug("run(mode)")
        count=0
        while True:
            count=count+1
            if ( count % self.HEARTBEAT == 0):
                items=mode.split(',')
                func=None
                print items
                if (len(items)==1):
                    func = getattr(self, items[0] )
                    func()
                if (len(items)==2):
                    func = getattr(self, items[0] )
                    func(items[1])

                #    self.error("run(mode) - no existe modo: " + mode)

            time.sleep(1)


    #--------------------------------------
    #   METODOS PUBLICOS
    #--------------------------------------
    def init(self):
        #LOGGING
        self.logger_init()
        #ZMQ
        self.zmq_init()
        #envia saludo para inicializar msg. se necesita pq se pierde el primero!
        self.send_hello()



    def exec_commands(self):
        self.logger.debug("exec_commands()")
        params=sys.argv
        if len(params)<=1:
            self.help()
            exit(0)


        func,param="",""
        items=None
        try:
            #ejecuta la funcion correspondiente
            #   a) si no tiene parametros: ej app run => run()
            #   b) si tiene un param: ej app test:connection => test("connection")
            items=params[1].split(':')
            print(items)
            if (len(items)==1):
                #self.globals()[items[0]]()
                func = getattr(self, items[0] )
                func()
            if (len(items)==2):
                #self.globals()[items[0]](items[1])
                func = getattr(self, items[0] )
                func(items[1])
        except Exception as e:
            print getattr(e, 'message', repr(e))
            self.help()
            exit(0)



if __name__ == "__main__":
    drv=BaseDriver()

    drv.init()
    drv.help()
