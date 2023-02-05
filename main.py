import os.path

import pandas as pd
import re
import libs
from ReplacePair import ReplacePair
import DelLog
from ProductNameModifier import ProductNameModifier



if __name__ == '__main__':
    # pd config
    libs.pdConfig()
    path = "resources/aa/쿠팡가품.xlsx"
    keyword_path = 'resources/상품명가공 키워드지우기 리스트.xlsx'

    # 읽기
    df = pd.read_excel(path)
    keyword_df = pd.read_excel(keyword_path)  # 키워드 삭제는 엑셀로 관리한다.

    # df 전처리
    df.drop(inplace=True, index=0, axis=0)  # 행삭제. 행을 삭제해도 인덱스는 그대로 남아있다. 재정렬 안된다.
    # df.drop(inplace=True, index=1, axis=0)  # 필터행 삭제
    keyword_df['변경 후'].fillna(' ', inplace=True)  # 엑셀에서

    keyword_df = keyword_df.astype({'변경 전': 'string', '변경 후': 'string'})

    # parentheses = [['(', ')'], ['[', ']'], ['{', '}']]  # 괄호 안을 전부 지우기 위해 이런게 필요했다.

    product_col_name = '상품명'
    name_modifier = ProductNameModifier(df=df, product_col_name=product_col_name, keyword_df=keyword_df)

    # ----------------------------init-----------------------------
    """
    process() or process_coupang() 실행시키면 된다.
    """
    # del_logs=myFilter.process()

    del_logs = name_modifier.process_coupang()

    # --------------------------- 최종출력-----------------------------
    # absolute_brand_log = del_logs.absolute_brand_log
    # keyword_log = del_logs.keyword_log
    # regexp_log = del_logs.regexp_log
    # special_char_log = del_logs.special_char_log
    # coupang_brand_filter_log = del_logs.coupang_brand_filter_log

    file_name , extension = libs.get_file_name(path, sep='/')
    extension='xlsx'
    cnt = 1
    dir_name = 'resources'
    dir_name1 = 'resXls'
    file_path = dir_name + '/' + dir_name1 + '/' + file_name + str(cnt) +'.'+extension

    while os.path.isfile(file_path):  # 여러번 실행시킬 수 있도록.
        cnt += 1
        file_path = dir_name + '/' + dir_name1 + '/' + file_name + str(cnt)+'.' + extension

    with pd.ExcelWriter(file_path) as writer:
        name_modifier.df.to_excel(writer, sheet_name='기본정보', index=False)

    print(f'fileName : {file_path}')
    # print(f'len : {len(productNames)}')

    del_log_dir = dir_name +'/' +'del_log_' +file_name+'.'+extension

    with pd.ExcelWriter(del_log_dir) as writer:
        del_log1_df = del_logs.absolute_to_df() # 첨에 나오는 []는 무조건 브랜드

        del_log2_df = del_logs.keyword_to_df() # 키워드 삭제

        del_log3_df = del_logs.regexp_to_df()  # 정규표현식

        del_log4_df = del_logs.special_char_to_df()  # 특수문자 제거
        del_log5_df = del_logs.coupang_brand_to_df() # 쿠팡 브랜드. 호환.


        del_log1_df.to_excel(writer, sheet_name='처음에 나오는 대활호 삭제', index=False)
        del_log2_df.to_excel(writer, sheet_name='키워드 삭제', index=False)
        del_log3_df.to_excel(writer, sheet_name='정규표현식 삭제', index=False)
        del_log4_df.to_excel(writer, sheet_name='특수문자 삭제', index=False)
        del_log5_df.to_excel(writer, sheet_name='브랜드 호환', index=False)
