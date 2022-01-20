from datetime import date

import xlwt
import xlrd
from xlutils.copy import copy

import Config

def _get_ru_long_date(date):
    ru_month = ["января", "февраля", "марта", "апреля",
                "мая", "июня", "июля", "августа",
                "сентября", "октября", "ноября", "декабря"]
    return "«%d» %s %d год" % (date.day, ru_month[date.month - 1], date.year)


def _get_ru_short_date(date):
    ru_month = ["Январь", "Февраль", "Март", "Апрель",
                "Май", "Июнь", "Июль", "Август",
                "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    return "%s %d г." % (ru_month[date.month - 1], date.year)


def create_statement(template_file, payments_list):
    font0 = xlwt.Font()
    font0.name = "Times New Roman"
    font0.height = 12 * 20

    style0 = xlwt.XFStyle()
    style0.font = font0
    rb = xlrd.open_workbook(filename=template_file, on_demand=True, formatting_info=True)
    wb = copy(rb)
    sheet1 = wb.get_sheet(wb.sheet_index("Info"))
    sheet2 = wb.get_sheet(wb.sheet_index("Payments"))
    #itr1 = 14
    itr2 = 1

    sum = 0
    for row in payments_list:
        sum += row[4]
        tmp = " ".join([row[0], row[1], row[2]]).upper()
        '''sheet1.write(itr1, 2, tmp, style0)
        sheet1.write(itr1, 3, row[3], style0)
        sheet1.write(itr1, 4, row[4], style0)'''
        sheet2.write(itr2, 0, row[3], style0)
        sheet2.write(itr2, 1, row[4], style0)
        #itr1 += 1
        itr2 += 1

    short_today = _get_ru_short_date(date.today())
    long_today = _get_ru_long_date(date.today())

    sheet1.write(5, 1, date.today().strftime("%d.%m.%Y"))

    '''sheet1.write( 9, 1, "за " + short_today, style0)
    sheet1.write(10, 1, "согласно платежному поручению № !!! от %sа" % long_today, style0)
    sheet1.write(12, 5, long_today, style0)

    sheet1.write(36, 1, "Итого: %d количество перечислений" % len(payments_list), style0)
    sheet1.write(37, 1, "%d количество Работников" % len(payments_list), style0)
    sheet1.write(38, 1, "%d рублей" % sum, style0)'''

    filename = Config.statement_file.format(date.today())
    # filename.encode()

    wb.save(filename)
    return filename
