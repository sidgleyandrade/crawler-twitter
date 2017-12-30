import configparser
import os
import sys
import logging
import multiprocessing
from itertools import repeat

from crawler.src.TwitterApiScrap import TwitterApiScrap


def warp(args):
    TwitterApiScrap(*args)

def main():
    # Get the parameters from setup.cfg.
    path_home = os.path.dirname(os.path.realpath(__file__)) + '/crawler'
    cfg = configparser.ConfigParser()
    cfg.read(path_home + '/setup.cfg')

    # Create error log file.
    logging.basicConfig(filename=sys.argv[0].split(".")[0] + '.log',
                        format='%(asctime)s\t%(name)s\t[%(process)d]\t'
                               '%(processName)s\t%(threadName)s\t'
                               '%(module)s\t%(funcName)s\t%(lineno)d\t'
                               '%(levelname)s:%(message)s',
                        level=logging.ERROR)

    # List of parameters of configuration to create the connections threads.
    consumer_key = []
    consumer_secret = []
    access_token = []
    access_token_secret = []
    bounding_box = []
    conn_table = []
    conn_schema = []
    search_word = []

    try:
        for conn in cfg.sections():
            params = cfg.items(conn)
            bounding_box_format = ''

            for param in params:
                if param[0] == 'connection.consumer_key':
                    consumer_key.append(param[1])
                if param[0] == 'connection.consumer_secret':
                    consumer_secret.append(param[1])
                if param[0] == 'connection.access_token':
                    access_token.append(param[1])
                if param[0] == 'connection.access_token_secret':
                    access_token_secret.append(param[1])
                if param[0] == 'connection.bounding_box':
                    bounding_box_format = param[1].split(',')
                if param[0] == 'connection.search_word':
                    search_word.append(param[1].split(',')[0]) \
                        if param[1].split(',')[0] != '' \
                        else search_word.append(None)
                if param[0] == 'database.table':
                    conn_table.append(param[1].split(',')[0])
                if param[0] == 'database.schema':
                    conn_schema.append(param[1].split(',')[0])

            # Format bounding box.
            if len(bounding_box_format) == 4:
                for k, geo in enumerate(bounding_box_format):
                    bounding_box_format[k] = (float(geo))
            bounding_box.append(bounding_box_format)

        pool = multiprocessing.Pool(len(cfg.sections()))
        crawler_args = zip(repeat(path_home), cfg.sections(), conn_schema,
                           conn_table, consumer_key, consumer_secret,
                           access_token, access_token_secret,
                           bounding_box, search_word)
        pool.map(warp, crawler_args)

    except Exception as e:
        logging.error(e)
        exit(0)

if __name__ == '__main__':
    main()