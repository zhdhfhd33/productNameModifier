import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main.stores.EsellersFilter import *
from main.core import *
from PIL import Image
from main.aws_core import *


def init():
    pdConfig()
    path = "resources/오너클랜 이셀러스.xls"  # test폴더 안에 있기 때문에 test는 빼야한다.

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
    return ef


# def write(path, df):
#     with pd.ExcelWriter(path) as writer:
#         df.to_excel(writer, sheet_name='기본정보', index=False)


def test_option_add_price_filter():
    ef = init()
    # ef1=ef.copy()
    # ef.option_add_price_filter()
    # print(ef.df_basic[ef.option_col_name]) #  테스트에서 출력을 보고 싶으면 옵션을 추가해야한다.
    with pd.ExcelWriter('test.xlsx') as writer:
        ef.df_basic.to_excel(writer, index=False)

def test_option50_over_filter():
    ef = init()
    d=ef.option50_over_filter()
    for i in d:
        print(i)

def test_img_down_all():
    ef=init()
    ef.img_down_all('resources/imgs/img_down_test/') # 마지막에 /까지 붙여야한다. 폴더가 실제로 존재해야함.


def test_img_size():
    li=os.listdir('resources/imgs/img_down_test')
    size_li=[]

    for i in li:
        img = Image.open('resources/imgs/img_down_test/'+i)
        size_li.append(img.size)

    for i in size_li:
        print(i) # 거의 이미지는 640*640이거나 1000*1000이다.

    x =  [i[0] for i in size_li]
    y =  [i[1] for i in size_li]
    print(f'min x : {min(x)}')
    print(f'min y : {min(y)}')

def test_img_filter():

    ef=init()
    ef.img_filter('resources/imgs/img_down_test/', 'resources/imgs/after_processing/', text_ratio=0.015, logo_ratio=0.15, text_loc= (10, 80), logo_loc=(10, 10) ) # 이 비율이 딱 예쁘다.



def test_s3_upload_img(): # 테완
    ef=init()
    path = "C:/Users/minkun/Downloads/test.jpg"
    bucket_name = 'my-shopping-img'
    filename = 'test_upload_img_s3123123.jpg' # 확장자 있이 사용. 확장자 없이 사용하면 내부적으로 처리해야하는게 늘고 역할이 2개가 된다.
    s3= aws_core.s3_getclient()

    url = ef.s3_upload_img(s3_client=s3, path=path, bucket_name=bucket_name, s3_file_name=filename) # url을 반환한다.
    print(url) # url에 접속하면 사진이 뜬다.


def test_s3_upload_img_all():
    ef=init()
    s3= aws_core.s3_getclient()

    # 상대경로를 넣으면 안된다. 항상 절대경로를 사용해야한다. 테스트 프레임웤이 아니라서 main으로 넘어가면 경로가 달라진다..
    urls = ef.s3_upload_img_all(s3_client=s3, dirpath = 'C:/Users/minkun/OneDrive/minkun/pyCharmWP/productNameModifier/test/resources/imgs/after_processing/')


    for i in urls:
        print(i)









# ----------------------------이렇게 검증할 수 있다.
# test_option50_over_filter()
# test_option_add_price_filter()
# test_img_down_all()
# test_img_size()
# test_img_filter()
# test_s3_upload_img()

test_s3_upload_img_all()











