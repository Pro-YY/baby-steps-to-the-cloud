import scrapy
from scrapy import Request
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin

from scrapyspider.items import TsinghuaItem


class tsinghuaSpider(scrapy.Spider):
    name = 'tsinghua'
    allowed_domains = ['www.tsinghua.edu.cn']
    start_urls = ['https://www.tsinghua.edu.cn/szdw1/jcrc/lyys1.htm', ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapyspider.pipelines.MyImagesPipeline': 400,
            'scrapyspider.pipelines.InsertDBPipeline': 300
        },
    }

    def parse(self, response, **kwargs):
        href_list = response.css('div.yuanShi a::attr(href)').extract()
        for href in href_list:
            yield Request(url=urljoin(get_base_url(response), href), callback=self.parse_detail)

    def parse_detail(self, response, **kwargs):
        teacher_name = self.trim(str(response.css('header.contentNav h1::text').extract()))
        content = self.trim(str(response.css("div.v_news_content *::text").extract()))
        image_url = urljoin(get_base_url(response), str(response.css('div.yS img::attr(src)').extract()))
        item = TsinghuaItem()
        item['teacher_name'] = teacher_name
        item['content'] = content
        item['image_url'] = image_url
        yield item

    @staticmethod
    def trim(value: str):
        if value is None:
            return ''
        bad_chars = ['\n', '\t', '\u3000', '\xa0', ' ', '\r', '&nbsp', '\r\n']
        for char in bad_chars:
            value = value.replace(char, '')
        return value.strip()
