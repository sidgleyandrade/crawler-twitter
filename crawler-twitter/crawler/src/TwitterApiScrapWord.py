import tweepy

from crawler.src.CRUD import CRUD


class TwitterApiScrapWord():
    consumer_key = 'jProkL6CvWN9KDDeHDwvgmxR3'
    consumer_secret = '2LphoxXamFhXJpvP1GVC5NDrGDQ8ZvzYyzGGn9zZ5OajDbuxJF'

    access_token = "1240286418-q1EOqEInPfAPXQvBnstfvnMFalgNOQnb7OnWNQP"
    access_token_secret = "OHIqrOjP8XnVhXW2WwYX5SBU2d2curojjRpmCH9EEDSQ3"
    auth = ''

    def __init__(self, database,path_home, geo = None, searchword = None ):
        self.geo = geo
        self.path_home = path_home
        self.database = database
        self.searchword = searchword
        self.CRUD = CRUD(self.path_home)
        self.init()


    def init(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(self.auth)

        myStreamListener = MyStreamListener
        myStream = tweepy.Stream(auth=self.auth, listener=myStreamListener(crud=self.CRUD, database=self.database))
        if self.searchword:
            myStream.filter(track=[self.searchword], async=True)
        else:
            myStream.filter(locations=self.geo, async=True)


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, crud, database):
        self.crud = crud
        self.database = database
        #super().__init__()
        super(MyStreamListener, self).__init__()


    def on_data(self, raw_data):
        self.crud.save(raw_data, self.database)
