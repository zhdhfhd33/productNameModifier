from PIL import Image
import cv2

from main.core import *

img1 = cv2.imread('C:\\Users\\minkun\\OneDrive\\minkun\\pyCharmWP\\productNameModifier\\main\\resources\\logo.png')
img2 = cv2.imread('C:/Users/minkun/OneDrive/minkun/pyCharmWP/productNameModifier/test/resources/imgs/test_img.jpg')
cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)  # open cv는 BGR로 나타낸다.
print(type(img1))

# print(img1)
# print(img2) # 이미지는 5차원이다. 2차원 x,y좌표. 그 안에 3차원 RGB값.

#
nrows, ncols, nchannels = img1.shape
print(f'img1. shape : {img1.shape}')

#
roi = img2[10:10 + nrows, 10:10 + ncols]  # x, y 좌표 먼저 정하고 그 다음 rgb값이 있다.

mask = get_img_mask(img1, 255, 255, 255)  # 흰색 찾는다. 흰색=255. 로고가 있는 곳을 검정(0)인 마스크 이미지 생성
cv2.imshow('mask', mask)
# mask_inv = cv2.bitwise_not(mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imshow('asdf', mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


roi_bg = cv2.bitwise_and(roi, roi, mask=mask)  # 로고있는 곳은 검정(0)으로 만듦..
cv2.imshow('roi_bg', roi_bg)
cv2.waitKey(0)
cv2.destroyAllWindows()

# TODO : 이미지 경계선에 흰부분이 남는다. bitwise_not()하면서 경계가 생김.. 다른 방법은 없나??..
mask_inv = cv2.bitwise_not(mask)
bgremove_logo = cv2.bitwise_and(img1, img1, mask=mask_inv)  # 로고배경제거
cv2.imshow('bgremove_logo', bgremove_logo)
cv2.waitKey(0)
cv2.destroyAllWindows()

res = cv2.add(roi_bg, bgremove_logo)  # 로고 씌우기
cv2.imshow('res', res)
cv2.waitKey(0)
cv2.destroyAllWindows()

#
img2[10:10 + nrows, 10:10 + ncols] = res
#
cv2.imshow('resutl', img2)
cv2.destroyAllWindows()
cv2.waitKey(0)


