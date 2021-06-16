import scrapy
from scrapy.http import FormRequest 
from product_scraper.items import Product
import urllib
from scrapy.shell import inspect_response
 
class EcomSpider(scrapy.Spider):
    name = 'ecom_spider'
    params = {
            'number': 'у019ао797',
            'name' : '',
            'id' : '',
            'region': 'ALL'
        }
    allowed_domains = ['https://mtdi.mosreg.ru/deyatelnost/celevye-programmy/taksi1/']
    start_urls = [f'https://mtdi.mosreg.ru/deyatelnost/celevye-programmy/taksi1/proverka-razresheniya-na-rabotu-taksi?{urllib.parse.urlencode(params)}']
    #start_urls = ['https://mtdi.mosreg.ru/deyatelnost/celevye-programmy/taksi1/proverka-razresheniya-na-rabotu-taksi']
    #start_urls = ['https://mtdi.mosreg.ru/deyatelnost/celevye-programmy/taksi1/proverka-razresheniya-na-rabotu-taksi?number=%D1%83019%D0%B0%D0%BE797&name=&id=&region=ALL']

    def parse(self, response):
        #print(response.url)
        item = Product()
        item['product_url'] = response.url
        print('---------------')
        print(item['product_url'])
        print('---------------')
        table = response.xpath('//table//tbody')
        rows = table.xpath('//tr')
        print(len(rows.getall()))
        row = rows[len(rows.getall()) - 1]
        print(row.xpath('td//text()')[0].extract())
        #inspect_response(response, self)
        '''
        frmdata = {"number":"у019ао797"}
        request = scrapy.Request( start_urls, method='POST', 
                          body=json.dumps(frmdata), 
                          headers={'Content-Type':'application/json'} )
        
        table = response.xpath("*[@class='table-responsive']//table//tbody")
        rows = table.xpath('//tr')
        item['price'] = response.xpath("//div[@class='table-responsive']//table//tbody/tr/td/text()").get()
        #item['title'] = response.xpath('//section[1]//h2/text()').get()
        #item['img_url'] = response.xpath("//div[@class='product-slider']//img/@src").get(0)
        '''
        return item