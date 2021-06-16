import scrapy
 
class Product(scrapy.Item):
    product_url = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()