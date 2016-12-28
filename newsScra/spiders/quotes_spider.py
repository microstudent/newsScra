import scrapy
from scrapy.loader import ItemLoader


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://www.ithome.com/list/list_1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
    	itemLoader = ItemLoader(item = News(), response = response)
    	itemLoader.add_xpath('title','//div[@class="post_list"]//a[@target="_blank"]/text()')
    	itemLoader.add_xpath('time','//div[@class="post_list"]//span[@class="cate"]/text()')
    	itemLoader.add_xpath('category','//div[@class="post_list"]//a[@target="_blank"]/text()')
    	yield itemLoader.load_item()

    	next_page = response.xpath('//div[@class="pagenew"]/a[last()]/@href').extract_first()
    	if next_page is not None:
    		next_page = response.urljoin(next_page)
    		yield scrapy.Request(next_page,callback=self.parse)

class News(scrapy.Item):
	title =scrapy.Field()
	time = scrapy.Field()
	category = scrapy.Field()
