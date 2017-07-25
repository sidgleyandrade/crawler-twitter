import tweepy
import logging
import time

from crawler.src.CRUD import CRUD
from crawler.src.db.DBConnection import DBConnection


class TwitterApiScrap:
    """ Define the initial parameters and create the stream object 
    for fetching and storing the tweets.
    """
    def __init__(self, path_home, conn_sec, schema, table, consumer_key,
                 consumer_secret, access_token, access_token_secret,
                 geo=None, search_word=None):
        self.geo = geo
        self.path_home = path_home
        self.conn_sec = conn_sec
        self.conn_schema = schema
        self.conn_table = table
        self.search_word = search_word
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.running = False

        # Create database connection to store the tweets
        self.CRUD = CRUD(self.path_home, self.conn_sec)

        # Create database table if it does not exist
        self.create_table()

        # Create the Twitter Stream object if running variable is False
        while True:
            if not self.running:
                self.init()

    def create_table(self):
        """ Create the tweets's database table from the template
        (file template-table.sql).
        """
        try:
            conn = DBConnection(self.path_home, self.conn_sec).connect_database()

            try:
                template = open(self.path_home + '/template-table.sql', 'r').read() % \
                           (str(self.conn_schema), str(self.conn_table),
                            str(self.conn_table), str(self.conn_schema),
                            str(self.conn_table), str(self.conn_schema),
                            str(self.conn_table), str(self.conn_table),
                            str(self.conn_schema), str(self.conn_table))
                cur = conn.cursor()
                cur.execute(template)
                conn.commit()
            except Exception as e:
                raise e
            finally:
                conn.close()

        except Exception as e:
            logging.error(e)
            pass

    def init(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        try:
            my_stream_listener = MyStreamListener
            my_stream = tweepy.Stream(auth=auth,
                                      listener=my_stream_listener(
                                          crud=self.CRUD,
                                          conn_sec=self.conn_sec,
                                          conn_schema=self.conn_schema,
                                          conn_table=self.conn_table))

            # Choose the kind of stream - either bounding box or word track.
            if self.search_word:
                my_stream.filter(track=[self.search_word], async=True)
            else:
                my_stream.filter(locations=self.geo, async=True)

            # Check if the connection stream is active and
            # break if it is not. init() function will restart
            # the connection stream.
            self.running = my_stream.running
            while True:
                if not my_stream.running:
                    self.running = False
                    time.sleep(60)  # Check each 60 sec.
                    break
        except Exception as e:
            logging.error(e)
            pass


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, crud, conn_sec, conn_schema, conn_table):
        self.crud = crud
        self.conn_sec = conn_sec
        self.conn_schema = conn_schema
        self.conn_table = conn_table
        super(MyStreamListener, self).__init__()

    def on_data(self, raw_data):
        # print(self.conn_sec, raw_data)
        self.crud.save(raw_data, self.conn_schema + '.' + self.conn_table)

    def on_exception(self, exception):
        logging.error(exception)
        pass

    def on_connect(self):
        logging.info('Connection ' + self.conn_sec + ' established!!')
        pass

    def on_disconnect(self, notice):
        logging.info('Connection ' + self.conn_sec + ' lost!! : ', notice)
        pass

    def on_error(self, status):
        logging.error(status)
        pass
