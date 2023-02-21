
# 전역 함수
import numpy as np
import pandas as pd
import re
import cv2
import PIL.Image


INT_MAX=int(2e9) # 대충 20억


def pdConfig():
    pd.set_option('display.max_columns', None)  # 전체 열 보기
    pd.set_option('display.max_rows', None)  # 전체 행 보기
    pd.set_option('mode.chained_assignment', None)  # SettingWithCopyWarning 경고 끈다


def simple_minlen_name_similarity(a, b):
  """
  가장 단순한 방법으로 이름 유사도를 측정.
  return : cnt, MIN_LEN,MAX_LEN
  이름의 일부일 수도 있기 때문에 MIN_LEN이 맞을 것 같기두?
  cnt/MAX를 쓸 수도 있을 것.
  """
  LEN_A=len(a)
  LEN_B=len(b)
  MAX_LEN = max(LEN_A, LEN_B)
  MIN_LEN = min(LEN_A, LEN_B)
  cnt = 0
  for i in range(MIN_LEN):
    if a[i]!=b[i]:
      break
    cnt+=1
  return cnt/MIN_LEN

def get_file_name(path, sep):
    """
    :param path: "C:/Users/minkun/Downloads/최저가확인관 최근순.xls"

    :param sep: '/' or '\\'
    :return: file_name, extension
    """
    li = path.split(sep=sep)
    full_name = li[len(li)-1]
    extension_idx = full_name.rfind('.')

    extension = full_name[extension_idx+1:]
    file_name = full_name[:extension_idx]
    return file_name, extension

def replace_by_regexp(strs, find_strs, replace_strs):
    """
    코어함수
    :param strs: [str1, str2, str3, ,,,]
    :param find_strs: 찾고자하는 정규표현식 리스트 ['\\s+',,] 공백 여러 개를 공백 하나로 바꾼다.
    :param repalceStrs: 이 문자열로 바꾸자 [' ',,]
    :return: filteredNames, del_logs
    """
    filteredNames = []
    del_logs = []
    for i, val_i in enumerate(strs):  # [상품1, 상품2, 상품3]
        filteredName = val_i
        for j, val_j in enumerate(find_strs):  # val_j = 정규표현식
            regex = re.compile(f'{val_j}')
            indicies = [_ for _ in re.finditer(regex, filteredName)]  # 문자를 찾은 인덱스 정보
            LEN = len(indicies)
            for k in range(LEN - 1, -1, -1):  # 특수문자가 있는 인덱스의 자리. 뒤에서 부터 삭제. 영향 안받는다. 0까지 하고 싶으면 -1로 설정해야한다.
                startIdx = indicies[k].span()[0]
                endIdx = indicies[k].span()[1]
                del_content = filteredName[startIdx:endIdx]
                filteredName = filteredName[:startIdx] + replace_strs[j] + filteredName[endIdx:]
                del_logs.append(DelLog(i, del_content, val_j))
        filteredNames.append(filteredName if filteredName != '' else val_i)
    return filteredNames, del_logs


def get_ratio_by_range(ratio_ranges, price):

    """
    무료배송일때 Domeme수정시 필요하다 써야한다.
    :ratio_ranges [[0, 1000, 4], [1000, 2000, 3],,,[start, end, ratio]]
    :default_ratio 범위에 없는 price가 들어왔을 때 반환.
    :return 요율을 반환. 계속 수정되는 함수임.
    """
    for i in ratio_ranges:
        start, end = i[0], i[1]
        if price in range(start, end+1):
            return i[2]

    raise Exception('범위에 없는 수가 들어왔습니다!')


def get_img_mask(img, R, G, B):
    """

    :param img: ndarray. imread()하면 ndarray가 된다.
    :param R: 0~255
    :param G: 0~255
    :param B: 0~255
    :return:
    """
    assert isinstance(img, np.ndarray)
    assert isinstance(R, int)
    assert isinstance(G, int)
    assert isinstance(B, int)

    N = len(img)
    M = len(img[0])
    # print(f'N : {N}')
    # print(f'M : {M}')
    match=255 # 255 = 흰, 0 = 검정.
    notMatch=0
    mask = [[match if img[j][i][0] == R and img[j][i][1] == G and img[j][i][2] == B else notMatch for i in range(M) ] for j in range(N)] # 2차원 배열 만들기. 특이하게 col을 먼저 써야한다.

    mask = np.array(mask, dtype=np.uint8)
    assert isinstance(mask, np.ndarray)
    assert mask.dtype==np.uint8
    return mask


def paste_logo(logo, bg, xoffset, yoffset):
    """
    :param logo:삽입하고자 하는 로고 이미지 ndarray
    :param bg: 배경 ndarray
    :param xoffset: x 로고 삽입 위치
    :param yoffset: y 로고 삽입 위치
    :return: 수정된 파일 ndarray
    """
    assert isinstance(logo, np.ndarray)
    assert isinstance(bg, np.ndarray)
    assert isinstance(xoffset, int)
    assert isinstance(yoffset, int)
    #
    # logo = cv2.imread(logo)
    # bg = cv2.imread(bg)
    cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)  # open cv는 BGR로 나타낸다.
    cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    # 이미지는 5차원이다. 2차원 x,y좌표. 그 안에 3차원 RGB값.
    nrows, ncols, nchannels = logo.shape
    # print(f'img1. shape : {logo.shape}')

    bg_part = bg[xoffset:xoffset + nrows, yoffset:yoffset + ncols]  # x, y 좌표 먼저 정하고 그 다음 rgb값이 있다.

    mask = get_img_mask(logo, 255, 255, 255)  # 흰색 찾는다. 흰색=255. 로고가 있는 곳을 검정(0)인 마스크 이미지 생성

    roi_bg = cv2.bitwise_and(bg_part, bg_part, mask=mask)  # 로고있는 곳은 검정(0)으로 만듦..

    mask_inv = cv2.bitwise_not(mask) # 여기서 흰 테두리가 생긴다..
    bgremove_logo = cv2.bitwise_and(logo, logo, mask=mask_inv)  # 로고배경제거

    res = cv2.add(roi_bg, bgremove_logo)  # 로고 씌우기

    bg[xoffset:xoffset + nrows, yoffset:yoffset + ncols] = res

    assert isinstance(bg, np.ndarray)
    return bg


def piltocv2(pil_image):
    assert isinstance(pil_image, PIL.Image.Image)
    #
    # # open image using PIL
    # pil_image=PIL.Image.open("./learning_python.png")
    #
    # use numpy to convert the pil_image into a numpy array
    numpy_image=np.array(pil_image)

    # convert to a openCV2 image and convert from RGB to BGR format
    opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return opencv_image

def cv2topil(cv2_img):
    assert isinstance(cv2_img, np.ndarray)

    # convert from BGR to RGB
    color_coverted = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # convert from openCV2 to PIL
    pil_image = PIL.Image.fromarray(color_coverted)
    return pil_image

#
# def path_win_to_linux(path):
#     assert isinstance(path, str)
#
#     new = path.replace('\\', '/')
#     return new




