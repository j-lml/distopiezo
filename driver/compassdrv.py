import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler


context=None
socket=None
logger=None
PORT = "8000"
APP_NAME = "COMPASS_DRV"

def logger_init(path):
    global APP_NAME

    #logger
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)

    #to console
    consoleHandler=logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    #to file
    timehandler = TimedRotatingFileHandler(path,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    timehandler.setFormatter(logFormatter)
    logger.addHandler(timehandler)

    #init
    logger.debug( "logger_init()" )
    logger.info("app name: " + APP_NAME )
    logger.info("log file: " + path )

    return logger

def zmq_init():
    global PORT
    logger.debug( "zmq_init()" )
    logger.info( "zmq: " + zmq.pyzmq_version() )

#    if len(sys.argv) > 1:
#        PORT =  sys.argv[1]
#        int(PORT)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % PORT)

    logger.info( "bind: " + PORT )
    return socket

def help():
    logger.debug("help()")
    print("drv - v0.1")
    print("help:    muestra ayuda")
    print("run:     ejecuta programa principal")
    exit(0);

def run():
    logger.debug("run()")
    while True:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        print "%d %d" % (topic, messagedata)
        socket.send("%d %d" % (topic, messagedata))
        time.sleep(1)

def parse_commands():
    logger.debug("parse_commands()")
    params=sys.argv
    print(params)
    if len(params)<=1:
        help()

    func,param="",""
    items=None
    try:
        #ejecuta la funcion correspondiente
        #   a) si no tiene parametros: ej app run => run()
        #   b) si tiene un param: ej app test:connection => test("connection")
        items=params[1].split(':')
        if (len(items)==1):
            globals()[items[0]]()
        if (len(items)==2):
            globals()[items[0]](items[1])
    except:
        help()



if __name__ == "__main__":
    #LOGGING
    log_file = APP_NAME.lower() + ".log"
    logger=logger_init(log_file)
    #ZMQ
    socket=zmq_init()

    #MAIN
    parse_commands()
