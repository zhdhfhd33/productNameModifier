import os.path

import pandas as pd
import re


class DelLog():
    def __init__(self, idx, content, regexp):
        self.regexp=regexp
        self.content = content
        self.idx = idx

    def __str__(self):
        return f'regexp : {self.regexp}    content : {self.content}    idx : {self.idx}    xlsIdx : {self.getXlsIdx()}'

    def getXlsIdx(self):
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


    def replaceRegexpStrs(self, targetStrs, repalceStrs):
        """
        코어함수
        키워드를 제거하거나 변경할 때 사용한다.
        :param targetStrs: 바꾸고자 하는 문자열
        :param repalceStrs: 이 문자열로 바꾸자
        :return: filteredNames, del_logs
        """
        productNames = df['상품명'].tolist()
        filteredNames = []
        delLogs = []
        for i, val_i in enumerate(productNames):  # [상품1, 상품2, 상품3]
            tmp_val_i = val_i
            filteredName = ''
            for j, val_j in enumerate(targetStrs):
                regex = re.compile(f'{val_j}')
                indicies = [_ for _ in re.finditer(regex, tmp_val_i)]  # 문자를 찾은 인덱스 정보
                LEN = len(indicies)
                for k in range(LEN):  # 특수문자가 있는 인덱스의 자리

                    #잘라내서 붙일 인덱스
                    startIdx = 0 if k == 0 else indicies[k - 1].span()[1] + 1
                    endIdx = indicies[k].span()[0]
                    filteredName += val_i[startIdx:endIdx] + repalceStrs[j] # 단순삭제가 아니라 replace해야한다.
                    tmp_val_i = filteredName

                    #잘라내서 없앨 인덱스
                    del_start_idx = indicies[k].span()[0]
                    del_end_idx = indicies[k].span()[1]
                    delLogContent = val_i[del_start_idx:del_end_idx]
                    delLogs.append(DelLog(i, delLogContent, val_j))
                # 마지막에 처리 한번 더 해야한다.
                if LEN > 0:
                    startIdx = indicies[LEN - 1].span()[1]
                    filteredName += val_i[startIdx:]
            filteredNames.append(filteredName if filteredName != '' else val_i)
        return filteredNames, delLogs

    def removeChars(self, chars):
        """
        특수문자 제거에 사용한다.
        chars에 있는 문자를 지운다. 단순 remove임.
        :param chars: [/, \, =,,,]
        :return: [newName1, newName2,,,]
        """
        replaceChars=['']*len(chars)
        filteredNames, delLogs = self.replaceRegexpStrs(chars, replaceChars)

        return filteredNames, delLogs

    def removeDuplicatedSpace(self, productNames):
        # productNames = df['상품명'].tolist()
        trimedStr = []
        for i in productNames:
            newStr = re.sub(r'\s+', ' ', i)  # 이런 방법을 잘 기억해 두자!
            trimedStr.append(newStr)
        return trimedStr

    def removeReg(self, regStrs):
        """
        :param regStrs: [r's+' r'(0-9)+', ,,,,]
        :return: regStrs에 해당하는 부분을 찾아서 없앤다.
        """
        tmp=['']*len(regStrs)

        filteredNames, del_logs, = self.replaceRegexpStrs(regStrs, tmp)
        return filteredNames, del_logs

def make_log_df(del_logs):
    del_log1_df = pd.DataFrame({'정규표현식': [i.regexp for i in del_logs], '삭제된 문자열': [i.content for i in del_logs],
                                '엑셀 idx': [i.getXlsIdx() for i in del_logs]})
    return del_log1_df

if __name__ == '__main__':
    # df 출력설정.
    pd.set_option('display.max_columns', None)  # 전체 열 보기
    pd.set_option('display.max_rows', None)  # 전체 행 보기

    df = pd.read_excel('C:/Users/minkun/Downloads/마이박스.xls')
    df.drop(inplace=True, index=0, axis=0) # 행삭제. 행을 삭제해도 인덱스는 그대로 남아있다. 재정렬 안된다.
    # df = df.iloc[1:, :]

    parentheses = [['(', ')'], ['[', ']'], ['{', '}']]  # 괄호 안을 전부 지우기 위해 이런게 필요했다.

    myFilter = MyFileter(df, parentheses)

    # 원본출력
    print('origin : ', df['상품명'].count())
    print(df['상품명'].head(10))
    print(df['상품명'].count())
    print()
    print()

    # 키워드 지우기
    removingStrs = ['후니케이스', '다번다', '뷰티컬'
        , '아이윙스', '피포페인팅', '하이셀', '에이브', '이거찜', 'PVC', '리빙114', '슬림스', '모던스', 'SNW', 'ABM도매콜', '애니포트', '헤어슈슈', '베이비캠프',
                    '가디언블루', '그린피앤에스', '템플러', '클리카', '유앤미', '저혈당', '레인보우', 'ABM', '도매콜', '성기', '애니포트', '정확도'
                    ]
    before_len=len(removingStrs)
    removingStrs_set=set(removingStrs)
    after_len=len(removingStrs_set)
    removingStrs = list(removingStrs_set)
    print('중복되는 키워드 개수 : ', before_len-after_len)
    print('상품명 카운트', df['상품명'].count())
    charFiltered, del_logs1 = myFilter.removeChars(removingStrs)
    charFiltered.insert(0, 0) # 앞에 더미값 하나 추가해줘야 올바르게 동작함. 아니면 시리즈[0]에 해당하는 row가 잘린다...
    tmpSeries= pd.Series(charFiltered)
    print(tmpSeries)
    myFilter.df['상품명'] = tmpSeries # 데이터 프레임에 추가될 때는 인덱스를 기준으로 추가된다. 앞에서 잘랐기 때문에 인덱스가 1부터 시작된다. 0부터 있어서 문제가 되었던 것이다.
    print('키워드 지우기')
    print(myFilter.df['상품명'].head(10))
    print(myFilter.df['상품명'].count())
    print()
    print()


    #특수문자 제거
    # 스페이스로 대체. 스페이스가 2개 되더라도 나중에 뒤에서 스페이스 여러개 처리하기 때문에 상관 x
    targetStrs = ['\/', '\(', '\)', '\[', '\]', '\{', '\}']  # regexp가 아니라서 이스케이프 안해도 된다. regexp일 때는 이스케이프 해야함.
    replacedStrs = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert len(targetStrs) == len(replacedStrs), f'{len(targetStrs)}=={len(replacedStrs)}'
    replacedStrs, del_logs2  = myFilter.replaceRegexpStrs(targetStrs, replacedStrs)
    replacedStrs.insert(0,0)
    myFilter.df['상품명'] = pd.Series(replacedStrs)
    print('특수문자 -> 스페이스')
    print(df['상품명'].count())
    print(myFilter.df['상품명'].head(10))
    print()

    # 정규표현식 삭제
    # re.sub를 사용할 떈 //g를 사용하면 안된다.
    targetStrs = [
        r'[0-9a-zA-Z]+-[0-9a-zA-Z]+',  # DP-1234,
        r'[a-zA-Z]{1,2}[0-9]+',  # DB12 //잘못하면 USB2 이런것도 걸린다.
        r'^[0-9]+\.',  # 09. 발가락 보호대. 12. 허리보호대
        r'[0-9]{4,9}',  # 숫자4개 이상연속
    ]

    regFiltered, del_logs3 = myFilter.removeReg(targetStrs)
    regFiltered.insert(0,0)
    myFilter.df['상품명'] = pd.Series(regFiltered)
    print('regex 필터')
    print(myFilter.df['상품명'].head(10))
    print()
    print()

    # 들어있다면 row 자체를 삭제
    booleanFilter = myFilter.df['상품명'].str.contains('랜덤')  # '랜덤|싸다|최저가' 이렇게 |로 나열해주면된다.
    print('booleanFilter count : ', myFilter.df[booleanFilter == True].count())
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
    #TODO csv가 아니라 엑셀로 만들기
    cnt = 1
    dir_name='resources'
    dir_name1='resXls'
    fileName = dir_name+ '/' + dir_name1+'/'+'resCsv' + str(cnt) + '.csv'

    while os.path.isfile(fileName):  # 여러번 실행시킬 수 있도록.
        cnt += 1
        fileName = dir_name +'/' + dir_name1 +'/'+'resCsv' + str(cnt) + '.csv'
    resDf.to_csv(fileName, encoding='cp949')  # 엑셀로 열려면 cp949 해야한다!
    print(f'fileName : {fileName}')
    print(f'len : {len(productNames)}')

    #del_log 파일 만들기
    #TODO : 폴더 경로 정리.

    del_log_dir='resources/del_logs.xlsx'

    with pd.ExcelWriter(del_log_dir) as writer:
        del_log1_df = make_log_df(del_logs1)# 키워드

        del_log2_df = make_log_df(del_logs2)# 특수문자

        del_log3_df = make_log_df(del_logs3)# 정규표현식

        del_log1_df.to_excel(writer, sheet_name='키워드삭제')
        del_log2_df.to_excel(writer, sheet_name='특수문자 삭제')
        del_log3_df.to_excel(writer, sheet_name='정규표현식 삭제')


    # del_log1_df.to_csv('del_log1.csv', encoding='cp949')
    #
    # del_log2_df.to_csv('del_log2.csv', encoding='cp949')
    #
    # del_log3_df.to_csv('del_log3.csv', encoding='cp949')









