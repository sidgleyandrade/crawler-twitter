import tweepy
import logging

from crawler.src.CRUD import CRUD
from crawler.src.db.DBConnection import DBConnection

class TwitterApiScrap():

    auth = ''

    def __init__(self,path_home, conn_sec, schema, table, consumer_key, consumer_secret,
                 access_token, access_token_secret, geo=None, searchword=None):

        ''' initial parameters '''
        self.geo = geo
        self.path_home = path_home
        self.conn_sec = conn_sec
        self.conn_schema = schema
        self.conn_table = table
        self.CRUD = CRUD(self.path_home, self.conn_sec)
        self.searchword = searchword
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.create_table()
        self.init()


    ''' if not exists, then to create table from cfg file '''
    def create_table(self):
        try:
            template = open(self.path_home + '/template-table.sql', 'r').read() % (str(self.conn_schema), str(self.conn_table), str(self.conn_table),
                                                                             str(self.conn_schema), str(self.conn_table), str(self.conn_schema),
                                                                             str(self.conn_table), str(self.conn_table), str(self.conn_schema), str(self.conn_table))

            conn = DBConnection(self.path_home, self.conn_sec).connect_database()
            cur = conn.cursor()
            cur.execute(template)
            conn.commit()
        except Exception as e:
            print e
            raise e
        finally:
            conn.close()


    ''' creating a stream '''
    def init(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(self.auth)

        try:
            myStreamListener = MyStreamListener
            myStream = tweepy.Stream(auth=self.auth, listener=myStreamListener(crud=self.CRUD, conn_sec=self.conn_sec, conn_schema=self.conn_schema, conn_table=self.conn_table))

            ''' starting a stream  '''
            if self.searchword:
                myStream.filter(track=[self.searchword], async=True)
            else:
                myStream.filter(locations=self.geo, async=True)

        except Exception as e:
            logging.error(e)


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, crud, conn_sec, conn_schema, conn_table):
        self.crud = crud
        self.conn_sec = conn_sec
        self.conn_schema = conn_schema
        self.conn_table = conn_table
        super(MyStreamListener, self).__init__()

    def on_data(self, raw_data):
        self.crud.save(raw_data, self.conn_schema + '.' + self.conn_table)

    def on_connect(self):
        logging.info('Connection ' + self.conn_sec + ' established!!')

    def on_disconnect(self, notice):
        logging.error('Connection ' + self.conn_sec + ' lost!! : ', notice)

    def on_error(self, status):
        logging.error(status)

