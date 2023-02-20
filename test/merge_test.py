import pandas as pd

df1=pd.read_excel('resources/스스 상품리스트.xls')
df2=pd.read_excel('resources/올린상품들.xls')

merge_outer = pd.merge(df1,df2, how='outer',on='도매매 상품번호')
with pd.ExcelWriter('merged.xlsx') as writer:
    merge_outer.to_excel(writer, index=False)


