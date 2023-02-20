import math

import pandas as pd
from core import *
from ProductNameModifier import *


class DomemeModifier():
    def __init__(self, df):
        self.df = df

    def all_list_to_upload_form(self, is_coupang=False):
        """
        도매매에서 '전송리스트다운' 버튼으로 받은 xlsx파일을 엑셀 업로드 할 수 있게 형식을 바꿔 df를 반환하는 함수
        :return: 업로드 형식에 맞는 df
        """
        cols = ['도매매 상품번호', '상품명']
        res_df = self.df[cols].copy()
        img_col_name = '대표이미지'  # ''넣으면 된다.

        # 요율 제대로 넣어야함.
        price_ratio = '판매가요율'

        # 다 0넣으면 된다.
        option_ratio = '옵션가요율'
        market_comission = '수수료(%)'
        sale_ratio = '할인율'
        abs_add_price = '추가금액(+)'
        abs_sale_price = '할인금액(-)'

        #
        before_price = '공급가격'
        after_price = '판매가격'
        zero_cols = [option_ratio, market_comission
            , sale_ratio, abs_add_price, abs_sale_price]

        res_df.loc[:, img_col_name] = ''
        if is_coupang:
            ratio_ranges=[[0,1000, 4], [1000, 2000, 3], [2000, 3000, 2], [3000, INT_MAX, 1.6]]
            res_df[price_ratio] = self.df[before_price].apply(lambda x : get_ratio_by_range(ratio_ranges, x)) # apply() 시리즈 반환.

        else:
            res_df[price_ratio] = round(self.df[after_price] / self.df[before_price], 3)  # 요율계산. ser반환. 소숫점 3자리 까지만
        for i in zero_cols:
            res_df.loc[:, i] = 0
        return res_df

#-----------------------------ProductNameModifier까지 완료-------------------------------
pdConfig()
path = "C:/Users/minkun/Downloads/쿠팡_전송리스트_20230210102650.xls"
df = pd.read_excel(path)
keyword_df=pd.read_excel('resources/상품명가공 키워드지우기 리스트.xlsx')
keyword_df['변경 후'].fillna(' ', inplace=True)  # 엑셀에서
keyword_df = keyword_df.astype({'변경 전': 'string', '변경 후': 'string'})

dmm = DomemeModifier(df)
res_df = dmm.all_list_to_upload_form(is_coupang=True)

product_col_name = '상품명'
name_mod = ProductNameModifier(res_df, product_col_name=product_col_name, keyword_df=keyword_df)
name_mod.process_coupang()

print(res_df.head(10))
with pd.ExcelWriter('test.xlsx') as wr:
    name_mod.df.to_excel(wr, index=False)

