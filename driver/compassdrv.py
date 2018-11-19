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

    #logger
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)
  
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
    logger.info("log file: " + path )
    
    return logger
 

def zmq_init():
    global PORT
    logger.info( "zmq: " + zmq.pyzmq_version() )
    
    if len(sys.argv) > 1:
        PORT =  sys.argv[1]
        int(PORT)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % PORT)
    
    logger.info( "bind: " + PORT )    
    return socket



if __name__ == "__main__":
    #LOGGING
    log_file = APP_NAME.lower() + ".log"
    logger=logger_init(log_file)
    
    logger.info("app name: " + APP_NAME )
    
    #ZMQ
    socket=zmq_init()
    
    #MAIN
    while True:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        print "%d %d" % (topic, messagedata)
        socket.send("%d %d" % (topic, messagedata))
        time.sleep(1)
    
    
    
    