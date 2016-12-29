import sys

sys.path.append('..')
sys.path.append('../..')
import scrapy

from newsScra.items import NewsItem


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            'http://www.ithome.com/list/list_1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_links = response.xpath('//div[@class="post_list"]//a[@target="_blank"]/@href').extract()
        for news_link in news_links:
            yield scrapy.Request(news_link, callback=self.parse_news_item)
            next_page = response.xpath('//div[@class="pagenew"]/a[last()]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page,callback=self.parse)

    def parse_news_item(self, response):
        item = NewsItem()
        self.parse_title(response, item)
        self.parse_time(response, item)
        self.parse_category(response, item)
        yield item

    def parse_title(self, response, item):
        title = response.xpath('//div[@class="post_title"]/h1/text()').extract_first()
        item['title'] = title

    def parse_time(self, response, item):
        time = response.xpath('//span[@id="pubtime_baidu"]/text()').extract_first()
        item['time'] = time

    def parse_category(self, response, item):
        category = response.xpath('//div[@class="current_nav"]/a[last()]/text()').extract_first()
        item['category'] = category
