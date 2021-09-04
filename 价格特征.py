import numpy as np
import pandas as pd
import os

"""
价格特征：
新的用户输入城市、宝宝年龄、性别。结合注册来源，给用户推荐不同价格档次的商品，可以根据实际情况分配比例
所以最后需要加一步 与线上商品的档次 连接
"""

os.chdir('E:\数据分析\冷启动')


# 会员年龄处理 不同年龄段设置
def divide_age(age):
    """
    根据宝宝年龄分为以下8个档位
    """
    if age >= 0 and age <= 3:
        return 0 #初生儿
    if age >= 4 and age <= 6:
        return 1 #乳儿
    if age >= 7 and age <= 12:
        return 2 #婴儿
    if age >= 13 and age <= 24:
        return 3 #幼儿
    if age >= 25 and age <= 36:
        return 4 #小童
    if age >= 37 and age <= 72:
        return 5 #中童
    if age >= 73 and age <= 168:
        return 6 #大童
    else:
        return 9 #无法分类

data=pd.read_csv('冷启动-价格特征.csv',encoding='gbk')

# 数据空值和特殊值处理
data.isnull().sum()/data.count()
data.dropna(inplace=True)
data=data.replace('="0"',0)
data['sb_age']=data['sb_age'].astype(int)
data['creator_city_code']=data['creator_city_code'].astype(str)

# 打标年龄
data['sb_age'] = data['sb_age'].apply(divide_age)

# 去除结果表无关的列
data_deal=data.drop(['fuid','creator_city_name'],axis=1)

# 等分购买力区间 --已尝试过聚类，但效果不佳
data_deal['buy_label']=pd.qcut(data_deal['buy_avgprice'], 5, labels=[0,1,2,3,4])
data_deal=data_deal.drop('buy_avgprice',axis=1)

# 根据城市、注册来源、宝宝年龄、宝宝性别对购买力进行区间分类
data_deal_label=data_deal.groupby(['creator_city_code','register_source','sb_age','sb_sex']).apply(lambda x:x['buy_label'].mode()).reset_index()
data_deal_label=data_deal_label.rename(columns={'level_4': 'pro_buy'})
data_deal_label['pro_buy'].value_counts()

# 结果输出
result_pd=data_deal_label
result_pd.to_csv("UserColdStart_PriceFeature.csv", encoding="utf_8_sig")

