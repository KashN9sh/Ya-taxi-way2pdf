from datetime import timedelta
import urllib
from urllib import parse
from selenium import webdriver
import time
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import sys
from PyQt5 import QtWidgets
import MainWindow 

class Carrier():
    status = ''
    date = ''
    regNum = ''
    carrier = ''
    ogrn = ''
    inn = ''
    markAuto = ''
    modelAuto = ''
    gosReg = ''
    yearOfCreate  = ''
    NumberOfResolution = ''
    CompeteUL = ''
    DateOfCompete  = ''
    Region = ''
    OKPO = ''
    name = ''
    addres = ''
    phoneNumber = ''
    garajeNumber = ''
    driverLicense = ''
    category = ''

def parse(gosReg):

    params = {
        'number': gosReg,
        'name' : '',
        'id' : '',
        'region': 'ALL'
    }

    if params['number'] != '' :

        mtdi_url = f'https://mtdi.mosreg.ru/deyatelnost/celevye-programmy/taksi1/proverka-razresheniya-na-rabotu-taksi?{urllib.parse.urlencode(params)}'
        

        driver = webdriver.Safari()
        driver.get(mtdi_url)
        item = Carrier()

        #f = open("demofile2.txt", "a")

        item.status = ''
        j = 0

        while item.status != 'Действующее' :
            next = driver.find_elements_by_xpath("//a[@class='js-popup-open']")[j]
            next.click()
            
            arr = []
            for i in range(1, 15):
                table = driver.find_element_by_xpath(f"//div[@id='taxi-info']/div[@class='typical']/div[@class='table-responsive']/table/tbody/tr[{i}]/td[2]").text
                arr.append(table)
                
            item.status = arr[0]
            item.date = arr[1]
            item.regNum = arr[2]
            item.carrier = arr[3]
            item.ogrn = arr[4]
            item.inn = arr[5]
            item.markAuto = arr[6]
            item.modelAuto = arr[7]
            item.gosReg = arr[8]
            item.yearOfCreate = arr[9]
            item.NumberOfResolution = arr[10]
            item.CompeteUL = arr[11]
            item.DateOfCompete = arr[12].replace(' ', '').replace('\n', ' ')
            item.Region = arr[13]

            next = driver.find_element_by_xpath("//button[@class='mfp-close']")
            next.click()
            
            time.sleep(1)

            j += 1
        '''
        f.write(item.gosReg + ' : {\n')

        f.write('status : ' + item.status + '\n')
        f.write('date : ' + item.date + '\n')
        f.write('regNum : ' + item.regNum + '\n')
        f.write('carrier : ' + item.carrier + '\n')
        f.write('ogrn : ' + item.ogrn + '\n') 
        f.write('inn : ' + item.inn + '\n')
        f.write('markAuto : ' + item.markAuto + '\n')
        f.write('modelAuto : ' + item.modelAuto + '\n')
        f.write('gosReg : ' + item.gosReg + '\n')
        f.write('yearOfCreate : ' +  item.yearOfCreate + '\n')
        f.write('NumberOfResolution : '  + item.NumberOfResolution + '\n')
        f.write('CompeteUL : ' + item.CompeteUL + '\n')
        f.write('DateOfCompete : ' + item.DateOfCompete + '\n')
        f.write('Region : ' + item.Region + '\n')
        '''

        time.sleep(1)

        next = driver.find_element_by_xpath("//img[@alt='QR']")
        next.click()

        time.sleep(1)

        inn = {
            'inn' : item.inn
        }
        b_kontur_url = f'https://www.b-kontur.ru/profi/okpo-po-inn-ili-ogrn?{urllib.parse.urlencode(inn)}'
        
        driver.get(b_kontur_url)
        time.sleep(2)

        OKPO = driver.find_elements_by_xpath("//dd")[2].text
        item.OKPO = OKPO

        '''    
        f.write('OKPO : ' + item.OKPO + '\n')
        f.write('}\n')

        f.close()
        '''

        driver.close()

        return item

def makePDF(Carrier, dateFrom, dateTo):
    date = dateFrom
    canvas = Canvas("font-colors.pdf", pagesize = landscape(A4))

    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf'))

    while date != dateTo + timedelta(days = 1):
        canvas.setFont('FreeSans', 8)
        canvas.setLineWidth(0.5)

        canvas.drawString(75 * mm, 15 * mm, 'Показания одометра, км: ')
        canvas.line(110 * mm, 14.5 * mm, 140 * mm, 14.5 * mm)

        canvas.drawString(75 * mm, 22 * mm, 'Механик')
        canvas.line(90 * mm, 21.5 * mm, 110 * mm, 21.5 * mm)
        canvas.line(112 * mm, 21.5 * mm, 140 * mm, 21.5 * mm)

        canvas.drawString(10 * mm, 22 * mm, 'Водитель')
        canvas.line(24 * mm, 21.5 * mm, 44 * mm, 21.5 * mm)
        canvas.line(46 * mm, 21.5 * mm, 74 * mm, 21.5 * mm)

        canvas.drawString(75 * mm, 75 * mm, 'Диспетчер нарядчик')
        canvas.line(104 * mm, 74.5 * mm, 118 * mm, 74.5 * mm)
        canvas.line(120 * mm, 74.5 * mm, 140 * mm, 74.5 * mm)

        canvas.drawString(75 * mm, 82 * mm, 'Время возвращения в гараж')
        canvas.line(113 * mm, 81.5 * mm, 140 * mm, 81.5 * mm)

        canvas.drawString(75 * mm, 88 * mm, 'Диспетчер нарядчик')
        canvas.line(104 * mm, 87.5 * mm, 118 * mm, 87.5 * mm)
        canvas.line(120 * mm, 87.5 * mm, 140 * mm, 87.5 * mm)

        canvas.drawString(75 * mm, 95 * mm, 'Время выезда из гаража')
        canvas.line(110 * mm, 94.5 * mm, 140 * mm, 94.5 * mm)

        canvas.drawString(10 * mm, 95 * mm, 'Водитель')
        canvas.line(24 * mm, 94.5 * mm, 44 * mm, 94.5 * mm)
        canvas.line(46 * mm, 94.5 * mm, 74 * mm, 94.5 * mm)

        canvas.drawString(75 * mm, 112 * mm, 'Адрес подачи: ')
        canvas.line(95 * mm, 111.5 * mm, 140 * mm, 111.5 * mm)
        canvas.line(75 * mm, 106.5 * mm, 140 * mm, 106.5 * mm)
        canvas.line(75 * mm, 101.5 * mm, 140 * mm, 101.5 * mm)

        canvas.drawString(75 * mm, 123 * mm, 'В распоряжение организации: ')
        canvas.line(117 * mm, 122.5 * mm, 140 * mm, 122.5 * mm)
        canvas.line(75 * mm, 117.5 * mm, 140 * mm, 117.5 * mm)

        canvas.drawString(10 * mm, 112 * mm, 'Механик')
        canvas.line(24 * mm, 111.5 * mm, 44 * mm, 111.5 * mm)
        canvas.line(46 * mm, 111.5 * mm, 74 * mm, 111.5 * mm)

        canvas.drawString(10 * mm, 118 * mm, 'Выезд разрешён')
        canvas.line(33 * mm, 117 * mm, 74 * mm, 117 * mm)

        canvas.drawString(10 * mm, 123 * mm, 'Показания одометра, км: ')
        canvas.line(46 * mm, 122.5 * mm, 74 * mm, 122.5 * mm)

        canvas.drawString(75 * mm, 138 * mm, 'Категория: ')
        canvas.drawString(90 * mm, 138 * mm, Carrier.category)

        canvas.drawString(75 * mm, 142 * mm, 'Гаражный номер: ')
        canvas.drawString(100 * mm, 142 * mm, Carrier.garajeNumber)

        canvas.drawString(75 * mm, 148 * mm, 'Регистрационный № ')
        canvas.drawString(106 * mm, 148 * mm, Carrier.regNum + ' ' + Carrier.NumberOfResolution)

        canvas.drawString(10 * mm, 138 * mm, 'Водительское удостоверение №')
        canvas.drawString(54 * mm, 138 * mm, Carrier.driverLicense)

        canvas.drawString(10 * mm, 142 * mm, 'Водитель')
        canvas.drawString(30 * mm, 142 * mm, Carrier.name)

        canvas.drawString(10 * mm, 148 * mm, 'Лицензионная карточка: ')
        canvas.line(44 * mm, 147.5 * mm, 74 * mm, 147.5 * mm)

        canvas.drawString(10 * mm, 152 * mm, 'Государственный номерной знак: ')
        canvas.drawString(60 * mm, 152 * mm, Carrier.gosReg)

        canvas.drawString(10 * mm, 156 * mm, 'Марка и модель автомобиля: ')
        canvas.drawString(55 * mm, 156 * mm, Carrier.markAuto + ' ' + Carrier.modelAuto)

        canvas.drawString(10 * mm, 159 * mm, 'Организация: ')
        canvas.drawString(30 * mm, 159 * mm, Carrier.CompeteUL )

        canvas.drawString(10 * mm, 192 * mm, 'Телефон: ')
        canvas.drawString(30 * mm, 192 * mm, Carrier.phoneNumber)

        canvas.drawString(10 * mm, 196 * mm, 'Адрес: ')
        canvas.drawString(30 * mm, 196 * mm, Carrier.addres)

        canvas.drawString(10 * mm, 200 * mm, 'Перевозчик: ')
        canvas.drawString(30 * mm, 200 * mm, Carrier.carrier)

        canvas.drawString(105 * mm, 192 * mm, 'ОГРН: ')
        canvas.drawString(116 * mm, 192 * mm, Carrier.ogrn)

        canvas.drawString(112 * mm, 196 * mm, 'ИНН: ')
        canvas.drawString(120 * mm, 196 * mm, Carrier.inn)

        canvas.drawString(113 * mm, 200 * mm, 'ОКПО: ')
        canvas.drawString(125 * mm, 200 * mm, Carrier.OKPO)

        canvas.drawString(60 * mm, 175 * mm, date.strftime('«‎%d»‎ %B %Y'))

        canvas.setFont('FreeSans', 6)

        canvas.drawString(38 * mm, 168 * mm, 'Вид перевозок: перевозки пассажиров и багажа по заказам такси')
        canvas.drawString(28 * mm, 166 * mm, 'Виды сообщения: местное, городское, пригородное, междугороднее, международное')
        canvas.drawString(63 * mm, 164 * mm, '(ненужное зачеркнуть)')

        canvas.drawString(28 * mm, 108 * mm, '(подпись)')
        canvas.drawString(51 * mm, 108 * mm, '(расшифровка)')

        canvas.drawString(28 * mm, 91 * mm, '(подпись)')
        canvas.drawString(51 * mm, 91 * mm, '(расшифровка)')

        canvas.drawString(107 * mm, 85 * mm, '(подпись)')
        canvas.drawString(121 * mm, 85 * mm, '(расшифровка)')

        canvas.drawString(107 * mm, 71 * mm, '(подпись)')
        canvas.drawString(121 * mm, 71 * mm, '(расшифровка)')

        canvas.drawString(28 * mm, 18 * mm, '(подпись)')
        canvas.drawString(51 * mm, 18 * mm, '(расшифровка)')

        canvas.drawString(94 * mm, 18 * mm, '(подпись)')
        canvas.drawString(117 * mm, 18 * mm, '(расшифровка)')

        canvas.drawString(119 * mm, 78 * mm, '(ЧЧ:ММ)')
        canvas.drawString(119 * mm, 91 * mm, '(ЧЧ:ММ)')

        canvas.setFont('FreeSansBold', 9)

        canvas.drawString(90 * mm, 28 * mm, 'Автомобиль принял')
        canvas.drawString(25 * mm, 28 * mm, 'Автомобиль сдал')

        canvas.drawString(87 * mm, 63 * mm, 'медицинский осмотр')
        canvas.drawString(85 * mm, 66 * mm, 'Прошёл послерейсовый')

        canvas.drawString(23 * mm, 60 * mm, 'обязанностей допущен')
        canvas.drawString(16 * mm, 63 * mm, 'осмотр, к исполнению трудовых')
        canvas.drawString(13 * mm, 66 * mm, 'Прошёл предрейсовый медицинский')

        canvas.drawString(20 * mm, 100 * mm, 'исправном состоянии принял')
        canvas.drawString(23 * mm, 103 * mm, 'Автомобиль в технически')

        canvas.drawString(17 * mm, 129 * mm, 'Автомобиль технически исправен')
        canvas.drawString(91 * mm, 129 * mm, 'Задание водителю')

        canvas.drawString(30 * mm, 185 * mm, 'ПУТЕВОЙ ЛИСТ ЛЕГКОВОГО АВТОМОБИЛЯ ТАКСИ')

        canvas.setFont('FreeSansBold', 6)
        canvas.drawString(64 * mm, 182 * mm, 'серия:')

        canvas.showPage()
        date += timedelta(days = 1)

    canvas.save()

'''
if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
'''
class App(QtWidgets.QMainWindow, MainWindow.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.workbtn.clicked.connect(self.work)
    
    def work(self):
        CarrierForParse = Carrier()
        CarrierForParse = parse(self.gosNum.text())
        CarrierForParse.name = self.name.text()
        CarrierForParse.addres = self.addres.text()
        CarrierForParse.phoneNumber = self.phoneNumber.text()
        CarrierForParse.garajeNumber = self.garajeNumber.text()
        CarrierForParse.driverLicense = self.driverLicense.text()
        CarrierForParse.category = self.category.text()
        makePDF(CarrierForParse,self.dateEditFrom.date().toPyDate(), self.dateEditTo.date().toPyDate())

def main():
    app = QtWidgets.QApplication(sys.argv) 
    window = App()
    window.show()
    app.exec_() 

if __name__ == '__main__':
    main() 