# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 14:03:20 2016

@author: Administrator
"""
'''
import pandas as  pd
import numpy as np
ad=pd.read_csv('ad_15_16.csv',encoding='gbk')
##先创造出一个username和背景的dataframe，然后再把它merge到总表里面。
BG=pd.DataFrame({'username':ad['username'],'TF':ad['TF'],'GRE':ad['GRE'],'grad_gpa':ad['grad_gpa'],'grad_rank':ad['grad_rank']})
BG['grad_gpa']=BG['grad_gpa'].apply(lambda x: np.NaN if str(x).isspace() else x)##把GPA这一列的空值替换为NaN
BG=BG.dropna(thresh=3) ##thresh 是容忍阀，意思是至少有3个变量不为nan。
BG=BG.drop_duplicates(['username'])##如果username重复那就删除这一行。
#BG.to_csv('BG_15_16.csv')
##现在已经得到了一个索引，即username与背景意义对应的关系。我们先把背景merge进去，然后再对各个背景进行处理。
BG=pd.read_csv('bg.csv',encoding='gbk')
ad=ad.drop(['TF','GRE','grad_gpa','grad_rank'],axis=1)##不含这4列的总表（方便后面merge）
ad=pd.merge(ad,BG,on='username',how='outer')##how='outer'这样就不会把第二个DF里面不含username的行删去了，而是合并。（merge默认为inner）
ad.drop('Unnamed: 0_x',axis=1, inplace=True)  ##删除没用的几列
ad.drop('Unnamed: 0.1',axis=1, inplace=True)  
ad.drop('Unnamed: 0_y',axis=1, inplace=True)
##现在的ad是补充了所有背景信息的录取情况。
##统计描述：
ad.describe()
np.percentile(ad.GRE.dropna(),60) ##60分位数GRE324
np.percentile(ad.GRE.dropna(),50) ##中位数GRE322

np.percentile(ad.GRE_AW.dropna(),50)##AW中位数3
ad.GRE_AW.mean()                    ##均值3.30

##Gre is around 300-340 so we use GRE-300 as a feature,and we fillna
ad.GRE=ad.GRE-300
ad["GRE"] = ad["GRE"].fillna(ad["GRE"].median())
##As the same reason, GRE_AW-2 and fillna
ad.GRE_AW=ad.GRE_AW-2
ad["GRE_AW"] = ad["GRE_AW"].fillna(ad["GRE_AW"].median())
#TO DO
ad.result=ad.result.fillna(0)

ad.TF=ad.TF.fillna(102)
ad.TF=ad.TF-85

ad.TF_S=ad.TF_S-18
ad.TF_S=ad.TF_S.fillna(4)

ad.grad_gpa=ad.grad_gpa.fillna(87.1)
ad.grad_gpa=ad.grad_gpa.astype(float)
ad.loc[ad['grad_gpa']<4.1,'grad_gpa']=87.1+(4.5/0.4)*(ad[ad['grad_gpa']<4.1]['grad_gpa']-3.6)
ad.grad_gpa=ad.grad_gpa-80

##对结果赋值
ad.loc[ad["result"] == "AD小奖", "result"] = 1
ad.loc[ad["result"] == "AD无奖", "result"] = 1
ad.loc[ad["result"] == "Offer", "result"] = 1
ad.loc[ad["result"] == "Rej", "result"] = 0
ad.loc[ad["result"] == "WaitingList", "result"] = 0
##rank
ad.loc[ad['grad_rank'].str.contains('本科非211',na=False),'grad_rank']=1
ad.loc[ad['grad_rank'].str.contains('本科其他211',na=False),'grad_rank']=2
ad.loc[ad['grad_rank'].str.contains('本科Top30 211',na=False),'grad_rank']=3
ad.loc[ad['grad_rank'].str.contains('本科Top15 211',na=False),'grad_rank']=4
ad.loc[ad['grad_rank'].str.contains('本科：南大，浙大，复旦，上交',na=False),'grad_rank']=5
ad.loc[ad['grad_rank'].str.contains('本科：北大，清华，科大，中科院，特色学校牛专业',na=False),'grad_rank']=6
ad.loc[ad['grad_rank'].str.contains('海本',na=False),'grad_rank']=4
ad.grad_rank=ad.grad_rank.astype(float)
ad.grad_rank.describe()
ad.grad_rank=ad.grad_rank.fillna(4)


ad.to_csv('train.csv')
##start machine learning using logistic model
#from sklearn import cross_validation

##不必再重复前面的数据处理操作，直接读取train这个文件即可。

'''
from sklearn.linear_model import LinearRegression
import pandas as  pd


def predicting (school,major,GRE,GRE_AW,TF,TF_S,grad_gpa,grad_rank):
    ##先过滤出某学校某专业的数据
    ad=pd.read_csv('train.csv',encoding='gbk')
    if school=='CMU':
        pattern=r'(cmu)|(CMU)'
    else :
        pattern=school
    train_set=ad[ad['adschool'].str.contains(pattern,na=False)]
    train_set=train_set[train_set.major==major]
    ##开始训练
    predictors = ['GRE','GRE_AW','TF','TF_S','grad_gpa','grad_rank']

    alg = LinearRegression()
    alg.fit(train_set[predictors],train_set['result'])
    ##预测
    test=pd.DataFrame()
    test['GRE']=[GRE-300]
    test['GRE_AW']=[GRE_AW-2]
    test['TF']=[TF-85]
    test['TF_S']=[TF_S-18]
    test['grad_gpa']=[grad_gpa-80]
    test['grad_rank']=[grad_rank]
    prediction = alg.predict(test[predictors])
    
    return prediction[0]
    
##test
a=predicting('CMU','MIS',324,3.5,106,23,90.24,4)
'''
To evaluate the result

kf = KFold(ad.shape[0], n_folds=3, random_state=1)

scores = cross_validation.cross_val_score(alg, ad[predictors], ad["result"], cv=4)
predictions = []
for train,test in kf:
    train_predictors = (ad[predictors].iloc[train,:])
    # The target we're using to train the algorithm.
    train_target = ad["result"].iloc[train]
    # Training the algorithm using the predictors and target.
    alg.fit(train_predictors, train_target)
    # We can now make predictions on the test fold
    test_predictions = alg.predict(ad[predictors].iloc[test,:])
    predictions.append(test_predictions)
    
predictions = np.concatenate(predictions, axis=0)
accuracy = np.sum(predictions == ad["result"]) / len(predictions)
'''

