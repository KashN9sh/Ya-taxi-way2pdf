from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

canvas = Canvas("font-colors.pdf", pagesize = landscape(A4))

# Set font to Times New Roman with 12-point size
pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf'))
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
canvas.line(90 * mm, 137.5 * mm, 140 * mm, 137.5 * mm)

canvas.drawString(75 * mm, 142 * mm, 'Гаражный номер: ')
canvas.line(100 * mm, 141.5 * mm, 140 * mm, 141.5 * mm)

canvas.drawString(75 * mm, 148 * mm, 'Регистрационный № ')
canvas.line(104 * mm, 147.5 * mm, 140 * mm, 147.5 * mm)

canvas.drawString(10 * mm, 138 * mm, 'Водительское удостоверение №')
canvas.line(54 * mm, 137.5 * mm, 74 * mm, 137.5 * mm)

canvas.drawString(10 * mm, 142 * mm, 'Водитель')
canvas.line(24 * mm, 141.5 * mm, 74 * mm, 141.5 * mm)

canvas.drawString(10 * mm, 148 * mm, 'Лицензионная карточка: ')
canvas.line(44 * mm, 147.5 * mm, 74 * mm, 147.5 * mm)

canvas.drawString(10 * mm, 152 * mm, 'Государственный номерной знак: ')
canvas.line(57 * mm, 151.5 * mm, 140 * mm, 151.5 * mm)

canvas.drawString(10 * mm, 156 * mm, 'Марка и модель автомобиля: ')
canvas.line(50 * mm, 155.5 * mm, 140 * mm, 155.5 * mm)

canvas.drawString(10 * mm, 192 * mm, 'Телефон: ')

canvas.drawString(10 * mm, 196 * mm, 'Адрес: ')

canvas.drawString(10 * mm, 200 * mm, 'Перевозчик: ')

canvas.drawString(105 * mm, 192 * mm, 'ОГРН: ')

canvas.drawString(112 * mm, 196 * mm, 'ИНН: ')

canvas.drawString(113 * mm, 200 * mm, 'ОКПО: ')

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

# Save the PDF file
canvas.save()