import logging

logging.basicConfig(format='%(asctime)s : %(message)s',  datefmt='%d/%m/%Y %H:%M:%S', filename='debug.log', encoding='utf-8', level=logging.INFO)

def loggingError(res, funcName):
    message, code = res.json()["status"].values()
    logging.error(f'Request error {code} : {message} in {funcName}')

def loggingInfo(text):
    logging.info(text)