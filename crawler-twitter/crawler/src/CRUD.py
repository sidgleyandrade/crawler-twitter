import pytz
import copy
import json
import logging
import psycopg2

from tweepy.streaming import json
from datetime import datetime

from crawler.src.models import TwitterMessage
from crawler.src.models import TwitterUser
from crawler.src.models import TwitterPlace
from crawler.src.db.DBConnection import DBConnection


class CRUD:
    def __init__(self, path_home, conn_sec):
        self.set_up(path_home, conn_sec)

    def set_up(self, path_home, conn_sec):
        try:
            self.conn = DBConnection(path_home, conn_sec).connect_database()
            self.cur = self.conn.cursor()
        except Exception as e:
            raise e

    def save(self, tweet=None, conn_table=""):
        all_data = copy.deepcopy(json.loads(tweet))

        if tweet:
            tweet_message = TwitterMessage()
            tweet_user = TwitterUser()
            tweet_place = TwitterPlace()

            tweet_message.id = all_data['id']
            tweet_message.id_str = all_data['id_str']
            tweet_message.created_at = datetime.strptime(
                all_data['created_at'],
                '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
            tweet_message.date = str(tweet_message.created_at)[0:10]
            tweet_message.favorite_count = all_data['favorite_count']
            tweet_message.favorited = all_data['favorited']
            tweet_message.lang = all_data['lang']
            tweet_message.retweet_count = all_data['retweet_count']
            tweet_message.retweeted = all_data['retweeted']
            tweet_message.source = all_data['source']
            tweet_message.text = all_data['text']
            bounding_box = all_data.pop('coordinates')
            if bounding_box:
                box = bounding_box.pop('coordinates')
                tweet_message.longitude = box[0]
                tweet_message.latitude = box[1]
                tweet_message.coordinates = "POINT({} {})".\
                    format(tweet_message.longitude, tweet_message.latitude).replace(',', '.')

            user = all_data.pop('user')
            if user:
                tweet_user.id = user['id']
                tweet_user.id_str = user['id_str']
                tweet_user.name = user['name']
                tweet_user.screen_name = user['screen_name']
                tweet_user.contributors_enabled = user['contributors_enabled']
                tweet_user.followers_count = user['followers_count']
                tweet_user.friends_count = user['friends_count']
                tweet_user.geo_enabled = user['geo_enabled']
                tweet_user.lang = user['lang']
                tweet_user.location = user['location']
                tweet_user.protected = user['protected']
                tweet_user.time_zone = user['time_zone']
                tweet_user.utc_offset = user['utc_offset']

            place = all_data.pop('place')
            if place:
                tweet_place.id = place['id']
                tweet_place.bounding_box = None
                tweet_place.country = place['country']
                tweet_place.country_code = place['country_code']
                tweet_place.full_name = place['full_name']
                tweet_place.name = place['name']
                tweet_place.place_type = place['place_type']

            try:
                self.cur.execute("""SET TimeZone = 'UTC' """)
                self.cur.execute("""INSERT INTO """ + conn_table + """ 
                (id, id_str, created_at, date, favorite_count, favorited, 
                lang, retweet_count, retweeted, text, 
                user_contributors_enabled, user_followers_count, 
                user_friends_count, user_geo_enabled, user_lang, user_location, 
                user_protected, user_time_zone, user_utc_offset, place_country, 
                place_country_code, place_full_name, place_name, 
                place_place_type, tweet, coordinates, user_id, user_id_str, 
                user_name, user_screen_name) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                ST_GeomFromText(%s,4326), %s, %s, %s, %s)""",
                                 (tweet_message.id,
                                  tweet_message.id_str,
                                  tweet_message.created_at,
                                  tweet_message.date,
                                  tweet_message.favorite_count,
                                  tweet_message.favorited,
                                  tweet_message.lang,
                                  tweet_message.retweet_count,
                                  tweet_message.retweeted,
                                  tweet_message.text,
                                  tweet_user.contributors_enabled,
                                  tweet_user.followers_count,
                                  tweet_user.friends_count,
                                  tweet_user.geo_enabled,
                                  tweet_user.lang,
                                  tweet_user.location,
                                  tweet_user.protected,
                                  tweet_user.time_zone,
                                  tweet_user.utc_offset,
                                  tweet_place.country,
                                  tweet_place.country_code,
                                  tweet_place.full_name,
                                  tweet_place.name,
                                  tweet_place.place_type,
                                  tweet,
                                  tweet_message.coordinates,
                                  tweet_user.id,
                                  tweet_user.id_str,
                                  tweet_user.name,
                                  tweet_user.screen_name))
                self.conn.commit()
            except psycopg2.IntegrityError:
                self.conn.rollback()
                pass
