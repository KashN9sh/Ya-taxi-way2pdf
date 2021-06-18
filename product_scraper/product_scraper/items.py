import scrapy
 
class Product(scrapy.Item):
    status = scrapy.Field()
    date = scrapy.Field()
    regNum = scrapy.Field()
    carrier = scrapy.Field()
    ogrn = scrapy.Field()
    inn = scrapy.Field()
    markAuto = scrapy.Field()
    modelAuto = scrapy.Field()
    gosReg = scrapy.Field()
    yearOfCreate  = scrapy.Field()
    NumberOfResolution = scrapy.Field()
    CompeteUL = scrapy.Field()
    DateOfCompete  = scrapy.Field()
    Region = scrapy.Field()