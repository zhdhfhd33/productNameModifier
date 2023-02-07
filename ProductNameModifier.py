import os.path

import pandas as pd
import re
import libs
from ReplacePair import ReplacePair
from DelLog import DelLog

from DelLogs import DelLogs



class ProductNameModifier():
    def __init__(self, df, product_col_name, keyword_df):
        """
        df = param df:
        product_col_name = ex) '상품명' or '상품명*'
        """
        self.df = df
        self.product_col_name = product_col_name
        self.keyword_df = keyword_df
        # self.del_logs=[] process, process_coupang 둘 다 호출할 수 있으니까 멤버로 두면 안된다.

    def __replaceRegexpStrs(self, targetStrs, replaceStrs):
        """
        코어함수 private
        :param targetStrs: 바꾸고자 하는 문자열
        :param repalceStrs: 이 문자열로 바꾸자
        :return: filteredNames, del_logs
        """
        productNames = self.df[self.product_col_name].tolist()
        filteredNames = []
        del_logs = []
        for i, val_i in enumerate(productNames):  # [상품1, 상품2, 상품3]
            filteredName = val_i
            for j, val_j in enumerate(targetStrs):  # val_j = 정규표현식
                regex = re.compile(f'{val_j}')
                indicies = [_ for _ in re.finditer(regex, filteredName)]  # 문자를 찾은 인덱스 정보
                LEN = len(indicies)
                for k in range(LEN - 1, -1, -1):  # 특수문자가 있는 인덱스의 자리. 뒤에서 부터 삭제. 영향 안받는다. 0까지 하고 싶으면 -1로 설정해야한다.
                    startIdx = indicies[k].span()[0]
                    endIdx = indicies[k].span()[1]
                    del_content = filteredName[startIdx:endIdx]
                    filteredName = filteredName[:startIdx] + replaceStrs[j] + filteredName[endIdx:]
                    del_logs.append(DelLog(i, del_content, val_j))

            filteredNames.append(filteredName if filteredName != '' else val_i)
        return filteredNames, del_logs


    def remove_keywords(self, keywords, replaces):
        """
        키워드 제거
        chars에 있는 문자를 지운다. 단순 remove임.
        :param targets: [] 찾는 키워드
        :param replaces: [] 바꾸는 키워드

        df를 받는 것 보다는 계속 리스트를 인자로 받는 것이 일관성 있다. 일관성이 코딩에 중요하다!
        :return: [newName1, newName2,,,]
        """

        # 제대로 동작하기 위해서는 글자수가 긴 것 부터 해야한다.
        keywords.sort(key=lambda x: len(x))
        keywords = keywords[::-1]

        # replacekeywords = [''] * len(keywords)
        filteredNames, delLogs = self.__replaceRegexpStrs(keywords, replaces)

        # 대입
        self.df[self.product_col_name] = filteredNames
        return filteredNames, delLogs

    def remove_special_chars(self, replace_pairs):
        """
        특수문자 제거
        :replace_pairs = ReplacePair 객체 리스트
        """
        target_strs = []
        replace_strs = []
        for i in replace_pairs:
            target_strs.append(i.target)
            replace_strs.append(i.replace)
        filtered_names, del_logs = self.__replaceRegexpStrs(target_strs, replace_strs)

        # 대입
        self.df[self.product_col_name] = filtered_names
        return filtered_names, del_logs

    def removeDuplicatedSpace(self, productNames):
        """
        스페이스 2개 제거
        :param productNames:
        :return:
        """
        # productNames = df['상품명'].tolist()
        trimedStr = []
        for i in productNames:
            newStr = re.sub(r'\s+', ' ', i)  # 이런 방법을 잘 기억해 두자!
            trimedStr.append(newStr)
        return trimedStr

    def removeReg(self, regStrs):
        """
        정규표현식으로 제거
        :param regStrs: [r's+' r'(0-9)+', ,,,,]
        :return: regStrs에 해당하는 부분을 찾아서 없앤다.
        """
        tmp = [''] * len(regStrs)

        filteredNames, del_logs, = self.__replaceRegexpStrs(regStrs, tmp)

        # 대입
        self.df[self.product_col_name] = filteredNames
        return filteredNames, del_logs

    def brandFilter(self, replace_pairs):
        """
        :param regStrs: ['갤럭시', '갤럭시 워치', '애플',,,]
        :param tmp: ['갤럭시 호환', '갤럭시 워치 호환', '애플 호환',,,]
        :return:
        """
        target_strs = []
        replace_strs = []
        for i_val in replace_pairs:
            target_strs.append(i_val.target)
            replace_strs.append(i_val.replace)
        filtered_names, del_logs = self.__replaceRegexpStrs(target_strs, replace_strs)


        # 호환 여러번 들어가면 젤 뒤의 호환만 남긴다.
        # 마지막에 '호환' 하나는 놔두고 지워야하기 때문에 새로 구현할 수 밖에 없었다.
        # 'z플립4 호환' 이렇게 하고 싶었는데 z플립 호환 4 이렇게 될 것이다.
        filtered_names2=[]
        del_logs2=[]
        regex = re.compile(r'호환')
        for i, i_val in enumerate(filtered_names):
            indicies = [_ for _ in re.finditer(regex, i_val)]
            list_i = list(i_val) # str to list
            if len(indicies) > 1: # 호환이 여러 개 일때
                for j in range(len(indicies)-2, -1, -1): # 거꾸로 해야 del 가능. 마지막 하나는 남겨둬야하기 때문에 -2.
                    start_idx = indicies[j].span()[0]
                    end_idx = indicies[j].span()[1]
                    del_logs2.append(DelLog(i, list_i[start_idx:end_idx], '제거'))
                    del list_i[start_idx:end_idx]
            filtered_names2.append(''.join(list_i))
        self.df[self.product_col_name] = filtered_names2 # 대입
        sum_del_logs = del_logs+del_logs2 # del_log 합치기
        return filtered_names, sum_del_logs


    def contain_row_drop(self, keywords):
        """
        :keywords = regexp형식. '랜덤|새총|새 총|섹시|sexy'
        :return = 삭제된 cnt, 삭제 후 row cnt

        """
        booleanFilter = self.df[self.product_col_name].str.contains(keywords)  # 정규표현식에서 '랜덤|싸다|최저가' 이렇게 |로 나열해주면된다.
        del_cnt = self.df[booleanFilter == True].count()
        self.df = self.df[~booleanFilter]
        row_cnt = self.df[self.product_col_name].count()

        return del_cnt, row_cnt

    def get_name_similarity(self, func, k):
        """
        func : 함수. 매개변수 2개. return 이름의 유사도를 측정하는 방법.
        k : k%로 유사도가 k%를 넘으면 저장해서 보여준다. 이후는 사람이 비교함. ex) k=50
        {원본 : [비슷한 상품명]}을 만들어서 df로 뽑으면 컬럼이 상품명이 된다.
        버블소트 방식 사용
        첨에는 모든 데이터에 대해 simple_minlen_name_similarity가 어떻게 나오는지 알아야한다.
        """
        nd = self.df.to_numpy()  # n^2 이라서 ndarray로함.
        res = {}

        LEN = len(self.nd)
        for i in range(LEN):
            for j in range(i + 1, LEN):
                sim = libs.simple_minlen_name_similarity(nd[i], nd[j]) # libs에 있는 함수 사용
                if sim >= k:
                    if nd[i] in res:  # 자동으로 키를 준다.
                        res[nd[i]].append(nd[j])
                    else:
                        res[nd[i]] = []
                        res[nd[i]].append(nd[j])
        return res


    def remove_duplicated(self):
        """
        상품명이 완전히 같으면 지우기
        :return:
        """
        self.df.drop_duplicates([self.product_col_name], inplace=True, keep='first')



    def __process1(self):
        """
        private 함수
        : return [del_logs1, del_logs2, del_logs3]
        """

        del_logs = DelLogs()

        # 원본출력
        print('origin : ', self.df[self.product_col_name].count())
        print(self.df[self.product_col_name].head(10))
        print(self.df[self.product_col_name].count())
        print()
        print()

        # 들어있다면 row 자체를 삭제. 젤 먼저 해야한다.
        row_drop_keyword = '랜덤|렌덤|새총|새 총|섹시|sexy|칼 |나이프|리얼돌|토르소|티팬티|티펜티|해외|음경'
        del_cnt, row_cnt = self.contain_row_drop(row_drop_keyword)
        print('booleanFilter count : ', del_cnt)
        print('row 삭제 후 상품명: ', row_cnt)
        print()
        print()

        # 젤 앞에 []는 무조건 브랜드임. 정규식을 삭제
        targetStrs = [
            r'^\[.+\]' # ^는 시작을 의미.
        ]
        absolute_brand_filtered, absolute_brand_log = self.removeReg(targetStrs)
        del_logs.absolute_brand_log = (absolute_brand_log)


        # 이름이 완벽하게 같을 때만 삭제
        self.remove_duplicated()

        # self.get_name

        # 키워드 지우기
        # removingStrs = ['후니케이스', '다번다', '뷰티컬'
        #     , '아이윙스', '피포페인팅', '하이셀', '에이브', '이거찜', 'PVC', '리빙114', '슬림스', '모던스', 'SNW', 'ABM도매콜', '애니포트', '헤어슈슈', '베이비캠프',
        #                 '가디언블루', '그린피앤에스', '템플러', '클리카', '유앤미', '저혈당', '레인보우', 'ABM', '도매콜', '성기', '애니포트', '정확도', '특가',
        #                 '세일', '할인', '최저가', '액티몬', '엑티몬', '특가', '세일', '할인', '최저가', 'TWEEZER', 'coms', '문구List', 'PC용품', '제이앤지', '네오텍스', 'NEWUM', '네오텍스', '네온샌드', '키친프리'
        #                 ,'헨리제이에스','로하스', '비츠온', 'NEW', '미러범퍼', '아몬스', '정밀 핀셋', '드리온', '금홍팬시', 'kimspp', 'GPOP', '삼아', '우일파워', '파워맨', '로마네', '매직온'
        #                 , '폼폼푸린', 'SYSMAX', 'bob', '샤샤', '데이즈', '쓰리몰', '프릴카라', '아잠', '풍선대통령', '딜라이트 ', 'New', '바니랜드', '은창', '자미로운', '리브리움', '비온뒤'
        #                 , '뉴벌크', '플레플레', '대성푸드', '그린무역', '네추럴스파이스', '면사랑', '이엔푸드', '이츠웰', 'SIB', 'TYESO', 'BEAT', 'BTWIN'
        #                 ]
        # 중복제거
        col_before = '변경 전'
        col_after = '변경 후'

        removingStrs = self.keyword_df[col_before].tolist()
        replaces = self.keyword_df[col_after].tolist()
        before_len = len(removingStrs)
        removingStrs_set = set(removingStrs)  # 중복지우기
        after_len = len(removingStrs_set)
        removingStrs = list(removingStrs_set)
        print('중복되는 키워드 개수 : ', before_len - after_len)
        charFiltered, keyword_log = self.remove_keywords(removingStrs, replaces)  # 새로운 배열을 return한다.
        del_logs.keyword_log = (keyword_log)
        # tmpSeries = (charFiltered)
        # print(tmpSeries)
        # myFilter.df[product_col_name] =  charFiltered # 데이터 프레임에 추가될 때는 인덱스를 기준으로 추가된다. 앞에서 잘랐기 때문에 인덱스가 1부터 시작된다. 0부터 있어서 문제가 되었던 것이다.
        print('키워드 지우기')
        print(self.df[self.product_col_name].head(10))
        print(self.df[self.product_col_name].count())
        print()
        print()

        # 정규표현식 삭제
        # re.sub를 사용할 떈 //g를 사용하면 안된다.
        targetStrs = [
            r'[0-9a-zA-Z]+-[0-9a-zA-Z]+',  # DP-1234,
            r'[a-zA-Z]{2}[0-9]{3,}',  # DB12 //잘못하면 USB2 이런것도 걸린다. x12 이런게 같이 걸림. W019..이건 양보하자.
            r'^[0-9]+\.',  # 09. 발가락 보호대. 12. 허리보호대
            r'^[0-9]{4,}',  # 1000 발가락 보호대, 2500 손소독제 이런 이름이 있다.
            r'[0-9]{5,9}',  # 숫자5개 이상연속
            r'[0-9]+원'  # 숫자+원

        ]
        regFiltered, regexp_log = self.removeReg(targetStrs)
        del_logs.regexp_log = (regexp_log)

        # 특수문자 제거
        # 특수문자는는 페이스로 대체. 스페이스가 2개 되더라도 나중에 뒤에서 스페이스 여러개 처리하기 때문에 상관 x

        replace_pairs = []
        replace_pairs.append(ReplacePair('\/', ' '))  # . regexp일 때는 괄호도 이스케이프 해야함. regexp에서 특수문자기 때문.
        replace_pairs.append(ReplacePair('\(', ' '))
        replace_pairs.append(ReplacePair('\)', ' '))
        replace_pairs.append(ReplacePair('\[', ' '))
        replace_pairs.append(ReplacePair('\]', ' '))
        replace_pairs.append(ReplacePair('\{', ' '))
        replace_pairs.append(ReplacePair('\}', ' '))
        replace_pairs.append(ReplacePair('-', ' '))
        # replace_pairs.append(ReplacePair('EA', '개')) # 브랜드에 ea가 들어가면 '개' 로 바꿔버림...
        # replace_pairs.append(ReplacePair('ea', '개'))
        replacedStrs, special_char_log = self.remove_special_chars(replace_pairs)
        del_logs.special_char_log = (special_char_log)
        print('특수문자 -> 스페이스')
        print('row 개수 : ', self.df[self.product_col_name].count())
        print('상위10개 : ', self.df[self.product_col_name].head(10))
        print()
        print()

        # myFilter.df[product_col_name] = (regFiltered)
        print('regex 필터')
        print(self.df[self.product_col_name].head(10))
        print()
        print()
        return del_logs

    def process(self):
        """
        올인원 함수. 함수 호출 하나로 모두 해결가능하게
        쿠팡은 아니다.
        """
        del_logs = self.__process1()

        # 좌우 공백 삭제, strip. 인덱스가 1부터 시작인 상황.
        stripList = self.df[self.product_col_name].tolist()
        for i in range(len(stripList)):
            stripList[i] = stripList[i].strip()
        # myFilter.df[product_col_name] = pd.Series(stripList) # 수정한 것을 다시 대입할 수 없다.
        self.df[self.product_col_name] = stripList

        # 띄어쓰기 두번 삭제
        productNames = self.df[self.product_col_name].tolist()
        duplicatedSpaceRemoved = self.removeDuplicatedSpace(productNames)
        # productNames = pd.Series(duplicatedSpaceRemoved)
        self.df[self.product_col_name] = duplicatedSpaceRemoved
        print('duplicatedSpaceRemoved : \n', self.df[self.product_col_name].head(10))
        print()
        print()
        return del_logs

    def process_coupang(self):
        """
        """
        del_logs = self.__process1()

        # 이것도 순서대로 바꾸기 때문에 문자열이 긴 것부터 바꿔야한다. 근데 ()이런거 때문에 애매... 이건 완벽하게 하지말고 엑셀에서 눈으로 보면서 수정하자!
        # brand_regex = ['갤럭시 (?!워치)', '갤럭시워치', '갤럭시 워치'  # (?!x) 뒤에 x가 나오는 것은 제외.
        #     , '애플 (?!워치)', '애플워치', '애플 워치'
        #     , '아이폰 (?!워치)', '아이폰워치', '아이폰 워치'
        #     , '호환 호환', '호환  호환']  # '갤럭시워치'를 '갤럭시 워치'로 바꾸기 때문에 '갤럭시워치' -> '갤럭시 워치 호환 ' -> '갤럭시 워치 호환 호환'으로 바뀐다. 그래서 '호환 호환'을 처리해 줌

        # 나중에 스페이스 2개는 처리되기 때문에 뒤에 스페이스 붙이는게 로버스트함.
        # replace_strs = ['갤럭시 호환 ', '갤럭시 워치 호환 ', '갤럭시 워치 호환 '
        #     , '애플 호환 ', '애플 워치 호환 ', '애플 워치 호환 '
        #     , '아이폰 호환 ', '아이폰 워치 호환 ', '아이폰 워치 호환 '
        #     , '호환 ', '호환 ']

        # 브랜드 명 뒤에는 '호환' 붙이기. for 쿠팡.
        brand_replace_pairs = []
        # brand_replace_pairs.append(ReplacePair(r'갤럭시 (?!워치)', '갤럭시 호환 '))  # 클래스로 나타내는게 더 보기 좋다.
        brand_replace_pairs.append(ReplacePair(r'갤럭시', '갤럭시 호환 '))
        brand_replace_pairs.append(ReplacePair(r'갤럭시워치', '갤럭시 워치 호환 '))
        brand_replace_pairs.append(ReplacePair(r'갤럭시 워치', '갤럭시 워치 호환 '))

        brand_replace_pairs.append(ReplacePair(r'애플 (?!워치)', '애플 호환 '))
        brand_replace_pairs.append(ReplacePair(r'애플워치', '애플 워치 호환 '))
        brand_replace_pairs.append(ReplacePair(r'애플 워치', '애플 워치 호환 '))

        # brand_replace_pairs.append(ReplacePair(r'아이폰 (?!워치)', '아이폰 호환 '))
        brand_replace_pairs.append(ReplacePair(r'아이폰', '아이폰 호환 ')) #TODO : 아이폰13 케이스 아이폰 13 호환으로 하고 싶었는데 일단 아이폰 호환 13으로 했다..
        brand_replace_pairs.append(ReplacePair(r'아이폰워치', '아이폰 워치 호환 '))
        brand_replace_pairs.append(ReplacePair(r'아이폰 워치', '아이폰 워치 호환 '))


        brand_replace_pairs.append(ReplacePair(r'[zZ]플립', 'z플립 호환 '))
        brand_replace_pairs.append(ReplacePair(r'[zZ]폴드', 'z폴드 호환 '))



        # brand_replace_pairs.append(ReplacePair('호환 호환', '호환 '))
        # brand_replace_pairs.append(ReplacePair('호환  호환', '호환 '))

        brand_filterd, coupang_brand_filter_log = self.brandFilter(brand_replace_pairs)
        del_logs.coupang_brand_filter_log =(coupang_brand_filter_log)


        # 좌우 공백 삭제, strip. 인덱스가 1부터 시작인 상황.
        stripList = self.df[self.product_col_name].tolist()
        for i in range(len(stripList)):
            stripList[i] = stripList[i].strip()
        # myFilter.df[product_col_name] = pd.Series(stripList) # 수정한 것을 다시 대입할 수 없다.
        self.df[self.product_col_name] = stripList

        # 띄어쓰기 두번 삭제
        productNames = self.df[self.product_col_name].tolist()
        duplicatedSpaceRemoved = self.removeDuplicatedSpace(productNames)
        # productNames = pd.Series(duplicatedSpaceRemoved)
        self.df[self.product_col_name] = duplicatedSpaceRemoved
        print('duplicatedSpaceRemoved : \n', self.df[self.product_col_name].head(10))
        print()
        print()
        return del_logs
