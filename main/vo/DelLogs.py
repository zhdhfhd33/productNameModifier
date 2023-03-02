import pandas as pd

class DelLogs():
    def __init__(self):
        self.absolute_brand_log =None
        self.keyword_log =None
        self.regexp_log = None
        self.special_char_log =None
        self.coupang_brand_filter_log = None

    def absolute_to_df(self):
        absolute_df={'정규표현식' : [i.regexp for i in self.absolute_brand_log],
                     '삭제된 문자열':[i.content for i in self.absolute_brand_log],
                     '엑셀 idx' : [i.getXlsIdx() for i in self.absolute_brand_log]}
        return pd.DataFrame(absolute_df)

    def keyword_to_df(self):
        keyword_df = {'키워드': [i.regexp for i in self.keyword_log],
                       '삭제된 문자열': [i.content for i in self.keyword_log],
                       '엑셀 idx': [i.getXlsIdx() for i in self.keyword_log]}
        return pd.DataFrame(keyword_df)

    def regexp_to_df(self):
        regexp_df = {'정규표현식': [i.regexp for i in self.regexp_log],
                      '삭제된 문자열': [i.content for i in self.regexp_log],
                      '엑셀 idx': [i.getXlsIdx() for i in self.regexp_log]}
        return pd.DataFrame(regexp_df)
    def special_char_to_df(self):
        special_char_df = {'제거하는 특수문자': [i.regexp for i in self.special_char_log],
                       '삭제된 특수문자': [i.content for i in self.special_char_log],
                       '엑셀 idx': [i.getXlsIdx() for i in self.special_char_log]}
        return pd.DataFrame(special_char_df)

    def coupang_brand_to_df(self):
        coupang_brand_df = {'정규표현식': [i.regexp for i in self.coupang_brand_filter_log],
                       '삭제된 문자열': [i.content for i in self.coupang_brand_filter_log],
                       '엑셀 idx': [i.getXlsIdx() for i in self.coupang_brand_filter_log]}
        return pd.DataFrame(coupang_brand_df)

    def to_xlsx(self, path):
        del_log1_df = self.absolute_to_df()  # 첨에 나오는 []는 무조건 브랜드
        del_log2_df = self.keyword_to_df()  # 키워드 삭제
        del_log3_df = self.regexp_to_df()  # 정규표현식
        del_log4_df = self.special_char_to_df()  # 특수문자 제거
        del_log5_df = self.coupang_brand_to_df()  # 쿠팡 브랜드. 호환.
        with pd.ExcelWriter(path) as writer:
            del_log1_df.to_excel(writer, sheet_name='처음에 나오는 대활호 삭제', index=False)
            del_log2_df.to_excel(writer, sheet_name='키워드 삭제', index=False)
            del_log3_df.to_excel(writer, sheet_name='정규표현식 삭제', index=False)
            del_log4_df.to_excel(writer, sheet_name='특수문자 삭제', index=False)
            del_log5_df.to_excel(writer, sheet_name='브랜드 호환', index=False)
        return path








