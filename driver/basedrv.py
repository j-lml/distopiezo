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
#pip install numpy
#pip install numpy-stl
#eliminar pip unistall stl si error)

class BaseDriver(object):

    logger=None

    _context=None
    _pub_socket=None
    _sub_socket=None
    _status="ON"

    PORT = "8000"
    TYPE_DRV = "GENERIC"
    MACHINE_NAME = "M1"
    APP_NAME = "GENERIC_DRV"

    HEARTBEAT=3


    def __init__(self):
        pass

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------
    @property
    def header(self):
        return self.TYPE_DRV + ";" + self.MACHINE_NAME + ";" + self.APP_NAME

    @property
    def name(self):
        return self.APP_NAME;

    @name.setter
    def name(self, nombre):
        self.APP_NAME=nombre        

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
    #   METODOS PROTECTED (usados de forma interna ppalmente)
    #--------------------------------------
    def set_random_name(self):
        self.APP_NAME='DISTO'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def send_msg(self,topic,message_data):
        #ref: http://zguide.zeromq.org/php:chapter2#Pub-Sub-Message-Envelopes
        #topic y msg en mismo nivel:
        #self._pub_socket.send("%s %s" % (topic, message_data))
        #para separar topic de msg:
        self._pub_socket.send_multipart([topic, message_data])
        self.logger.info("" + "["+ topic +"]," + message_data )

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

    def zmq_pub_port(self):
        return self.PORT
    def zmq_sub_port(self):
        return str( int(self.PORT) + 1000 )
    def zmq_init(self):
        self.logger.debug( "zmq_init()" )
        self.logger.info( "zmq: " + zmq.pyzmq_version() )


        #contexto
        self._context = zmq.Context()
        #pub socket
        self._pub_socket = self._context.socket(zmq.PUB)
        self._pub_socket.bind("tcp://*:%s" % self.zmq_pub_port() )
        #sub socket
        self._sub_socket = self._context.socket(zmq.SUB)
        self._sub_socket.connect("tcp://localhost:%s" % self.zmq_sub_port())

        #subscribir a tema
        filter = "COMMAND"
        # Python 2 - ascii bytes to unicode str
        if isinstance(filter, bytes):
            filter = filter.decode('ascii')
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, filter)


        self.logger.info( "pub  bind: " + self.zmq_pub_port() )
        self.logger.info( "sub bind: " + self.zmq_sub_port() )


    #--------------------------------------
    #   COMANDOS
    #--------------------------------------
    def send_hello(self):
        # hi;type;machine_name;app_name;status;val1;val2;val3
        cad="HI"  + ";" + self.header + ";"
        self.send_msg( "HI" , cad)

    def help(self):
        self.logger.debug("help()")
        print("basedrv - v0.1")
        print("help:    muestra ayuda")
        print("run:comando  ejecuta de forma repetida programa principal. ej: app.py run:send_hello")

    def run(self):
        logger.debug("run()")
        while True:
            topic = random.randrange(9999,10005)
            messagedata = random.randrange(1,215) - 80
            self.logger.info( "%d %d" % (topic, messagedata) )
            #socket.send("%d %d" % (topic, messagedata))
            self._pub_socket.send("%d %d" % (topic, messagedata))
            time.sleep(1)

    def run(self,mode):
        #modo   run:        consigue ejecutar la funcion de siguiete param
        #ej:    run:help
        #ej:    run:random,3
        self.logger.debug("run(mode)"+mode)
        count=0
        while True:
            count=count+1
            if ( count % self.HEARTBEAT == 0):
                items=mode.split(',')
                func=None
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
        self.logger.debug("basedrv::exec_commands()")
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
            if (len(items)==1):
                #self.globals()[items[0]]()
                func = getattr(self, items[0] )
                func()
            if (len(items)==2):
                #self.globals()[items[0]](items[1])
                func = getattr(self, items[0] )
                func(items[1])
        except Exception as e:
            self.logger.error("basedrv::exec_comands() - error al ejecutar funcion." + repr(items))
            print getattr(e, 'message', repr(e))
            self.help()
            exit(0)



if __name__ == "__main__":
    drv=BaseDriver()

    drv.init()
    drv.help()
