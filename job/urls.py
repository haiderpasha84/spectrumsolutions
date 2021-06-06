"""jobvac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('' , views.index, name ="home" ),


    path('prof/' , views.UserEdit_profile, name ="profile11" ),
    path('user-login/' , views.userlogin, name ="userlogin" ),
    path('user-home/' , views.userhome, name ="userhome" ),
    path('user-register/' , views.user_signup, name ="usersignup" ),
    path('user-dashbord/' , views.user_dashbord, name ="userdash" ),
    path('user-logout/' , views.userlogout, name ="userlogout" ),
    path('jobs/' , views.userlatest_job, name ="userjobs" ),
    path('jobs/<str:cat>/' , views.userlatest_job, name ="userjobs" ),
    path('job-detail/<int:id>/' , views.job_detail, name ="jobdetail" ),
    path('applyjob/<int:jid>/' , views.apply_job, name ="apply" ),
    path('changepassword/' , views.Change_Password, name ="changepassword" ),
    path('profile/' , views.Profile, name ="userprofile" ),
    path('catagoryy/' , views.catagory_job, name ="catagorywise" ),
    path('latestjobs1/' , views.userlatestjobs, name ="userlatestjobs" ),
    path('/search1/', views.home_search, name="search1"),
    path('usrblog/', views.user_blogg, name="usrblog"),



    # company api
    path('company-login/' , views.Company_Login, name ="companylogin" ),
    path('recuiter-logout/' , views.recruiterlogout, name ="companylogout" ),
    path('company-register/' , views.companyregister, name ="companyregister" ),
    path('company-home/' , views.companyhome, name ="companyhome" ),
    path('add-job/' , views.add_job, name ="addjob" ),
    path('add-cat/' , views.add_cat, name ="addcat" ),
    path('job-list/' , views.job_list, name ="joblist" ),
    path('editjob/<int:id>/' , views.job_edit, name ="jobedit" ),
    path('deljob/<int:id>/' , views.deljob, name ="deljob" ),
    path('apply/<int:id>/' , views.deljob, name ="apply" ),
    path('view_apply/', views.view_apply, name="view_apply"),
    path('change-pass/', views.RecruiterChange_Password, name="cchangepass"),
    path('edit_profilr/', views.CEdit_profile, name="editprofile"),
    path('cblog/' , views.blogg , name="companyblog"),
    path('subscride/' , views.blogg , name="companyblog"),



    # admin apis

    path('admin-login/', views.adminlogin, name="home"),
    path('admin-home/', views.admin_Home, name="adminhome"),
    path('admin-home1/', views.admin_Home1, name="adminhome1"),
    path('company-pending/' , views.view_newrecruiter, name ="newcompany" ),

    path('company-accepted/', views.acceptedcompanies, name="acceptedcompany"),
    path('company-rejected/', views.Rejected_companies, name="rejectcompany"),
    path('viewuser/', views.View_User, name="viewuser"),
    path('deluser/<int:id>/', views.del_User, name="deluser"),
    path('update/<int:id>/', views.assignstatus, name="assignstatuss"),
    path('delcompany/<int:id>/', views.Del_Recruiter, name="delcompany"),
    path('rejectuser/<int:id>/', views.Reject_Recruiter, name="rejectrecuiter"),
    path('adminblog/', views.admin_blogg, name="adminblog"),
    path('adminbloglist/', views.adminblog_list, name="adminbloglist"),
    path('delblog/<int:id>', views.delblog, name="adelblog"),




path('cbloglist/', views.cblog_list, name="cbloglist"),
path('cdelblog/<int:id>', views.cdelblog, name="cdelblog"),


path('ubloglist/', views.uublog_list, name="ubloglist"),
path('udelblog/<int:id>', views.uudelblog, name="udelblog"),




path('rec/', views.receiver1, name="receiver"),
path('snde/', views.mailsnd, name="mailsnd"),

path('sndemail/', views.mailsndfooter, name="sndemail"),



]

