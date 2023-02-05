import os.path

import pandas as pd
import re
import csv
import EsellersFilter as es

path = "C:/Users/minkun/Downloads/ownerclan_zhdhfhd33_ESELLERS_1659172 (1)/zhdhfhd33_템플릿1 수정일 1개월_ESELLERS_1659172_1_1.xls"

col1 = '스마트스토어 태그'
col2 = '쿠팡 검색어'


df_basic = pd.read_excel(path, sheet_name='기본정보')

