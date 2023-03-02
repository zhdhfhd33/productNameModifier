import os.path

import pandas as pd

from main import core
import urllib.request as req

from PIL import Image, ImageFont, ImageDraw
# import aws_core
from main import aws_core
from main import security




class Option50Log():
    def __init__(self, idx, len, after_len):
        """
        :param idx: 데이터프레임 idx
        :param len: 처리 전 옵션 개수
        :param after_len: 처리 후 옵션 개수
        """
        self.idx = idx
        self.len = len
        self.after_len = after_len

    def __str__(self):
        return f'idx : {self.idx} len : {self.len}'


class EsellersCombinationalOption():
    def __init__(self, names, add_price, cnt, is_expose, url='', manage_code='', volume=0
                 ):

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
        self.is_expose = is_expose

        self.url = url
        self.manage_code = manage_code
        self.volume = volume

    def __str__(self):
        return f'option_names : {self.names}, add_price : {self.add_price}, cnt : {self.cnt}, is_expose : {self.is_expose}, url : {self.url}, manage_code : {self.manage_code}, volumn : {self.volume}'

    def to_str(self):
        res = ''
        for i in self.names:
            res += i + '*'

        res += '*'  # 하나만 더 추가하면 **가 된다.
        after_members = [self.add_price, self.cnt, self.is_expose, self.url, self.manage_code,
                         self.volume if self.volume != 0 else '']
        for i in after_members:
            res += str(i) + '*'

        filtered_names, delogs = core.replace_by_regexp([res], [r'\*+$'], [''])
        assert len(filtered_names) == 1 and len(delogs) == 1
        return filtered_names[0]


class EsellersFilter:
    def __init__(self, df_basic, df_extend, product_col_name='상품명*', option_col_name='선택사항 상세정보',
                 option_type_col_name='선택사항 타입', price_col_name='판매가*', represent_img_col_name='이미지1(대표/기본이미지)*',
                 my_code='판매자 관리코드'):
        self.df_basic = df_basic
        self.df_extend = df_extend
        self.product_col_name = product_col_name  # 상품명*
        self.option_col_name = option_col_name  # 선택사항 상세정보
        self.option_type_col_name = option_type_col_name  # 선택사항 옵션명
        self.price_col_name = price_col_name  # 판매가*
        self.represent_img_col_name = represent_img_col_name
        self.my_code = my_code

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

        tmp_others = [''] * 5 + [0]
        for i in range(len(others)):
            if i == 0 or i == 1:
                tmp_others[i] = int(others[i])  # add_price, cnt는 숫자로 인식
            else:
                tmp_others[i] = others[i]
        es_option = EsellersCombinationalOption(names=option_names, add_price=tmp_others[0], cnt=1,
                                                is_expose=tmp_others[2], url=tmp_others[3], manage_code=tmp_others[4],
                                                volume=tmp_others[5])
        return es_option

    def parse_df_options(self):
        """
        옵션 파싱해서 Series 반환. 인덱스도 동일.
        리스트나 ndarr로 하면 안된다. 옵션이 아예없는 애들도 있기 때문에 인덱스로 join해야함.. df상태에서 다뤄야한다.
        :return: series. ser[i]=[EsellersCombinationalOption1, EsellersCombinationalOption2,,,,]
        """
        option_types = self.df_basic[self.option_type_col_name].str.strip()  # 혹시 모르니 strip()
        option_str = self.df_basic[self.option_col_name]  # 시리즈
        idx = []
        parsed = []
        for i in option_types.index:  # range사용할 때는 .iloc사용해야함. 인덱스로 다루는게 편하다. 다른 컬럼에 접근할 때도 유용함.
            row = []
            if option_types[i] == '조합형' and not pd.isna(option_str[i]):
                options = option_str[i].split('\n')  # 개행으로 끊어야한다.
                for j in options:
                    row.append(self.__parse_option(j))
                parsed.append(row)
                idx.append(i)
        ser = pd.Series(parsed, index=idx)
        return ser

    def option_add_price_filter(self):
        """
        옵션에 추가금있으면 지마켓, 옥션에는 등록 안된다. (지마켓, 옥션)
        '옵션 추가금'을 '가격'으로 반영
        :return:
        """
        ser = self.parse_df_options()  # 시리즈반환. EsellersCominationOption 객체가 들어있다.
        del_logs = []
        # 추가금을 0으로하고 가격을 추가
        for i in ser.index:
            add_prices = [_.add_price for _ in ser[i]]  # 가격만 뽑는다.
            max_add_price = max(add_prices)

            # del log
            # if max_add_price != 0:
            # del_logs.append(DelLog(content=None, regexp=None, idx=i))
            # TODO : log남기기. 우선순위낮음.

            self.df_basic[self.price_col_name][i] += max_add_price
            for j in ser[i]:
                j.add_price = 0
        # 셀 하나에 들어갈 수 있게  합치기
        res_li = []
        for i in ser.index:
            str_li = [_.to_str() for _ in ser[i]]
            res_li.append('\n'.join(str_li))

        zero_add_price_ser = pd.Series(res_li, ser.index)
        self.df_basic[self.option_col_name] = zero_add_price_ser
        return zero_add_price_ser, del_logs

    def option50_over_filter(self, ):
        """
        옵션이 50개 넘어가면 50개 까지만 등록. for 지마켓, 옥션
        :return:
        """
        del_logs = []
        ser = self.parse_df_options()
        for i in ser.index:
            LEN = len(ser[i])
            if LEN > 50:
                ser[i] = ser[i][:51]  # 50개 까지만 넣기기
                del_logs.append(Option50Log(idx=i, len=LEN, after_len=len(ser[i])))

        res_li = []
        for i in ser.index:
            str_li = [_.to_str() for _ in ser[i]]
            res_li.append('\n'.join(str_li))

        res_ser = pd.Series(res_li, index=ser.index)
        self.df_basic[self.option_col_name] = res_ser
        return del_logs

    def img_down_all(self, save_dir):
        """
        :param save_dir 저장하고자 하는 폴더 ex)2023-2-13-오너클랜최신순500. 엑셀이름 그대로 사용.
        :return:
        """

        if not os.path.isdir(save_dir):  # 없을 때만 만든다.
            os.makedirs(save_dir)
        down_img = lambda url, savdir: req.urlretrieve(url, savdir)  # 임시함수
        imglink_ser = self.df_basic[self.represent_img_col_name]
        my_code_ser = self.df_basic[self.my_code]

        for i in imglink_ser.index:
            # 확장자 얻기.
            # 파일이름은 판매자관리코드를 사용
            _, ext = os.path.splitext(imglink_ser[i])
            save_path = save_dir + my_code_ser[i] + ext
            down_img(imglink_ser[i], save_path)
            print(save_path)

    def img_filter(self, before_dirpath, after_dirpath, text_ratio, logo_ratio, text_loc, logo_loc):
        """
        이미지를 읽어서 로고 삽입 이후 after dirpath에 저장한다.

        :param before_dirpath: 원본 이미지들이 있는 dir path. 마지막에 / 로 끝나야한다.
        :param after_dirpath: 수정된 이미지들이 저장될 dir path. 존재하지 않아도 된다. 마지막에 /로 끝나야 한다.
        :param text_ratio 0.1 # 10%
        :param y_ratio 0.1 # 10%
        :return: None
        """
        if not os.path.isdir(after_dirpath):  # after_dirpath 없을 때만 만든다.
            os.makedirs(after_dirpath)

        imglist = os.listdir(before_dirpath)
        fontpath = 'C:/Users/minkun/OneDrive/minkun/pyCharmWP/productNameModifier/main/resources/GmarketSansTTF/GmarketSansTTFBold.ttf'
        logo = Image.open('/main/resources/logo.png')

        for i in imglist:
            img = Image.open(before_dirpath + i)
            # 이미지 마다 사이즈는 다르다.
            x, y = img.size
            fontsize = int(x * text_ratio)

            logo_x, logo_y = logo.size  # 로고 크기
            logo_coefficient = (x * logo_ratio) / logo_x  # logo_y * logo_coefficient 하면 x, y비율이 보존된다. 전체 크기의
            resized_logo = logo.resize((int(logo_x * logo_coefficient), int(logo_y * logo_coefficient)))
            font = ImageFont.truetype(fontpath, fontsize)
            imgdraw = ImageDraw.Draw(img)
            imgdraw.text(text_loc, '넥스트 레벨 스토어(널리)', (0, 0, 0), font=font)  # (11,81,238) 파란색
            cv2_logo = core.piltocv2(resized_logo)
            cv2_img = core.piltocv2(img)
            after_cv2_img = core.paste_logo(cv2_logo, cv2_img, *logo_loc)  # 로고 씌우기. 가로,세로. * = unpacking
            img = core.cv2topil(after_cv2_img)
            # img.paste(im=resized_logo, box=(fontsize + 25, fontsize + 10))  # 사진 덮어 씌우기.
            after_path = after_dirpath + i
            img.save(after_path)  # 이미지 저장.
            print(f'img after_path : {after_path}')
            # 이미지 한번에 for문으로 읽으면 터질듯. with으로 open close해야한다. 여기선 그런게 없기 때문에 알아서 갈비지 컬렉션 할듯??..
        return


    def s3_upload_img(self, s3_client, path, bucket_name, s3_file_name):
        """
        S3에 이미지를 업로드한다.
        :param s3_client s3객체
        :param path:
        :param bucket_name:
        :param s3_file_name: 확장자 있어야한다.
        :return: 접근 url을 반환.
        """
        # assert '.' not in s3_file_name, 'filename은 확장자(.)를 포함하지 않아야 합니다.'
        # assert '/' not in s3_file_name, 'filename은 /를 포함하지 않아야 합니다.'

        dirname, ext = os.path.splitext(path)

        s3_client.upload_file(
            path,  # "C:/Users/minkun/Downloads/이미지다운4.jpg", 확장자 까지 포함해야한다.
            bucket_name,  # 'my-shopping-img'
            s3_file_name,  # 'test3.jpg' 확장자 까지 제대로 붙여야한다. 이 이름으로 버킷에 저장된다.
            ExtraArgs={'ContentType': f"image/{ext[1:]}", 'ACL': "public-read"}  # content type을 설정해야 브라우저에서 올바르게 띄워준다.

        )
        base, ext = os.path.splitext(path)
        url = aws_core.get_url(s3_client, s3_file_name)
        return url

    def s3_upload_img_all(self, s3_client, dirpath):
        """
        :param dirpath: 사진들이 저장되어 있는 dir 경로
        :return: urls [url1, url2, url3,,]
        """
        files = os.listdir(dirpath)
        urls=[]

        for i in files:
            path = dirpath+i
            url = self.s3_upload_img(s3_client=s3_client, path=path, bucket_name=security.bucket_name, s3_file_name= i)
            urls.append(url)

        return urls




if __name__ == '__main__':
    # ProductNameModifier.pdConfig()
    core.pdConfig()
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
