import pandas as pd

from main.EsellersFilter import *
from main.libs import *
import sys


def init():
    pdConfig()
    path = "resource/오너클랜 이셀러스.xls"  # test폴더 안에 있기 때문에 test는 빼야한다.

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


def test_option_add_price_filter():
    ef = init()
    ef.option_add_price_filter()
    # print(ef.df_basic[ef.option_col_name]) #  테스트에서 출력을 보고 싶으면 옵션을 추가해야한다.
    with pd.ExcelWriter('test.xlsx') as writer:
        ef.df_basic.to_excel(writer, index=False)

test_option_add_price_filter()
