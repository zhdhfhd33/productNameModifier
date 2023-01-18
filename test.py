import os.path

import pandas as pd
import re
import csv



class DelLog():
    def __init__(self, idx, content):
        self.content = content
        self.idx = idx

    def __str__(self):
        return f'content : {self.content}    idx : {self.idx}    xlsxIdx : {self.getXlsxIdx()}'

    def getXlsxIdx(self):
        return self.idx + 2

def replaceChars(self, targetStrs, repalceStrs):
    pd.set_option('display.max_columns', None)  # 전체 열 보기
    pd.set_option('display.max_rows', None)  # 전체 행 보기

    df = pd.read_csv('C:/Users/minkun/Downloads/마이박스.csv', encoding='cp949')

    productNames = df['상품명'].tolist()
    filteredNames = []
    delLogs = []

    for i, val_i in enumerate(productNames):  # [상품1, 상품2, 상품3]
        filteredName = val_i
        for j, val_j in enumerate(targetStrs):
            regex = re.compile(f'{val_j}')
            indicies = [i for i in re.finditer(regex, filteredName)]  # 문자를 찾은 인덱스 정보
            for k in indicies:  # 특수문자가 있는 인덱스의 자리
                startIdx = k.span()[0]
                endIdx = k.span()[1]
                filteredName = filteredName[:startIdx] + repalceStrs[j] + filteredName[
                                                                           endIdx:]  # 단순삭제가 아니라 replace해야한다.
                delLogContent = filteredName[startIdx:endIdx]
                delLogs.append(DelLog(i, delLogContent))
        filteredNames.append(filteredName)
    return filteredNames, delLogs

if
