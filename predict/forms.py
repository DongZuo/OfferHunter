from django import forms
from django.contrib.auth.models import User
from .models import Student,Apply#,PredUser

class StudentForm(forms.ModelForm):## inherit the Modelform class

    #StuId=forms.IntegerField(widget=forms.HiddenInput(), initial=0)##例如20160200001，02指MIS,widget=forms.HiddenInput()就是不在页面上显示此栏的意思。
    username=forms.CharField(max_length=64,help_text="Please enter the username")
    GRE=forms.IntegerField( initial=0,help_text="Please enter the GRE score")##GREv+q
    GRE_W=forms.FloatField(widget=forms.HiddenInput(),initial=0)##GRE writing
    GPA=forms.FloatField(initial=0,help_text="Please enter the GPA")##GPA
    TF=forms.IntegerField(widget=forms.HiddenInput(), initial=0)##toefl
    major=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##major
    college=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##school
    exp=forms.CharField(widget=forms.HiddenInput(),max_length=128,initial='NA')##exprience
    year=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##yaer
    country=forms.CharField(widget=forms.HiddenInput(),max_length=16,initial='NA')##country

    class Meta:
        model=Student
        fields=('username','GRE','GPA',)


class ApplyForm(forms.ModelForm):

    AdId=forms.IntegerField(help_text="Please enter the ID")##例如20160200001，02指MIS,UNIQUE,PRIMARY_KEY

    username=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##一亩三分地用户名
    GRE=forms.IntegerField(widget=forms.HiddenInput(), initial=0)##GREv+q
    GRE_W=forms.FloatField(widget=forms.HiddenInput(),initial=0)##GRE writing
    GPA=forms.FloatField(widget=forms.HiddenInput(),initial=0)##GPA
    TF=forms.IntegerField(widget=forms.HiddenInput(), initial=0)##托福总分
    major=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##本科专业
    college=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##本科学校
    exp=forms.CharField(widget=forms.HiddenInput(),max_length=128,initial='NA')##特殊经历
    year=forms.CharField(widget=forms.HiddenInput(),max_length=64,initial='NA')##年份
    country=forms.CharField(widget=forms.HiddenInput(),max_length=16,initial='NA')##国籍

    ap_date=forms.DateField(help_text='please enter the date',initial='2016-01-01')##申请日期
    result=forms.CharField(max_length=16,help_text="Please enter the result")##申请结果：AD无奖，AD小奖，Red，WaitingList等
    adschool=forms.CharField(max_length=32,help_text="Please enter the program name")##申请目标学校
    degree=forms.CharField(max_length=16,widget=forms.HiddenInput(),initial='NA')#申请目标学位MS，PHD
    class Meta:
        model=Apply
        exclude=('exp','TF_S',)


##predictform


class PredictForm(forms.ModelForm):

    MAJOR_CHOICES = (
        ('MIS', 'MIS'),
        ('CS', 'CS'),
        ('ALL', 'ALL'),)
    GRE=forms.IntegerField(help_text="Please enter your GRE total score like 325")##GREv+q
    GRE_W=forms.FloatField(help_text="Please enter your GRE writing score like 3.5")##GRE writing
    GPA=forms.FloatField(help_text="Please enter your GPA like 90.24")
    TF=forms.IntegerField(help_text="Please enter your TOEFL score like 105")##托福总分
    TF_S=forms.IntegerField(help_text="Please enter your TOEFL speaking score like 23")
    major=forms.ChoiceField(choices=MAJOR_CHOICES,help_text="Please choose your interested major")##本科专业
    adschool=forms.CharField(help_text="Please enter your interested school like CMU")
    country=forms.CharField(widget=forms.HiddenInput(),max_length=16,initial='NA')




    class Meta:
        model=Apply
        exclude=('country','exp','AdId','username','college','year','result','degree','ap_date',)


##User system

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
'''
class PredUserForm(forms.ModelForm):
    class Meta:
        model = PredUser
        fields = ('website', 'picture')'''
