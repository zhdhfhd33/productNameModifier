import ProductNameModifier
import os.path

import pandas as pd
import re


class EsellersFilter:
    def __init__(self, df_basic, df_extend):
        self.df_basic=df_basic
        self.df_extend=df_extend

    #기본정보, 확장정보는 같이 지워야한다.
    def drop_row(self, idx):
        """
        inplace = True
        :param idx:
        :return:
        """
        self.df_basic.drop(inplace=True, index = idx, axis=0)
        self.df_extend.drop(inplace=True, index = idx, axis=0)



if __name__ == '__main__':
    ProductNameModifier.pdConfig()
    path = 'C:\\Users\\minkun\\Downloads\\2023-1-15-오너클랜\\2023-1-15-오너클랜템플릿1-수정일1개월.xls'

    df_basic=pd.read_excel(path, sheet_name='기본정보')
    df_extend=pd.read_excel(path, sheet_name='확장정보')


    ef = EsellersFilter(df_basic, df_extend)
    ef.drop_row(1)
    print(ef.df_basic['상품명*'])





