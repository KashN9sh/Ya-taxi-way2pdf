import pandas as pd
import os

files = os.listdir('Otc/')

list_of_dfs = []
for file in files:
    #os.rename('Otc/' + file, 'Otc/' + file + '.xlsx')
    xl = pd.ExcelFile(os.path.join('Otc/',file))
    res = len(xl.sheet_names)
    if res < 2:
        d = pd.read_excel(os.path.join('Otc/',file), sheet_name=0)
        list_of_dfs.append(d)
        #print(d)
big_df = pd.concat(list_of_dfs, ignore_index=True)#ignore_index to reset index of big_df
big_df = big_df.drop_duplicates('Номер счета')
print(big_df)

big_df.to_csv('data.csv', index=False)