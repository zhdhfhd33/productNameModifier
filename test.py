import os.path

import pandas as pd
import re
import csv

a=[1,2,3,4]

b= pd.Series(a)
print(b)

df=pd.DataFrame({'가':[1,2,3], '나':[4,5,6]}, index=[2,1,0])


print(df)

df['다']=b
print(df)
