# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TsinghuaItem(scrapy.Item):
    teacher_name = scrapy.Field()
    content = scrapy.Field()
    image_url = scrapy.Field()

    def __init__(self):
        super(TsinghuaItem, self).__init__()
        for key in self.fields:
            self._values[key] = ''


class MicroInfoItem(scrapy.Item):
    company = scrapy.Field()
    location = scrapy.Field()
    company_date = scrapy.Field()
    level_name = scrapy.Field()
    tag = scrapy.Field()
    years_at_company = scrapy.Field()
    years_of_experience = scrapy.Field()
    total_compensation = scrapy.Field()
    base = scrapy.Field()
    stock = scrapy.Field()
    bonus = scrapy.Field()

    def __init__(self):
        super(MicroInfoItem, self).__init__()
        for key in self.fields:
            self._values[key] = ''
