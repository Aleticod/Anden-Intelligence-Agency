# Import the scrapy framework
import scrapy

# XPATH


# links = //a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href
# title = //h1[@class="documentFirstHeading"]/text()
# paragraph = //div[@class="field-item even"]//p[not(@class)]/text()


# Spider class
class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]

    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # custom_settings = {
    #     'FEEDS': {
    #         'cia.json' : {
    #             'format': 'json',
    #             'encoding': 'utf-8',
    #             'store_empty': False,
    #             'fields': None,
    #             'indent': 4,
    #             'item_export_kwargs': {
    #                 'export_empty_fields': True
    #             }

    #         }
    #     }
    # }

    # Method parse

    def parse(self, response):

        links_declassified = response.xpath('//a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href').getall()

        for link in links_declassified:

            yield response.follow(link, callback=self.parse_link, cb_kwargs = {'url': response.urljoin(link)})


    
    def parse_link(self, response, **kwargs):

        # if kwargs:
        link = kwargs['url']

        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()

        paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)][3]/text()').get()

        yield {
            'url': link,
            'title': title,
            'body': paragraph
        }