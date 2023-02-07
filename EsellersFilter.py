import os.path

import pandas as pd
import re
import libs


class EsellersCombinationalOption():
    def __init__(self, names, add_price, cnt, expose, url='', manage_code='', volume = 0):
        """
        :param names:
        :param add_price:
        :param cnt:
        :param expose:

        아래 3개는 없어도 된다.
        :param url:
        :param manage_code: 없다면 ''
        :param volume: 롯데온에서만 사용용. 없다면 0대입.
       """
        self.names = names
        # **
        self.add_price = add_price
        self.cnt = cnt
        self.is_expose = expose

        self.url = url
        self.manage_code = manage_code
        self.volume = volume

    def __str__(self):
        return f'names : {self.names}, add_price : {self.add_price}, cnt : {self.cnt}, is_expose : {self.is_expose}, url : {self.url}, manage_code : {self.manage_code}, volumn : {self.volume}'



class EsellersFilter:
    def __init__(self, df_basic, df_extend, product_col_name, option_col_name, option_type_col_name):
        self.df_basic = df_basic
        self.df_extend = df_extend
        self.product_col_name = product_col_name
        self.option_col_name = option_col_name
        self.option_type_col_name =option_type_col_name

    # 기본정보, 확장정보는 같이 지워야한다. 같이 안해도 된다. 이셀러스에서 알아서 inner join함.
    def drop_row(self, idx):
        """
        inplace = True
        :param idx:
        :return:
        """
        self.df_basic.drop(inplace=True, index=idx, axis=0)
        self.df_extend.drop(inplace=True, index=idx, axis=0)

    def __parse_option(self, option_str):
        """
        조합형일 경우에만 사용.
        아직까지 독립형 한번도 못보긴 했다.
        :option_str : 상품선택*베이지**0*999*Y*https://cdn.ownerclan.com/rD0fHE4mN0V4nGhkVM1cyXkw7Qvn3BYb84g5FilqFVs/marketize/auto/as/v1.jpg
        :return :
        """
        arr = option_str.split('**')
        option_names = arr[0].split('*')
        others = arr[1].split('*')
        tmp_others = ['']*5 +[0]
        for i in range(len(others)):
            tmp_others[i] = others[i]
        es_option =  EsellersCombinationalOption(names = option_names, add_price=tmp_others[0], cnt = 1, is_expose=tmp_others[2],  url=tmp_others[3], manage_code=tmp_others[4], volume=tmp_others[5])
        return es_option

    def __parse_df_options(self):
        """
        옵션 파싱해서 Series 반환. 인덱스도 동일.
        리스트나 ndarr로 하면 안된다. 옵션이 아예없는 애들도 있기 때문에 인덱스로 join해야함.. df상태에서 다뤄야한다.
        :return:
        """
        option_types = self.df_basic[self.option_type_col_name]
        option_strs = self.df_basic[self.option_col_name]
        idx=[]
        parsed=[]
        for i in option_types.index: # range사용할 때는 .iloc사용해야함. 인덱스로 다루는게 편하다. 다른 컬럼에 접근할 때도 유용함.
            if option_types[i]=='조합형':
                parsed.append(self.__parse_option(option_strs[i]))
                idx.append(i)

        ser = pd.Series(parsed, index=idx)
        return ser















    def option_add_price(self):
        """
        옵션에 추가금있으면 지마켓, 옥션에는 등록 안된다.
        옵션 추가금을 가격으로 반영
        :return:
        """
        option_objs = self.__parse_df_options() # 리스트
        if



















    # def bool_indexing(self, arr):
    #     self.df_basic = self.df_basic[arr]
    #     self.df_extend = self.df_extend[arr]


# TODO : 일단은 엑셀로 진행
def set_price_by_ratio(series, blocks, ratios):
    """
    series
    blocks = [(500, 1000), (1001, 1500), (1501, 2000), (2000, 3000), (3001, 20000)]
    ratios = [4, 3, 3, 2, 1.6]
    """
    pass


if __name__ == '__main__':
    # ProductNameModifier.pdConfig()
    libs.pdConfig()
    # path = '2023-1-15-오너클랜/2023-1-15-오너클랜템플릿1-수정일1개월.xls'
    path = '/content/drive/MyDrive/Colab Notebooks/ProductNameModifier/2023-1-15-오너클랜/템플릿1 유료배송 수정일 1개월.xls'

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

    # -----------------------init------------------------------------------
    # print(ef.df_basic['상품명*'])
    # print(ef.df_basic['판매가*'])

    # 카테고리 값 없으면 제거.
    ef.df_basic.dropna(subset=[category_col_name], inplace=True)

    # 혹시모를 초기화. 원가 != 판매가인 상품도 있다.
    # ef.df_basic[price_col_name] = ef.df_basic['원가']

    # 500, 20000 사이의 가격만 남긴다.
    bool_idx = (500 <= df_basic[price_col_name]) & (df_basic[price_col_name] <= 20000)
    ef.df_basic = ef.df_basic[bool_idx]  # inplace = True
    # assert len(ef.df_basic)==len(ef.df_extend), '길이가 일치하지 않습니다'
    print(len(ef.df_basic[price_col_name]))

    # 가격, 이름으로 정렬. 옵션으로 뺄 수 있으면 뺀다. 이름은 같은 옵션은 묶을려구..
    first_ordering = price_col_name  # 판매가*
    second_ordering = ef.product_col_name  # 상품명*
    ef.df_basic.sort_values(by=[first_ordering, second_ordering], inplace=True)

    # 상품명 가공 전에 상세페이지에 원래 이름 한번 써준다. 상품명 가공 전에 이걸 먼저 돌려야한다. df에 넣어야 상수 컬럼이 만들어진다. series로 하면 row 1 밖에 안만들어 진다.
    # ef.df_basic['start'] = ("""<center><p align="center">
    #     <h1>안녕하세요 :) 넥스트레벨스토어(널리)를 찾아주셔서 감사합니다.</h1>""")
    # ef.df_basic['middle'] = ef.df_basic[ef.product_col_name].astype('str') # 처리 전의 상품명
    # ef.df_basic['end'] = pd.Series("""</p></center>""")

    start = ("""<center><p align="center">
         <h2>안녕하세요 :)</h2> <h2>넥스트레벨스토어(널리)를 찾아주셔서 감사합니다.</h2>""")
    middle = ef.df_basic[ef.product_col_name].astype('str')  # 처리 전의 상품명
    end = """</p></center>"""

    # ef.df_basic[detail_col_name] = ef.df_basic['start'].astype('str') + ef.df_basic['middle'].astype('str') + ef.df_basic[detail_col_name].astype('str')  + ef.df_basic['end'].astype('str')
    ef.df_basic[detail_col_name] = start + middle + end + ef.df_basic[detail_col_name]
    # ef.df_basic.drop(['start', 'middle', 'end'], inplace=True, axis=1) # 임의로 만든 컬럼 삭제

    # ----------------------------- 출력 --------------------------------------------
    file_path = '/content/drive/MyDrive/Colab Notebooks/ProductNameModifier/resources/EsellersResXls/res.xls'  # xls로 뽑아야 이셀러스에 넣을 수 있다.

    with pd.ExcelWriter(file_path) as writer:
        ef.df_basic.to_excel(writer, sheet_name='기본정보', index=False)
        ef.df_extend.to_excel(writer, sheet_name='확장정보', index=False)
    print(f'file_path : {file_path}')

    #
    # 이건 원본상품에서 손대지 않는다.
    # # TODO : 판매가 설정.
    # blocks = [(500, 1000), (1001, 1500), (1501, 2000), (2000, 3000), (3001, 20000)]
    # ratios = [4, 3, 3, 2, 1.6]
    # before=ef.df_basic[price_col_name].head(20).tolist()
    # # set_price_by_ratio(ef.df_basic['판매가'], blocks=blocks, ratios=ratios)
    # after = ef.df_basic[price_col_name].head(20).tolist()











