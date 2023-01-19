import os.path

import pandas as pd
import re
import csv

a=[1,2,3,4]

b= pd.Series(a)
print(b)

df=pd.DataFrame({'가':[1,2,1], '나':[4,5,6]})


print(df)

df['다']=b
print(df)
bo = df['가']==1
print(bo)

print(df[bo])

a=pd.Series([1, 2, 3, '', 3])
a=a.tolist()
print(a)

