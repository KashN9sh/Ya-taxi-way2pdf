import cv2,time
import numpy as np
import pytesseract

img = cv2.imread('half5.png')
img2 = img

height, width, channels = img.shape
# Number of pieces Horizontally
CROP_W_SIZE  = 1
# Number of pieces Vertically to each Horizontal
CROP_H_SIZE = 2

img_array = []
for ih in range(CROP_H_SIZE ):
    for iw in range(CROP_W_SIZE ):

        x = width/CROP_W_SIZE * iw
        y = height/CROP_H_SIZE * ih
        h = (height / CROP_H_SIZE)
        w = (width / CROP_W_SIZE )
        print(x,y,h,w)
        img_array.append(img[int(y) : int(y+h), int(x) : int(x+w)])



        NAME = str(time.time())
        #cv2.imwrite(str(time.time()) +  ".png",img_array[ih])
        img = img2

i=0
letters = []

img = img_array[0]

i += 1
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
binary = cv2.resize(binary, (binary.shape[1] * 2, binary.shape[0]))
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

y1 = 0
letter = []
j = 0
for idx, contour in enumerate(contours):
    (x, y, w, h) = cv2.boundingRect(contour)
    # print("R", idx, x, y, w, h, cv2.contourArea(contour), hierarchy[0][idx])
    # hierarchy[i][0]: the index of the next contour of the same level
    # hierarchy[i][1]: the index of the previous contour of the same level
    # hierarchy[i][2]: the index of the first child
    # hierarchy[i][3]: the index of the parent

    if idx == len(contours) - 1:
        letters.append(letter)

    if w > 20 and h > 34:
        if hierarchy[0][idx][3] == 0:
            if abs(y - y1) > 20:
                y1 = y
                j += 1
                if letter != [] :
                    letters.append(letter)
                letter = []

            #cv2.rectangle(binary, (x - 5, y - 5), (x + w + 5, y + h + 5), (70, 0, 0), 1)
            letter_crop = binary[int(y - 5) : int(y + h + 5), int(x - 5) : int(x + w + 5)]
            size_max = max(w, h)
            #letter_square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)
            if j == 1:
                letter.append((x, y//20, cv2.resize(letter_crop, (28, 56), interpolation = cv2.INTER_AREA)))
            else:
                letter.append((x, y // 20, cv2.resize(letter_crop, (56, 60), interpolation=cv2.INTER_AREA)))
cv2.imwrite(str(i) + ".png", binary)
#letters.sort(key=lambda x: x[0], reverse=False)
for i in range(len(letters)):
    #letters[i] = sorted(sorted(letters[i], key = lambda x : x[0]), key = lambda x : x[1], reverse = True)
    letters[i] = sorted(letters[i], key = lambda x: x[0])

j=0
#ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮйцукенгшщзхъфывапролджэёячсмитьбю
config1 = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
config2 = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮйцукенгшщзхъфывапролджэёячсмитьбю'

data = ''

for i in  range(len(letters)):
    for letter in range(len(letters[i])):
        if i == 0:
            data += pytesseract.image_to_string(letters[i][letter][2], config = config1, lang = 'rus')[0]
        else:
            data += pytesseract.image_to_string(letters[i][letter][2], config=config2, lang='rus')[0]
        #print(data[0])
        #cv2.imshow(f'img{j}', letters[i][letter][2])
        #cv2.waitKey(0)
        j+=1
    print(data)
    data = ''
