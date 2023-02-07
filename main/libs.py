
# 전역 함수
import pandas as pd
import re
from main.DelLog import *

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





