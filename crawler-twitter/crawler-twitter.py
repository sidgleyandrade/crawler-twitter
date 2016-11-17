__title__ = 'crawler-twitter'
__author__ = 'Sidgley Camargo de Andrade'
__license__ = 'GPLv3'

import configparser
import os
import sys
import logging

from crawler.src.TwitterApiScrap import TwitterApiScrap


''' main function '''
if __name__ == '__main__':

    path_home = os.getcwd() + '/crawler'

    cfg = configparser.ConfigParser()
    cfg.read(path_home + '/setup.cfg')

    ''' creates log file '''
    logging.basicConfig(filename=sys.argv[0].split(".")[0] + '.log',
                        format='%(asctime)s\t %(name)s\t [%(process)d] %(processName)s\t %(threadName)s\t %(module)s\t %(funcName)s\t %(lineno)d \t %(levelname)s:%(message)s',
                        level=logging.INFO)

    ''' initial variables of connections '''
    consumer_key = []
    consumer_secret = []
    access_token = []
    access_token_secret = []
    bounding_box = []
    conn_table = []
    conn_schema = []
    search_word = []

    try:
        ''' get parameters from config file '''
        for conn in cfg.sections():
            params = cfg.items(conn)
            bounding_box_format = ''

            for param in params:
                if param[0] == 'connection.consumer_key': consumer_key.append(param[1])
                if param[0] == 'connection.consumer_secret': consumer_secret.append(param[1])
                if param[0] == 'connection.access_token': access_token.append(param[1])
                if param[0] == 'connection.access_token_secret': access_token_secret.append(param[1])
                if param[0] == 'connection.bounding_box': bounding_box_format = param[1].split(',')
                if param[0] == 'connection.search_word': search_word.append(param[1].split(',')[0]) if param[1].split(',')[0] != '' else search_word.append(None)
                if param[0] == 'database.table': conn_table.append(param[1].split(',')[0])
                if param[0] == 'database.schema': conn_schema.append(param[1].split(',')[0])

            ''' format bounding box '''
            if (len(bounding_box_format)>2):
                for k, geo in enumerate(bounding_box_format):
                    bounding_box_format[k] = (float(geo))
            bounding_box.append(bounding_box_format)

        crawler = list()

        for i, conn in enumerate(cfg.sections()):
            crawler.append(TwitterApiScrap(path_home=path_home, conn_sec=conn, schema=conn_schema[i], table=conn_table[i],
                                           consumer_key=consumer_key[i], consumer_secret=consumer_secret[i], access_token=access_token[i],
                                           access_token_secret=access_token_secret[i], geo=bounding_box[i],searchword=search_word[i]))
    except Exception as e:
        logging.error(e)
        exit(0)