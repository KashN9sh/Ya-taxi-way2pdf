import scrapy
from scrapy.http import FormRequest 
from product_scraper.items import Product
import urllib
from scrapy.shell import inspect_response
from selenium import webdriver
import time
 
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
 
    def __init__(self):
        self.driver = webdriver.Safari()

    def parse(self, response):
        #print(response.url)
        self.driver.get(response.url)
        item = Product()

        print('---------------')

        f = open("demofile2.txt", "a")

        item['status'] = ''
        j = 0

        while item['status'] != 'Действующее' :
            next = self.driver.find_elements_by_xpath("//a[@class='js-popup-open']")[j]
            next.click()
            
            arr = []
            for i in range(1, 15):
                table = self.driver.find_element_by_xpath(f"//div[@id='taxi-info']/div[@class='typical']/div[@class='table-responsive']/table/tbody/tr[{i}]/td[2]").text
                arr.append(table)
                
            item['status'] = arr[0]
            item['date'] = arr[1]
            item['regNum'] = arr[2]
            item['carrier'] = arr[3]
            item['ogrn'] = arr[4]
            item['inn'] = arr[5]
            item['markAuto'] = arr[6]
            item['modelAuto'] = arr[7]
            item['gosReg'] = arr[8]
            item['yearOfCreate'] = arr[9]
            item['NumberOfResolution'] = arr[10]
            item['CompeteUL'] = arr[11]
            item['DateOfCompete'] = arr[12].replace(' ', '').replace('\n', ' ')
            item['Region'] = arr[13]

            next = self.driver.find_element_by_xpath("//button[@class='mfp-close']")
            next.click()
            
            time.sleep(1)

            next = self.driver.find_elements_by_xpath("//img[@alt='QR']")[j]
            next.click()

            j += 1

        f.write(item['gosReg'] + ' : {\n')

        f.write('status : ' + item['status'] + '\n')
        f.write('date : ' + item['date'] + '\n')
        f.write('regNum : ' + item['regNum'] + '\n')
        f.write('carrier : ' + item['carrier'] + '\n')
        f.write('ogrn : ' + item['ogrn'] + '\n') 
        f.write('inn : ' + item['inn'] + '\n')
        f.write('markAuto : ' + item['markAuto'] + '\n')
        f.write('modelAuto : ' + item['modelAuto'] + '\n')
        f.write('gosReg : ' + item['gosReg'] + '\n')
        f.write('yearOfCreate : ' +  item['yearOfCreate'] + '\n')
        f.write('NumberOfResolution : '  + item['NumberOfResolution'] + '\n')
        f.write('CompeteUL : ' + item['CompeteUL'] + '\n')
        f.write('DateOfCompete : ' + item['DateOfCompete'] + '\n')
        f.write('Region : ' + item['Region'] + '\n')

        f.write('}\n')

        f.close()

        print('---------------')
        self.driver.close()
        #table = self.driver.find_element_by_xpath("//div[@class='popup']/table//tbody//tr").text
        #print(table)
        #inspect_response(response, self)
        

        '''
        #print(rows.xpath('a//text()').extract())
        

        
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