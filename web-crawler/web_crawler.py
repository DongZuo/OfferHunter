import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from pandas import DataFrame
import pandas as pd
def getAdLinks(url):##不知道为什么，用了会话登录（即使登录失败了），就能获取全部数据，不用会话只能爬到一半的内容。
    s=requests.Session()
    ##目前来看不需要登录也可以获取关键信息，暂时不登录了。
    payload={'username':'cdzzz','cookietime':'2592000','password':'a7a02f0e41cb44637468003121a820ed','quickfoward':'yes','handlekey':'ls'}
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
    r=s.get(url,data=payload,headers=header)
    bsAd=BeautifulSoup(r.text)   ##get到的js格式内容可以直接beautifulsoup

    adLinks=[]

    for link in bsAd.findAll('a',href=(re.compile("^(http://www.1point3acres.com/bbs/((thread)|(forum.php\?mod=viewthread)))"))):
        if 'href' in link.attrs:
             adLinks.append(link.attrs['href'])

    return adLinks


##getAdLinks('http://www.1point3acres.com/bbs/thread-165697-1-1.html')



def copyData(links):     ##遍历所有地址，获取录取数据和背景信息
    i=-1
    adID=[]
    username=[]
    tf=[]
    g=[]
    bg=[]
    ap_time=[]
    country=[]
    result=[]
    year=[]
    degree=[]
    major=[]
    school=[]
    grad_major=[]
    grad_school=[]
    grad_gpa=[]
    grad_rank=[]
    for link in links:
        adHtml=urlopen(link)
        adBs=BeautifulSoup(adHtml)

        for td in adBs.findAll('td',{'class':'plc'}):
            for li in td.findAll('li') :  ##每一个li就是一个可能包含有某一个变量值的字符串，但是格式不是string需要转换。
                if 'T单项和总分' in li.get_text():##如果有这个子字符串说明这是一个offer帖。
                    username.append(adBs.find('a',{'class':'xi2'},target='_blank',href=(re.compile("^(http://www.1point3acres.com/bbs/space-uid)"))).get_text())
                    tf.append(li.get_text().replace('T单项和总分:','').strip())
                    result.append(adBs.find('span',{"style":'margin-top: 3px'}).find('font',{'color':'black'}).get_text().replace(']',''))
                    year.append(adBs.find('span',{"style":'margin-top: 3px'}).find('font',{'color':'#666'}).get_text().replace('[',''))
                    degree.append(adBs.find('span',{"style":'margin-top: 3px'}).find('font',{'color':'blue'}).get_text())
                    major.append(adBs.find('span',{"style":'margin-top: 3px'}).find('font',{'color':'#F60'}).get_text())
                    school.append(adBs.find('span',{"style":'margin-top: 3px'}).findAll('b')[2].get_text())
                    i=i+1
                    adID.append(i)



                if '本科:'in li.get_text() and ', GPA'in li.get_text() and '@'in li.get_text(): ##and 是逻辑的且。
                    regex=re.compile('@|\, GPA|\:')
                    tobesplit=li.get_text().replace('本科:','').strip()

                    grad_bg=regex.split(tobesplit)
                    grad_major.append(grad_bg[0])
                    grad_school.append(grad_bg[1])
                    grad_gpa.append(grad_bg[2])
                    grad_rank.append(grad_bg[3])

                if 'G单项和总分' in li.get_text():
                    g.append(li.get_text().replace('G单项和总分:','').strip())##strip是去除空格的操作
                if '背景的其他说明（如牛推等）'in li.get_text():
                    bg.append(li.get_text().replace('背景的其他说明（如牛推等）:','').strip())
                if '提交时间'in li.get_text():
                    ap_time.append(li.get_text().replace('提交时间:','').strip())
                if '结果学校国家、地区'in li.get_text():
                    country.append(li.get_text().replace('结果学校国家、地区:','').strip())
        if len(grad_major)>len(username): ##如果本科这一栏的个数超过了其他的个数，我们把这个多余的数据删掉。
                    grad_major.pop()
                    grad_school.pop()
                    grad_gpa.pop()
                    grad_rank.pop()





    adData={'country':country,'ap_time':ap_time,'year':year,'background':bg,'grad_rank':grad_rank,'grad_gpa':grad_gpa,'grad_school':grad_school,'grad_major':grad_major,'GRE':g,'TF':tf,'major':major,'degree':degree,'result':result,'adschool':school,'username':username}

    adFrame=DataFrame(adData,index=adID,columns=['username','adschool','result','degree','major','TF','GRE','grad_major','grad_school','grad_gpa','grad_rank','background','year','ap_time','country'])

    return adFrame










CS_16=getAdLinks('http://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=165697&extra=page%3D1%26filter%3Dtypeid%26typeid%3D598%26typeid%3D598')
ad_cs16=copyData(CS_16)


mis_15=pd.read_csv('mis_15.csv',encoding='gbk')
cs_15=pd.read_csv('CS_15.csv',encoding='gbk')
mis_16=pd.read_csv('mis_15.csv',encoding='gbk')
cs_16=pd.read_csv('CS_16.csv',encoding='gbk')
AD_15_16=mis_15.append(cs_15, ignore_index=True) ##这里的合并不是merge（）也不是concat
AD_15_16=AD_15_16.append(mis_16,ignore_index=True)
AD_15_16=AD_15_16.append(cs_16,ignore_index=True)

AD_15_16.to_csv('ad_15_16.csv')
