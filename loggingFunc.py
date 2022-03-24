import logging

logging.basicConfig(format='%(asctime)s : %(message)s',  datefmt='%d/%m/%Y %H:%M:%S', filename='debug.log', encoding='utf-8', level=logging.INFO)

def loggingError(code, funcName, more=''):
    listCode = {
        400 : 'Bad request',
        401 : 'Unauthorized',
        403 : 'Forbidden',
        404 : 'Data not found',
        405 : 'Method not allowed',
        415 : 'Unsupported media type',
        429 : 'Rate limit exceeded',
        500 : 'Internal server error',
        502 : 'Bad gateway',
        503 : 'Service unavailable',
        504 : 'Gateway timeout',
    }
    logging.error(f'Request error {code} : {listCode[code]} in {funcName} ({more})')

def loggingInfo(text):
    logging.info(text)