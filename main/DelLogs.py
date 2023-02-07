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










