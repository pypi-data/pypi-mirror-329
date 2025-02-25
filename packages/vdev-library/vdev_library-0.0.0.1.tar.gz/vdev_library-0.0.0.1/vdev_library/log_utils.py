import logging
from logging.handlers import RotatingFileHandler
import sys, os
def vdev_set_log(log_level: str, log_file_name, log_message: str, class_name: str):
    os.makedirs("logs/debug", exist_ok=True)
    os.makedirs("logs/info", exist_ok=True)
    os.makedirs("logs/warning", exist_ok=True)
    os.makedirs("logs/error", exist_ok=True)
    logging.getLogger().handlers.clear()
    
    logging.getLogger().setLevel(logging.NOTSET)

    # Add stdout handler, with level INFO
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)    
    # Add file rotating handler, with level
    log_folder = ""
    if log_level == "DEBUG":
        log_folder="debug"
    if log_level == "INFO":
        log_folder="info"
    if log_level == "WARNING":
        log_folder="warning"
    if log_level == "ERROR":
        log_folder="error"

    rotatingHandler = RotatingFileHandler(filename='logs/'+log_folder+'/'+log_file_name+'_rotating.log', maxBytes=10000000, backupCount=50)
    if log_level == "DEBUG":
        rotatingHandler.setLevel(logging.DEBUG)
    if log_level == "INFO":
        rotatingHandler.setLevel(logging.INFO)
    if log_level == "WARNING":
        rotatingHandler.setLevel(logging.WARNING)
    if log_level == "ERROR":
        rotatingHandler.setLevel(logging.ERROR)        

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    rotatingHandler.setFormatter(formatter)
    logging.getLogger().addHandler(rotatingHandler)

    #log = logging.getLogger("app." + __name__)
    log = logging.getLogger(class_name)
    
    if log_level == "DEBUG":
        log.debug(log_message)
    if log_level == "INFO":
        log.info(log_message)
    if log_level == "WARNING":
        log.warning(log_message)
    if log_level == "ERROR":
        log.error(log_message)

    return True