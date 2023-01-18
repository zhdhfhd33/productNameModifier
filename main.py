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


class MyFileter():
    def __init__(self, df, parenthèses):
        """
        :param df:
        :param parenthèses: [[(,)], [{,}]]
        """
        self.df = df
        self.parenthèses = parenthèses

    #
    # def getParenthesis(self, productName):
    #     """
    #     :param productName: (도매매)기모 장갑~~
    #     :return: dict {'(' : [], ')':[]}
    #     """
    #     indicies = {}
    #     for i in self.parenthèses:
    #         regex = re.compile(f"\\{i[0]}")
    #         indicies[i[0]] = [i for i in re.finditer(regex, productName)]
    #         regex2 = re.compile(f'\\{i[1]}')
    #         indicies[i[1]] = [i for i in re.finditer(regex2, productName)]
    #
    #     return indicies

    # def removeParenthesisStr(self):
    #     productNames = df['상품명'].tolist()
    #     for i in range(len(productNames)):
    #         indicies = self.getParenthesis(productNames[i], self.parenthèses)
    #
    #         for j in range(len(indicies)):
    #             filteredStr = productNames[i][:indicies['(']].start() + productNames[i][indicies[')'].start()]
    #     return filteredStr
    #
    # def removeStartEndParenthesisStr(self):
    #     """
    #     괄호의 시작부터 끝을 삭제
    #     :return:
    #     """
    #     productNames = df['상품명'].tolist()
    #     filteredNames = []
    #     for i in range(len(productNames)):  # i=상품명인덱스
    #         indicies = self.getParenthesis(productNames[i])
    #         newStr = productNames[i]
    #
    #         for j in parentheses:
    #             if len(indicies[j[0]]) == 0 or len(indicies[j[1]]) == 0:  # j[0] = (, [,, {, j[1] = ), ],, }
    #                 continue
    #
    #             newStr = newStr[:indicies[j[0]][0].start()] + newStr[indicies[j[1]][
    #                                                                      0].start() + 1:]  # 이렇게 숫자로 하는 것 보다 클래스 만드는게 유리하다.
    #
    #         filteredNames.append(newStr)
    #     return filteredNames

    def removeChars(self, chars):
        """
        chars에 있는 문자를 지운다. 단순 remove임.
        :param chars: [/, \, =,,,]
        :return: [newName1, newName2,,,]
        """
        productNames = df['상품명'].tolist()
        filteredNames = []
        delLogs = []

        for i, val in enumerate(productNames):  # [상품1, 상품2, 상품3]
            filteredName = val
            for j in chars:  #
                regex = re.compile(f'{j}')
                indicies = [i for i in re.finditer(regex, filteredName)]  # 문자를 찾은 인덱스 정보
                for k in indicies:  # 특수문자가 있는 인덱스의 자리
                    startIdx = k.span()[0]
                    endIdx = k.span()[1]
                    delLogContent = filteredName[startIdx:endIdx]
                    delLogs.append(DelLog(i, delLogContent))

                    filteredName = filteredName[:startIdx] + filteredName[endIdx:]
            filteredNames.append(filteredName)
        return filteredNames, delLogs
    #
    # replaceChars를 이렇게 짜면 로그를 남길 수 없다.
    # def replaceChars(self, targetStrs, replaceStrs):
    #     """
    #     :param targetStrs: 바꿔지는 문자열  ['a', 'b', ,,]
    #     :param replaceStrs: 바꾸고자 하는 문자열 ['A, 'B',,,]
    #     :return:
    #     """
    #     productNames = df['상품명'].tolist()
    #     filteredNames = []
    #     delLogs = []
    #     for i in range(len(productNames)):
    #         productName = productNames[i]
    #         for j in range(len(targetStrs)):
    #             productName = productName.replace(targetStrs[j], replaceStrs[j])
    #             if productName.find(targetStrs[j]) != -1:
    #                 delLogs.append(DelLog(i, targetStrs[j]))
    #         filteredNames.append(productName)
    #     return filteredNames

    def replaceChars(self, targetStrs, repalceStrs):
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
                    filteredName = filteredName[:startIdx] + replacedStrs[j] +filteredName[endIdx:] # 단순삭제가 아니라 replace해야한다.
                    delLogContent = filteredName[startIdx:endIdx]
                    delLogs.append(DelLog(i, delLogContent))
            filteredNames.append(filteredName)
        return filteredNames, delLogs

    def removeDuplicatedSpace(self, productNames):
        # productNames = df['상품명'].tolist()
        trimedStr = []
        for i in productNames:
            newStr = re.sub(r'\s+', ' ', i)  # 이런 방법을 잘 기억해 두자!
            trimedStr.append(newStr)
        return trimedStr

    # class MatchInfo:
    #     def __init__(self):
    #         self.idx = None
    #         self.matches = []
    #
    #     def __str__(self):
    #         return f'idx : {self.idx} matches : {self.matches}'
    # #
    # def getMatchInfos(self, words):
    #     productNames = df['상품명'].tolist()
    #     matchInfos = []
    #     for i in range(len(productNames)):
    #         match = self.MatchInfo()  # 이너클래스에 직접적으로 접근할 수 없다.
    #         match.idx = i
    #
    #         for j in words:
    #             if productNames[i].find(j) != -1:  # 못찾으면 -1반환
    #                 match.matches.append(j)
    #         matchInfos.append(match)
    #     return matchInfos

    def removeReg(self, regStrs):
        """
        :param regStrs: [r's+' r'(0-9)+', ,,,,]
        :return: regStrs에 해당하는 부분을 찾아서 없앤다.
        """
        productNames = df['상품명'].tolist()
        filteredNames = []
        del_logs=[]
        for i, i_val in enumerate(productNames):  # [상품1, 상품2, 상품3]
            filteredName = i_val
            for j in regStrs:
                regex = re.compile(j)
                indicies = [i for i in re.finditer(regex, filteredName)]  # 문자를 찾은 인덱스 정보. 인덱스는 i에서 찾고
                for k in indicies:  # 반영은 filteredName에서 한다.
                    startIdx = k.span()[0]
                    endIdx = k.span()[1]
                    del_content = DelLog(i, filteredName[startIdx:endIdx])
                    filteredName = filteredName[:startIdx] + filteredName[endIdx:]
                    del_logs.append(DelLog(i, del_content))
            filteredNames.append(filteredName)
            filteredNames.append(filteredName)
        return filteredNames, del_logs



if __name__ == '__main__':
    # df 출력설정.
    pd.set_option('display.max_columns', None)  # 전체 열 보기
    pd.set_option('display.max_rows', None)  # 전체 행 보기

    df = pd.read_csv('C:/Users/minkun/Downloads/마이박스.csv', encoding='cp949')
    parentheses = [['(', ')'], ['[', ']'], ['{', '}']]  # 괄호 안을 전부 지우기 위해 이런게 필요했다.

    myFilter = MyFileter(df, parentheses)

    # 원본출력
    print('origin : ', df['상품명'].count())
    print(df['상품명'].head(10))
    print()
    print()

    # 문자 지우기
    removingStrs = ['후니케이스', '다번다', '뷰티컬'
        , '아이윙스', '피포페인팅', '하이셀', '에이브', '이거찜', 'PVC', '리빙114', '슬림스', '모던스', 'SNW', 'ABM도매콜', '애니포트', '헤어슈슈', '베이비캠프',
                    '가디언블루', '그린피앤에스', '템플러', '클리카', '유앤미', '저혈당', '레인보우', 'ABM', '도매콜', '성기', '템플러', '애니포트'
                    ]
    charFiltered, delLogs1 = myFilter.removeChars(removingStrs)
    myFilter.df['상품명'] = pd.Series(charFiltered)
    print(myFilter.df['상품명'].head(10))
    print('specialChars :', myFilter.df['상품명'].count())
    print()
    print()

    # 스페이스로 대체. 스페이스가 2개 되더라도 나중에 뒤에서 스페이스 여러개 처리하기 때문에 상관 x
    targetStrs = ['\/', '\(', '\)', '\[', '\]', '\{', '\}']  # regexp가 아니라서 이스케이프 안해도 된다. regexp일 때는 이스케이프 해야함.
    replacedStrs = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert len(targetStrs) == len(replacedStrs), f'{len(targetStrs)}=={len(replacedStrs)}'
    replacedStrs, delLogs2  = myFilter.replaceChars(targetStrs, replacedStrs)
    myFilter.df['상품명'] = pd.Series(replacedStrs)
    print('특수문자 -> 스페이스', myFilter.df['상품명'])
    print()
    print()

    # 정규표현식 삭제
    # re.sub를 사용할 떈 //g를 사용하면 안된다.
    regStrs = [
        r'[0-9a-zA-Z]+-[0-9a-zA-Z]+',  # DP-1234,
        r'[a-zA-Z]{1,2}[0-9]+',  # DB12 //잘못하면 USB2 이런것도 걸린다.
        r'^[0-9]+\.',  # 09. 발가락 보호대. 12. 허리보호대
        r'[0-9]{4,9}',  # 숫자4개 이상연속
    ]

    regFiltered, delLogs3 = myFilter.removeReg(regStrs)
    myFilter.df['상품명'] = pd.Series(regFiltered)
    print(myFilter.df['상품명'].head(10))
    print('regex 필터')
    print()
    print()

    # 들어있다면 row 자체를 삭제
    booleanFilter = myFilter.df['상품명'].str.contains('랜덤')  # '랜덤|싸다|최저가' 이렇게 |로 나열해주면된다.
    print('booleanFilter count : ', booleanFilter[booleanFilter == True].count())
    myFilter.df = myFilter.df[~booleanFilter]
    # print('after del contain row : ', myFilter.df.count())

    # 좌우 공백 삭제, strip
    stripList = myFilter.df['상품명'].tolist()
    for i in range(len(stripList)):
        stripList[i] = stripList[i].strip()
    # myFilter.df['상품명'] = pd.Series(stripList) # 수정한 것을 다시 대입할 수 없다.
    productNames = stripList

    # 띄어쓰기 두번 삭제
    duplicatedSpaceRemoved = myFilter.removeDuplicatedSpace(productNames)
    productNames = pd.Series(duplicatedSpaceRemoved)
    print('duplicatedSpaceRemoved : \n', productNames.head(10))
    print()
    print()

    resDf = myFilter.df.copy()
    resDf['상품명'] = productNames
    myFilter.df = resDf  # 억지로 넣음..

    # TODO : 키워드 랜덤섞기 해야할지도?



    # 최종출력
    cnt = 1
    fileName = 'resCsv' + str(cnt) + '.csv'
    while os.path.isfile(fileName):  # 여러번 실행시킬 수 있도록.
        cnt += 1
        fileName = 'resCsv' + str(cnt) + '.csv'
    resDf.to_csv(fileName, encoding='cp949')  # 엑셀로 열려면 cp949 해야한다!
    print(f'fileName : {fileName}')
    print(f'len : {len(productNames)}')
