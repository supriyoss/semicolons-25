import pytesseract
import cv2
from matplotlib import pyplot as plt

# load the original image
image = cv2.imread(r'./resources/Claim_Bills_page_006.jpg')

# get co-ordinates to crop the image
# c = line_items_coordinates[1]
#
# # cropping image img = image[y0:y1, x0:x1]
# img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]

# plt.figure(figsize=(10,10))
# plt.imshow(img)
#
# # convert the image to black and white for better OCR
# ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
text = str(pytesseract.image_to_string(image)) #, config='--psm 6'
print(text)