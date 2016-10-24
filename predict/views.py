from django.shortcuts import render
from django.http import HttpResponse
from .models import Student,Apply
from .forms import StudentForm,ApplyForm
from django.contrib.auth.decorators import login_required ##用来拦截未登录用户使用某些功能
from datetime import datetime
def index(request):

    Student_list=Student.objects.order_by('GRE')[:5]##前五名的list
    context_dict={'Student5':Student_list}


    visits = request.session.get('visits')   ##
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())  ##session information stored in server side
        request.session['visits'] = visits                   ##instead of browser side
    context_dict['visits'] = visits


    response = render(request,'predict/index.html', context_dict)

    return response

def applier(request,username):##我们为每一个Student设计一个页面，来展示他的apply项目
    context_dict={}
    try:
        applier=Student.objects.get(username=username)
        context_dict['applier_name']=applier.username

        applys=Apply.objects.filter(username=applier.username)##一个student的申请列表

        context_dict['applys']=applys

        context_dict['applier']=applier

    except Student.DoesNotExist:
        pass

    return render(request,'predict/applier.html',context_dict)

@login_required  ##only for the login user
def add_student(request):
    if request.method=='POST':
        form=StudentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)

    else:
        form=StudentForm()

    return render(request,'predict/add_student.html',{'form':form})

@login_required
def add_apply(request,username):##先进入applier页面，在某个applier内部填写apply
    try:
        stu=Student.objects.get(username=username)
    except Student.DoesNotExist:
        stu=None


    if request.method=='POST':
        form=ApplyForm(request.POST)
        if form.is_valid():
            if stu:
                apply=form.save(commit=False)
                #apply.Student=stu
                apply.username=stu.username ##这里我们直接把username默认值设为该学生的username，就不用用户再填一次了。
                apply.save()##一定要save才能保存form的信息
                return applier(request,stu.username)##表单提交以后返回什么view
        else:
            print(form.errors)
    else :
        form=ApplyForm()

    context_dict = {'form':form, 'student': stu}

    return render(request, 'predict/add_apply.html', context_dict)
##开始预测
def Predicting (request,school,major,GRE,GRE_AW,TF,TF_S,grad_gpa):##,grad_rank,TF_S
    import pandas as pd
    from sklearn.linear_model import LinearRegression

    ##先过滤出某学校某专业的数据
    ad=pd.read_csv('train.csv',encoding='gbk')
    if school=='CMU':
        pattern=r'(cmu)|(CMU)'
    else :
        pattern=school
    train_set=ad[ad['adschool'].str.contains(pattern,na=False)]
    train_set=train_set[train_set.major==major]
    ##开始训练
    predictors = ['GRE','GRE_AW','TF','TF_S','grad_gpa']##grad_rank,TF_S

    alg = LinearRegression()
    alg.fit(train_set[predictors],train_set['result'])
    ##预测
    test=pd.DataFrame()
    test['GRE']=[GRE-300]
    test['GRE_AW']=[GRE_AW-2]
    test['TF']=[TF-85]
    test['TF_S']=[TF_S-18]
    test['grad_gpa']=[grad_gpa-80]

    prediction = alg.predict(test[predictors])
    value=prediction[0]
    context_dict={}
    context_dict['value']=value

    return render(request,'predict/predictresult.html',context_dict)

from django import forms
from .forms import PredictForm
def PredictForming(request):

    if request.method == 'POST': # 如果表单被提交
        form = PredictForm(request.POST) # 获取Post表单数据
        if form.is_valid(): # 验证表单
            test=form.save(commit=False)##
            return Predicting(request,test.adschool,test.major,test.GRE,test.GRE_W,test.TF,test.TF_S,test.GPA)##TF_S


    else:
        form = PredictForm() #获得表单对象

    return render(request,'predict/predictform.html', {'form': form})
#from .forms import UserForm, PredUserForm
'''

This part of registration function is disabled because we use the Django-Registration-Redux application
.
def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        pred_form = PredUserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and pred_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            pred = pred_form.save(commit=False)
            pred.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                pred.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            pred.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, pred_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        pred_form = PredUserForm()

    # Render the template depending on the context.
    return render(request,
            'predict/register.html',
            {'user_form': user_form, 'pred_form': pred_form, 'registered': registered} )

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/predict/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Predict account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print( "Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'predict/login.html', {})

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/predict/')
'''
