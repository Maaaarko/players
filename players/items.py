import scrapy


class PlayerInfoItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    date_of_birth = scrapy.Field()
    age = scrapy.Field()
    place_of_birth = scrapy.Field()
    country_of_birth = scrapy.Field()
    positions = scrapy.Field()
    current_club = scrapy.Field()
    national_team = scrapy.Field()
    appearances_in_current_club = scrapy.Field()
    goals_in_current_club = scrapy.Field()
    timestamp = scrapy.Field()
