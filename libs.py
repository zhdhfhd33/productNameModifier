
# 전역 함수
import pandas as pd
import re
# def make_log_df(del_logs):
#     del_log1_df = pd.DataFrame({'정규표현식': [i.regexp for i in del_logs], '삭제된 문자열': [i.content for i in del_logs],
#                                 '엑셀 idx': [i.getXlsIdx() for i in del_logs]})
#     return del_log1_df


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







