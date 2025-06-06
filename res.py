

import pandas as pd




pd1 = pd.read_csv('gov.csv')

if 'url' not in pd1.columns:
        pd1['url'] = ''


pd2 = pd.read_csv('./test/govss.csv')

# # pd2 的url 填充到pd1 的url中,根据code列匹配，如果pd1中没有url，则填充
for index, row in pd2.iterrows():
    code = row['code']
    url = row['url']
    if code in pd1['code'].values:
        if pd1.loc[pd1['code'] == code, 'url'].values[0] == '':
            pd1.loc[pd1['code'] == code, 'url'] = url





# # # 保存
pd1.to_csv('gov.csv', index=False)




# pd2 name 列出重复
pd2_duplicates = pd1[pd1.duplicated(subset=['name'], keep=False)]

# 打印重复的 name
print(pd2_duplicates[['name']])
