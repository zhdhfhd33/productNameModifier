import sys, os

import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main.EsellersFilter import *
from main.core import *
import sys
from PIL import Image


def init():
    pdConfig()
    path = "resources/오너클랜 이셀러스.xls"  # test폴더 안에 있기 때문에 test는 빼야한다.

    df_basic = pd.read_excel(path, sheet_name='기본정보')
    df_extend = pd.read_excel(path, sheet_name='확장정보')
    price_col_name = '판매가*'
    detail_col_name = '상세설명*'
    category_col_name = '카테고리 번호*'
    product_col_name = '상품명*'

    ef = EsellersFilter(df_basic, df_extend, product_col_name)
    ef.drop_row(0)  # 설명삭제

    # 자동 타입추론. 편하다.
    ef.df_basic = ef.df_basic.infer_objects()
    return ef


# def write(path, df):
#     with pd.ExcelWriter(path) as writer:
#         df.to_excel(writer, sheet_name='기본정보', index=False)


def test_option_add_price_filter(): # TODO : assert넣기
    ef = init()
    # ef1=ef.copy()
    # ef.option_add_price_filter()
    # print(ef.df_basic[ef.option_col_name]) #  테스트에서 출력을 보고 싶으면 옵션을 추가해야한다.
    with pd.ExcelWriter('test.xlsx') as writer:
        ef.df_basic.to_excel(writer, index=False)

def test_option50_over_filter(): # TODO : assert넣기
    ef = init()
    d=ef.option50_over_filter()
    for i in d:
        print(i)

def test_img_down_all():
    ef=init()
    ef.img_down_all('resources/imgs/img_down_test/') # 마지막에 /까지 붙여야한다. 폴더가 실제로 존재해야함.


def test_img_size():
    li=os.listdir('resources/imgs/img_down_test')
    size_li=[]

    for i in li:
        img = Image.open('resources/imgs/img_down_test/'+i)
        size_li.append(img.size)

    for i in size_li:
        print(i) # 거의 이미지는 640*640이거나 1000*1000이다.

    x =  [i[0] for i in size_li]
    y =  [i[1] for i in size_li]
    print(f'min x : {min(x)}')
    print(f'min y : {min(y)}')

def test_img_filter():

    ef=init()
    ef.img_filter('resources/imgs/img_down_test/', 'resources/imgs/after_processing/', 0.02, 0.1) # 0.02가 딱 맞다.






# ----------------------------이렇게 검증할 수 있다.
# test_option50_over_filter()
# test_option_add_price_filter()
# test_img_down_all()
# test_img_size()
test_img_filter()










