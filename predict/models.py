from django.db import models

# Create your models here.
class Student(models.Model):##一个申请人


    #StuId=models.IntegerField(default=0)##例如20160200001，02指MIS
    username=models.CharField(max_length=64,default='NA',primary_key=True,unique=True)##一亩三分地用户名
    GRE=models.IntegerField(default=0)##GREv+q
    GRE_W=models.FloatField(default=0)##GRE writing
    GPA=models.FloatField(default=0)##GPA
    TF=models.IntegerField(default=0)##托福总分
    TF_S=models.IntegerField(default=0)##托福口语
    major=models.CharField(max_length=64,default='NA')##本科专业
    college=models.CharField(max_length=64,default='NA')##本科学校
    exp=models.CharField(max_length=128,default='NA')##特殊经历
    year=models.CharField(max_length=64,default='NA')##年份
    country=models.CharField(max_length=16,default='NA')##国籍

    def __str__(self):
        return self.username

class Apply(models.Model):##一次申请记录

    AdId=models.IntegerField(default=0,primary_key=True)##例如20160200001，02指MIS,UNIQUE,PRIMARY_KEY
    username=models.CharField(max_length=64,default='NA')##一亩三分地用户名
    GRE=models.IntegerField(default=0)##GREv+q
    GRE_W=models.FloatField(default=0)##GRE writing
    GPA=models.FloatField(default=0)##GPA
    TF=models.IntegerField(default=0)##托福总分
    TF_S=models.IntegerField(default=0)##托福口语
    major=models.CharField(max_length=64,default='NA')##本科专业
    college=models.CharField(max_length=64,default='NA')##本科学校
    exp=models.CharField(max_length=128,default='NA')##特殊经历
    year=models.CharField(max_length=64,default='NA')##年份
    country=models.CharField(max_length=16,default='NA')##国籍m

    ap_date=models.DateField(default='2016-01-01')##申请日期
    result=models.CharField(max_length=16,default='NA')##申请结果：AD无奖，AD小奖，Red，WaitingList等
    adschool=models.CharField(max_length=32,default=' ')##申请目标学校
    degree=models.CharField(max_length=16,default='NA')##申请目标学位MS，PHD

    def __str__(self):
        return self.username

from django.contrib.auth.models import User ##登录系统的User


class PredUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)##引用django的User model，原本含有：username,password，email，first name，last name

    # The additional attributes we wish to include.
    website = models.URLField(blank=True) ##个人链接，可以不填
    picture = models.ImageField(upload_to='profile_images', blank=True) ##头像，上传到：<workspace>/taoxuezhe_project/media/profile_images/.

    # Override the __unicode__() method to return out username
    def __str__(self):##unicode
        return self.user.username
'''
##直接在model里面定义表单
MAJOR_CHOICES = (
        ('MIS', 'MIS'),
        ('CS', 'CS'),
        ('ALL', 'ALL'),
)
from django import forms
class PredictForm(forms.Form):

    school= forms.CharField(help_text="Please enter your interested school like CMU")
    major = forms.ChoiceField(choices=MAJOR_CHOICES,help_text="Please choose your interested major")
    grad_gpa= forms.FloatField(help_text="Please enter your GPA like 90.24")
    GRE = forms.IntegerField(help_text="Please enter your GRE total score like 325")
    GRE_AW = forms.FloatField(help_text="Please enter your GRE writing score like 3.5")
    TF = forms.IntegerField(help_text="Please enter your TOEFL score like 105")
    TF_S= forms.IntegerField(help_text="Please enter your TOEFL speaking score like 23")
'''