import numpy as np
import pandas as pd
import os
"""
类目特征：
新的用户输入城市、宝宝年龄、性别。结合注册来源，给用户推荐不同类目的商品，可以根据实际情况分配比例
"""

os.chdir('E:\数据分析\冷启动')

data=pd.read_csv('冷启动-类目特征.csv',encoding='gbk')

# 数据空值和特殊值处理
# data.isnull().sum()/data.count()
data.dropna(inplace=True)
data=data.replace('="0"',0)
data['creator_city_code']=data['creator_city_code'].astype(str)
data_deal=data.drop(['fuid','creator_city_name'],axis=1)

# 根据城市、注册来源、宝宝年龄、性别对每个类目的次数进行聚类，并基于此进行排序，找出最大的类目
data_deal_probuycate=data_deal.groupby(['creator_city_code','register_source','sb_age','sb_sex']).apply(lambda x:x[['orc_cate_code3','buy_times']].nlargest(1,columns='buy_times')).reset_index()
result_pd=data_deal_probuycate

result_pd.to_csv("UserColdStart_GoodscateFeature.csv", encoding="utf_8_sig")