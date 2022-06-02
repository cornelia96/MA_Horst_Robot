import pandas as pd

df=pd.DataFrame([['a', 'b'], ['c', 'd']], index=['row 1', 'row2'], columns=['col 1', 'col2'])

df.to_excel("excel.xlsx")