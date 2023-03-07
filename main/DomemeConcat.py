from main.stores.DomemeModifier import *

import os.path

# -----------------------------xlsx_concat 사용법-------------------------------
"""
도매매에서 마이박스 저장 후 수동으로 500개 씩 다운로드. 이후아래 함수를 통해 엑셀들 모두 합치면된다. 엑셀파일을 하나의 dir에 넣어놓으면 사용이 쉽다.
첨에 엑셀파일을 다 열어서 수동으로 하나씩 저장해줘야 하는 번거로움이 있다. pd가 열지를 못한다.
"""

dir = r"C:\Users\minkun\Downloads\2023.3.2도매매_일주일"
dir = dir.replace('\\', '/')
paths = os.listdir(dir)
abs_paths=[dir+'/'+i for i in paths]
concat_df = xlsx_concat(abs_paths)

res_path=r'C:\Users\minkun\OneDrive\minkun\pyCharmWP\productNameModifier\main\resources'
res_path = res_path.replace('\\', '/')
concat_df.to_excel(res_path+ '/' + '도매매_concat.xlsx', index=False)






