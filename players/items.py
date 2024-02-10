import scrapy


class PlayerInfoItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    dob = scrapy.Field()
    age = scrapy.Field()
    place_of_birth = scrapy.Field()
    country_of_birth = scrapy.Field()
    positions = scrapy.Field()
    current_club = scrapy.Field()
    national_team = scrapy.Field()
    appearances = scrapy.Field()
    goals = scrapy.Field()
    timestamp = scrapy.Field()
