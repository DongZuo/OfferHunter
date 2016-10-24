from django.conf.urls import url ##新版本取消了 patterns
from . import views  ##不用from regi



urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^applier/(?P<username>[\w\-]+)/$', views.applier, name='applier'), ##<>里面的username会传入views的applier函数作为参数。
    url(r'^add_student/$',views.add_student,name='add_student',),
    url(r'^applier/(?P<username>[\w\-]+)/add_apply/', views.add_apply, name='add_apply'),
    url(r'^predictform/', views.PredictForming,name='PredictForm'),##
    url(r'^predictresult',views.Predicting,name='Predicting')
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),

]
