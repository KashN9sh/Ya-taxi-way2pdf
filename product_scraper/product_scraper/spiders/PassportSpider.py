import cv2
import pytesseract

# Путь для подключения tesseract
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Подключение фото
img = cv2.imread('yourPhoto.jpeg')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#_____END_____#

img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
se=cv2.getStructuringElement(cv2.MORPH_RECT, (2048,2048))
bg=cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
out_gray=cv2.divide(img, bg, scale=255)
out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1]

#out_gray = cv2.medianBlur(out_gray, 1)
#out_binary = cv2.medianBlur(out_binary, 1)


#cv2.imshow('binary', out_binary)
#cv2.imwrite('binary.png',out_binary)

cv2.imshow('gray', out_gray)
cv2.imwrite('gray.png',out_gray)


# Будет выведен весь текст с картинки
config = r'--oem 3 --psm 6'
data = pytesseract.image_to_string(out_gray, config=config, lang='rus')

# Делаем нечто более крутое!!!

#print(pytesseract.image_to_data(out_gray, config=config, lang='rus'))

# Перебираем данные про текстовые надписи
for i, el in enumerate(data.splitlines()):
	if i == 0:
		continue

	el = el.split()
	try:
		# Создаем подписи на картинке
		x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
		cv2.rectangle(out_binary, (x, y), (w + x, h + y), (0, 0, 255), 1)
		cv2.putText(out_binary, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
	except IndexError:
		print("Операция была пропущена")

# Отображаем фото
cv2.imshow('Result', out_gray)
cv2.waitKey(0)