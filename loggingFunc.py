import logging

logging.basicConfig(format='%(asctime)s : %(message)s',  datefmt='%d/%m/%Y %H:%M:%S', filename='debug.log', encoding='utf-8', level=logging.INFO)

def error(code, text, func, file):
    logging.error(f'Request error {code} : {text} in {func}, {file}')

def info(text):
    logging.info(text)