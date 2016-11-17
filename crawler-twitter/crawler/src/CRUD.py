import pytz
import psycopg2
import logging
from tweepy.streaming import json
from datetime import datetime
from crawler.src.models import TwitterMessage
from crawler.src.models import TwitterUser
from crawler.src.models import TwitterPlace
from crawler.src.db.DBConnection import DBConnection

class CRUD():

    def __init__(self, path_home, conn_sec):
        self.setUp(path_home, conn_sec)

    def setUp(self, path_home, conn_sec):
        try:
            self.conn = DBConnection(path_home, conn_sec).connect_database()
            self.cur = self.conn.cursor()
        except Exception as e:
            raise e

    def save(self, tweet=None, conn_table=''):

        all_data = json.loads(tweet)

        if tweet:
            tweetMessage = TwitterMessage()
            tweetUser = TwitterUser()
            tweetPlace = TwitterPlace()

            ''' message data '''
            tweetMessage.id = all_data['id']
            tweetMessage.id_str = all_data['id_str']
            tweetMessage.created_at = datetime.strptime(all_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
            tweetMessage.date = str(tweetMessage.created_at)[0:10]
            tweetMessage.favorite_count = all_data['favorite_count']
            tweetMessage.favorited = all_data['favorited']
            tweetMessage.lang = all_data['lang']
            tweetMessage.retweet_count = all_data['retweet_count']
            tweetMessage.retweeted = all_data['retweeted']
            tweetMessage.source = all_data['source']
            tweetMessage.text = all_data['text']

            bounding_box = all_data.pop('coordinates')
            if bounding_box:
                box = bounding_box.pop('coordinates')
                tweetMessage.longitude = box[0]
                tweetMessage.latitude = box[1]
                tweetMessage.coordinates = "POINT({} {})".format(tweetMessage.longitude, tweetMessage.latitude).replace(',', '.')

            ''' user data '''
            user = all_data.pop('user')
            if user:
                tweetUser.id = user['id']
                tweetUser.id_str = user['id_str']
                tweetUser.contributors_enabled = user['contributors_enabled']
                tweetUser.followers_count = user['followers_count']
                tweetUser.friends_count = user['friends_count']
                tweetUser.geo_enabled = user['geo_enabled']
                tweetUser.lang = user['lang']
                tweetUser.location = user['location']
                tweetUser.protected = user['protected']
                tweetUser.time_zone = user['time_zone']
                tweetUser.utc_offset = user['utc_offset']

            ''' place data '''
            place = all_data.pop('place')
            if place:
                tweetPlace.id = place['id']
                tweetPlace.bounding_box = None
                tweetPlace.country = place['country']
                tweetPlace.country_code = place['country_code']
                tweetPlace.full_name = place['full_name']
                tweetPlace.name = place['name']
                tweetPlace.place_type = place['place_type']

            try:
                self.cur.execute("""SET TimeZone = 'UTC' """)
                self.cur.execute(
                    "INSERT INTO " + conn_table + " (id, id_str, created_at, date, favorite_count, favorited, lang, retweet_count, retweeted, text, coordinates, " +
                    "user_contributors_enabled, user_followers_count, user_friends_count, user_geo_enabled, user_lang, user_location, user_protected, user_time_zone,user_utc_offset, " +
                    "place_country, place_country_code, place_full_name, place_name, place_place_type, tweet)" +
                    """VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s,4326), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (tweetMessage.id, tweetMessage.id_str, tweetMessage.created_at, tweetMessage.date,
                     tweetMessage.favorite_count, tweetMessage.favorited,
                     tweetMessage.lang, tweetMessage.retweet_count, tweetMessage.retweeted,
                     tweetMessage.text, tweetMessage.coordinates,
                     tweetUser.contributors_enabled, tweetUser.followers_count, tweetUser.friends_count,
                     tweetUser.geo_enabled, tweetUser.lang, tweetUser.location,
                     tweetUser.protected, tweetUser.time_zone, tweetUser.utc_offset, tweetPlace.country,
                     tweetPlace.country_code, tweetPlace.full_name, tweetPlace.name,
                     tweetPlace.place_type, tweet))
                self.conn.commit()
            except psycopg2.IntegrityError as e:
                self.conn.rollback()
                pass
