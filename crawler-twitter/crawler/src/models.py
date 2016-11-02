class TwitterMessage():
    def __init__(self):
        self.id = None
        self.id_str = None
        self.created_at = None
        self.date = None
        self.favorite_count = None
        self.favorited = None
        self.lang = None
        self.latitude = None
        self.longitude = None
        self.coordinates = None
        self.retweet_count = None
        self.retweeted = None
        self.source = None
        self.text = None


class TwitterUser():
    def __init__(self):
        self.id = None
        self.id_str = None
        self.contributors_enabled = None
        self.followers_count = None
        self.friends_count = None
        self.geo_enabled = None
        self.lang = None
        self.location = None
        self.protected = None
        self.time_zone = None
        self.utc_offset = None


class TwitterPlace():
    def __init__(self):
        self.id = None
        self.bounding_box = None  # polygon 4 pares
        self.country = None
        self.country_code = None
        self.full_name = None
        self.name = None
        self.place_type = None


class TwitterEntity():
    def __init__(self):
        self.created_at = None
