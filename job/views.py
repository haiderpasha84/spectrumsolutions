from idlelib.idle_test.test_run import S
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout, login
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
# Create your views here.
from job.models import StudentUser
from job.models import Recruiter, Add_job, Catagory, Apply, allusers
from django.shortcuts import redirect
from datetime import date
from django.contrib import messages
from blog.models import post
from jobvac import settings
from django.core.paginator import Paginator


def index(request):
    data = Add_job.objects.filter().order_by('-id')[:10]
    dataxx = post.objects.filter().order_by('-post_id')[:4]
    datax1 = Recruiter.objects.filter().order_by('?')
    d = {'data': data, 'datax': dataxx, 'datay': datax1}
    return render(request, 'job/index-3.html', d)


#
# def usrhom(request):
#     return HttpResponse("Hii")


# users functions
@login_required(login_url='/user-login/')
def Profile(request):
    user = User.objects.get(id=request.user.id)
    data = StudentUser.objects.get(user=user)
    d = {'data': data}
    return render(request, 'job/usrprofile.html', d)


def UserEdit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user = User.objects.get(id=request.user.id)
    pro = StudentUser.objects.get(user=user)
    if request.method == 'POST':
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        m = request.POST['mobile']
        try:
            g = request.POST['gender']
            pro.gender = g
            pro.save()
        except:
            pass
        try:
            fi = request.FILES['image']
            pro.image = fi
            pro.save()
        except:
            pass
        pro.user.username = u
        pro.user.last_name = l
        pro.user.email = e
        pro.mobile = m
        pro.save()
        pro.user.save()
        error = True
    d = {'error': error, 'pro': pro}
    return render(request, 'job/profile.html', d)


def user_signup(request):
    error = ""

    if request.method == "POST":
        unn = request.POST['dzname']

        emal = request.POST['email']
        contact = request.POST['cnum']
        password1 = request.POST['pass']
        imge = request.FILES['photo']
        gen = request.POST['gender']

        print("============================")

        exist1 = User.objects.filter(email=emal)
        exist2 = User.objects.filter(username=unn)
        if exist2:
            error = "existss1"

        if exist1:
            error = "existss"

        else:
            try:
                user = User.objects.create_user(username=unn, email=emal, password=password1)
                StudentUser.objects.create(user=user, mobile=contact, image=imge, gender=gen, type="student")
                error = "no"
            except:
                error = "yes"

    dic = {'error': error}
    return render(request, 'job/user-register.html', dic)


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('/user-home/')
    error = ""
    if request.method == "POST":
        unam = request.POST["email"]
        passd = request.POST['password']
       
        user = authenticate(request, username=unam, password=passd)
        if user is not None:
           

            try:
                user12 = StudentUser.objects.get(user=user)

                if user12.type == "student":
                    login(request, user)
                    error = "no"
                else:
                    error = "yess"
            except:
                error = "yes"

        else:
            error = "yes"

    dic = {'error': error}

    return render(request, 'job/user-login.html', dic)


def userlogout(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect('/user-login')
    else:
        logout(request)

        return redirect('/user-login')


def home_search(request):
    d = ""
    if request.method == "POST":
        datas = request.POST['query']
        data1 = Add_job.objects.filter(title__icontains=datas)
        data2 = Add_job.objects.filter(recruiter__company__contains=datas)
        data3 = Add_job.objects.filter(description__icontains=datas)
        data4 = Add_job.objects.filter(position__icontains=datas)
        data5 = Add_job.objects.filter(location__icontains=datas)
        data6 = Add_job.objects.filter(catagory__catagory_name__contains=datas)
        data7 = Add_job.objects.filter(timee__contains=datas)

        x1 = data1.union(data2, data3)
        x2 = x1.union(data4, data5)
        x3 = x2.union(data6, data7)
        if x3.count == 0:
            messages.warning(request, "no result can be found please refine your query")
    
    print(x3)
    d = {'data': x3}
    return render(request, 'job/search.html', d)


def user_dashbord(request):
    if not request.user.is_authenticated:
        return redirect('/user-login')
    else:
        return render(request, 'job/userdashbord.html')


@login_required(login_url='/user-login/')
def userlatest_job(request):
    caa = Catagory.objects.all()
    data = Add_job.objects.all()
    user = User.objects.get(id=request.user.id)
    sign = StudentUser.objects.get(user=user)
    data1 = Apply.objects.filter(sign=sign)
    li = []
    for i in data1:
        li.append(i.job.id)
    d = {'data': data, 'li': li, 'catag': caa}
    return render(request, 'job/latestuser-jobs.html', d)


def userhome(request):
    data = Add_job.objects.all().order_by('-id')[:20]
    d = {'data': data}
    return render(request, 'job/userhome.html', d)


def userlatestjobs(request):
    data = Add_job.objects.all().order_by('-id')[:30]
    d = {'data': data}
    return render(request, 'job/homelatestjob.html', d)


@login_required(login_url='/user-login/')
def catagory_job(request):
    data = ""
    idd = ""
    catt = ""
    if request.method == "POST":
        caa = Catagory.objects.all()
        idd = request.POST['catwise']
        print("-===============")
        print(idd)
        print("-===============")
        if not idd:
            print("-======i ama in=========")
            catt = Catagory.objects.all()
            data = Add_job.objects.all()
        else:
            catt = Catagory.objects.get(id=idd)
            data = Add_job.objects.filter(catagory=catt)

        user = User.objects.get(id=request.user.id)
        sign = StudentUser.objects.get(user=user)
        data1 = Apply.objects.filter(sign=sign)
        li = []
        for i in data1:
            li.append(i.job.id)
        d = {'data': data, 'li': li, 'catag': caa}
        return render(request, 'job/catagorywise.html', d)


@login_required(login_url='/user-login/')
def job_detail(request, id):
    data = Add_job.objects.get(id=id)
    d = {'data': data}
    return render(request, 'job/jobdetail.html', d)


@login_required(login_url='/user-login/')
def apply_job(request, jid):
    error = ""
    user = User.objects.get(id=request.user.id)
    datausr = StudentUser.objects.get(user=user)
    today_date = date.today()
    jobb = Add_job.objects.get(id=jid)
    # startdate calculate
    s1 = jobb.start_date.day
    s2 = jobb.start_date.month
    s3 = jobb.start_date.year

    # enddate calculte

    e1 = jobb.end_date.day
    e2 = jobb.end_date.month
    e3 = jobb.end_date.year

    # toadydate calculation
    t1 = today_date.day
    t2 = today_date.month
    t3 = today_date.year

    # calculate num of days

    openn = s1 + (s2 * 30) + (s3 * 365)
    closedd = e1 + (e2 * 30) + (e3 * 365)
    todayy = t1 + (t2 * 30) + (t3 * 365)

    if openn > todayy:
        error = "notable"
    elif todayy > closedd:
        error = "closed"
    else:
        if request.method == 'POST':
            i = request.FILES['image']
            Apply.objects.create(image=i, sign=datausr, job=jobb)
            error = "able"
    d = {'error': error}
    return render(request, 'job/jobapplayresume.html', d)


@login_required(login_url='/user-login/')
def Change_Password(request):
    error = ""
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']

        usrr = User.objects.get(id=request.user.id)

        dec = usrr.check_password(o)
        if dec:
            if c == n:
                u = User.objects.get(username__exact=request.user.username)
                u.set_password(n)
                u.save()
                error = "yes"
            else:
                error = "not"
        else:
            error = "oldd"

    d = {'error': error}
    return render(request, 'job/userchangepassword.html', d)


def user_blogg(request):
    d = ""
    if request.method == "POST":
        nam = request.POST['uname']
        tit = request.POST['title']
        dat = request.POST['date']
        slg = request.POST['slug']
        img = request.FILES['image']
        stat = request.POST['status']
        cont = request.POST['content']
        z1 = request.user.id
        author = User.objects.get(id=z1)
        try:
            p1 = post.objects.create(title=tit, author=author, slug=slg, timeStamp=dat, thumbnail=img, status=stat,
                                     content=cont)
            p1.save()
            return redirect('/user-home/')
        except:
            messages.error(request, "there is something wrong in creating blog")

    x1 = request.user.id
    x2 = User.objects.get(id=x1)
    x3 = StudentUser.objects.get(user=x2)
    d = {'data': x3}

    return render(request, 'job/user-blog.html', d)


# companyy funactions
# def companylogin(request):
#     return render(request, 'job/company-login.html')

def blogg(request):
    d = ""
    if request.method == "POST":
        nam = request.POST['company']
        tit = request.POST['title']
        dat = request.POST['date']
        slg = request.POST['slug']
        img = request.FILES['image']
        stat = request.POST['status']
        cont = request.POST['content']
        z1 = request.user.id
        author = User.objects.get(id=z1)
        try:
            p1 = post.objects.create(title=tit, author=author, slug=slg, timeStamp=dat, thumbnail=img, status=stat,
                                     content=cont)
            p1.save()
            return redirect('/company-home/')
        except:
            messages.error(request, "there is something wrong in creating blog")

    x1 = request.user.id
    x2 = User.objects.get(id=x1)
    x3 = Recruiter.objects.get(user=x2)
    d = {'data': x3}

    return render(request, 'job/companyblog.html', d)


def companyregister(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['dzname']

        emal = request.POST['email']
        contact = request.POST['cnum']
        password1 = request.POST['pass']
        imge = request.FILES['photo']
        gen = request.POST['gender']
        comp = request.POST['cname']
        print("============================")
        print(fn)
        print(gen)
        print(comp)
        exist1 = User.objects.filter(username=emal)
        cn = Recruiter.objects.filter(company=comp)
        if exist1 or cn:
            error = "existss"
        else:
            try:
                user = User.objects.create_user(username=fn, email=emal, password=password1)
                Recruiter.objects.create(user=user, mobile=contact, image=imge, gender=gen, company=comp,
                                         status="null", type="recruiter")
                error = "no"
            except:
                error = "yes"

    dic = {'error': error}
    return render(request, 'job/company-register.html', dic)


def Company_Login(request):
    error = ""
    if request.user.is_authenticated:
        return redirect('/company-home/')
    if request.method == "POST":
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status != 'null':
                    login(request, user)
                    error = "yes"
                else:
                    error = "not"
            except:
                error = "no"
        else:
            error = "no"
    d = {'error': error}
    return render(request, 'job/company-login.html', d)


def recruiterlogout(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect('/')
    elif request.user.is_authenticated:
        logout(request)

        return redirect('/')

    return redirect('/')


def companyhome(request):
    if not request.user.is_authenticated:
        return redirect('/')
    elif request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        try:
            data = Recruiter.objects.get(user=user)
            uusr = User.objects.get(id=request.user.id)
            recr = Recruiter.objects.get(user=uusr)

            data = Add_job.objects.filter(recruiter=recr)
            return render(request, 'job/companies.html')
        except:
            return redirect('/')

    else:
        return redirect('/')


def add_job(request):
    catt = Catagory.objects.all()
   

    error = False
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        try:
            data = Recruiter.objects.get(user=user)
        except:
            return redirect('/')

        if data.type == "recruiter":
            if request.method == 'POST':
                c = request.POST['company']
                t = request.POST['title']
                s = request.POST['start_date']
                e = request.POST['end_date']
                de = request.POST['description']
                exp = request.POST['experience']
                sal = request.POST['salaryy']
                p = request.POST['position']
                loc = request.POST['loc']
                sk = request.POST['skills']
                cat = request.POST['jobcatago']
                i = request.FILES['image']
                tt = request.POST['tim']

                data1 = Recruiter.objects.get(company=c)
                gott = Catagory.objects.get(catagory_name=cat)
                Add_job.objects.create(recruiter=data1, title=t, start_date=s, end_date=e, description=de,
                                       experience=exp, catagory=gott, location=loc, position=p, timee=tt, image=i,
                                       skills=sk, salary=sal)
                error = True
        else:
            return redirect('/')
    else:
        return redirect('/')
    d = {'error': error, 'data': data, 'cat': catt}
    return render(request, 'job/addjobs.html', d)


def add_cat(request):
    error = ""
    if request.method == "POST":
        cnamm = request.POST['catagoryy1']
        Catagory.objects.create(catagory_name=cnamm)
        error = "no"
    d = {'error': error}
    return render(request, 'job/add-catagory.html', d)


def job_list(request):
    uusr = User.objects.get(id=request.user.id)
    recr = Recruiter.objects.get(user=uusr)

    data = Add_job.objects.filter(recruiter=recr)
    d = {'data': data}
    return render(request, 'job/job-list.html', d)


def job_edit(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

    error = ""
    xcat = Catagory.objects.all()
    # and and data.type =="recruiter"
    jobb = Add_job.objects.get(id=id)
    try:
        data = Recruiter.objects.get(user=user)
        if request.method == "POST":
            c = request.POST['company']
            t = request.POST['title']
            s = request.POST['start_date']
            e = request.POST['end_date']
            de = request.POST['description']
            exp = request.POST['experience']
            p = request.POST['position']
            loc = request.POST['location']
            sk = request.POST['skills']
            cat = request.POST['jobcatago']
            i = request.FILES['image']

            data1 = Recruiter.objects.get(company=c)
            gott = Catagory.objects.get(catagory_name=cat)
            jobb.recruiter.company = data1
            jobb.start_date = s
            jobb.end_date = e
            jobb.title = t
            jobb.position = p
            jobb.image = i
            jobb.description = de
            jobb.experience = exp
            jobb.catagory = gott
            jobb.location = loc
            jobb.skills = sk
            jobb.save()
            return redirect('/job-list/')

    except:
        return redirect('/')

    d = {'data': jobb, 'cat': xcat}
    return render(request, 'job/editjob.html', d)


def deljob(request, id):
    if request.user.is_authenticated:
        usrr = User.objects.get(id=request.user.id)
        try:
            rec = Recruiter.objects.get(user=usrr)
        except:
            return redirect('/')
    else:
        return redirect('/')
    try:
        usr = Add_job.objects.get(id=id)
        usr.delete()
        return redirect('/job-list/')
    except:
        return redirect('/')


def view_apply(request):
    try:
        user = User.objects.get(id=request.user.id)
        sign = Recruiter.objects.get(user=user)
    except:
        return redirect('/')
    data = Apply.objects.all()
    li = []
    for i in data:
        li.append(i.job.id)
    d = {'data': data, 'li': li, 'sign': sign}
    return render(request, 'job/view_apply.html', d)


def RecruiterChange_Password(request):
    error = ""
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']

        ur = Recruiter.objects.get(user=request.user.id)
        usrr = User.objects.get(id=ur.id)

        dec = usrr.check_password(o)
        if dec:
            if c == n:
                u = User.objects.get(username__exact=request.user.username)
                u.set_password(n)
                u.save()
                error = "yes"
            else:
                error = "not"
        else:
            error = "oldd"
    d = {'error': error}
    return render(request, 'job/companychangepass.html', d)


def CEdit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Recruiter.objects.get(user=user)
    if request.method == 'POST':
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        m = request.POST['mobile']
        try:
            g = request.POST['gender']
            pro.gender = g
            pro.save()
        except:
            pass
        try:
            fi = request.FILES['image']
            pro.image = fi
            pro.save()
        except:
            pass
        pro.user.username = u
        pro.user.last_name = l
        pro.user.email = e
        pro.mobile = m
        pro.save()
        pro.user.save()
        error = True
    d = {'error': error, 'pro': pro}
    return render(request, 'job/company_profile.html', d)


# admin functions


def adminlogin(request):
    if request.user.is_authenticated:
        return redirect('/admin-home/')
    else:
        error = ""
        if request.method == "POST":
            u = request.POST['uname']
            p = request.POST['pwd']
            user = authenticate(username=u, password=p)
            print("=====================")
            print(user)
            try:
                if user.is_staff:
                    login(request, user)
                    request.session['userr'] = u
                    error = "yes"
                else:
                    error = "no"
            except:
                error = "not"
        d = {'error': error}
        return render(request, 'job/admin_login.html', d)


def admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('/admin-login/')
    elif request.user.is_staff:
        comp = Recruiter.objects.all().count()
        job = Add_job.objects.all().count()
        usr = StudentUser.objects.all().count()
        d = {'company': comp, 'jobs': job, 'user': usr}
        return render(request, 'job/admin-home.html')
    else:
        return redirect('/')


def admin_Home1(request):
    if not request.user.is_authenticated:
        return redirect('/admin-login/')
    elif request.user.is_staff:
        comp = Recruiter.objects.all().count()
        job = Add_job.objects.all().count()
        usr = StudentUser.objects.all().count()
        d = {'company': comp, 'jobs': job, 'user': usr}
        return render(request, 'job/admin-home1.html', d)
    else:
        return redirect('/')


def view_newrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('/admin-login/')
    else:

        data = Recruiter.pendingrec.all()
        d = {'d': data}
        print("===========")
        print(data)
        return render(request, 'job/newcompany.html', d)


def acceptedcompanies(request):
    if not request.user.is_staff:
        return redirect('/admin-login/')
    else:

        data = Recruiter.acceptcompany.all()
        d = {'d': data}
        print("===========")
        print(data)
        return render(request, 'job/newcompany.html', d)


def Rejected_companies(request):
    if not request.user.is_staff:
        return redirect('/admin-login/')
    else:

        data = Recruiter.rejcomp.all()
        d = {'d': data}
        print("===========")
        print(data)
        return render(request, 'job/newcompany.html', d)


def View_User(request):
    usr = StudentUser.objects.filter(type="student")
    d = {'data': usr}
    return render(request, 'job/viewuser.html', d)


def del_User(request, id):
    if request.user.is_staff:
        dell = User.objects.filter(id=id)
        # print(dell)
        dell.delete()

    else:
        return redirect('/')

    return redirect('/viewuser/')


def assignstatus(request, id):
    submit = Recruiter.objects.get(id=id)

    error = False
    if request.method == "POST":
        a = request.POST['status']
        submit.status = a
        submit.save()
        error = "yes"
    d = {'error': error, 'data': submit}
    return render(request, 'job/assignstatus.html', d)


def Del_Recruiter(request, id):
    error = ""
    if request.user.is_staff:
        delu = User.objects.filter(id=id)
        delu.delete()
        error = "no"
    else:
        error = "yes"

    return redirect('/company-accepted/')


def Reject_Recruiter(request, id):
    error = ""
    delu = Recruiter.objects.get(id=id)
    if request.user.is_staff:

        delu.status = "Rejected"
        delu.save()
        error = "nott"
    else:
        error = "yes"
    d = {'error': error, 'data': delu}
    return render(request, 'job/assignstatus.html', d)


def admin_blogg(request):
    d = ""
    if request.method == "POST":
        nam = request.POST['uname']
        tit = request.POST['title']
        dat = request.POST['date']
        slg = request.POST['slug']
        img = request.FILES['image']
        stat = request.POST['status']
        cont = request.POST['content']
        z1 = request.user.id
        author = User.objects.get(id=z1)
        try:
            p1 = post.objects.create(title=tit, author=author, slug=slg, timeStamp=dat, thumbnail=img, status=stat,
                                     content=cont)
            p1.save()
            return redirect('/admin-home1/')
        except:
            messages.error(request, "there is something wrong in creating blog")

    x1 = request.user.id
    x2 = User.objects.get(id=x1)

    d = {'data': x2}

    return render(request, 'job/admin-blog.html', d)


def adminblog_list(request):
    if request.user.is_staff:
        x1 = request.user.id
        x2 = User.objects.get(id=x1)
        datap = post.objects.filter(author=x2)
        d = {'data': datap}
        return render(request, 'job/admin-bloglist.html', d)
    else:
        redirect('/')


def delblog(request, id):
    if request.user.is_staff:
        x = post.objects.get(post_id=id)
        x.delete()
        return redirect('/admin-home1/')
    else:
        return redirect('/')


def cblog_list(request):
    if request.user.is_authenticated:
        x1 = request.user.id
        x2 = User.objects.get(id=x1)
        datap = post.objects.filter(author=x2)
        d = {'data': datap}
        return render(request, 'job/comp-bloglist.html', d)
    else:
        redirect('/')


def cdelblog(request, id):
    if request.user.is_authenticated:
        x = post.objects.get(post_id=id)
        x.delete()
        return redirect('/company-home/')
    else:
        return redirect('/')


def uublog_list(request):
    if request.user.is_authenticated:
        x1 = request.user.id
        x2 = User.objects.get(id=x1)
        datap = post.objects.filter(author=x2)
        d = {'data': datap}
        return render(request, 'job/user-bloglist.html', d)
    else:
        redirect('/')


def uudelblog(request, id):
    if request.user.is_authenticated:
        x = post.objects.get(post_id=id)
        x.delete()
        return redirect('/user-home/')
    else:
        return redirect('/')


def receiver1(request):
    if request.method == "POST":
        ema = request.POST['emm']
        unam = request.POST['unam']
        titl = request.POST['tit']

        print(ema)

    d = {'data3': ema, 'unam': unam, 'title': titl}
    return render(request, 'job/contact11.html', d)


def mailsnd(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        uname = request.POST['usernamee']
        title = request.POST['titlee']
        dat = request.POST['datee']
        to_email = request.POST['email']

        x = Recruiter.objects.get(user=request.user)
        print(x)
        if subject and message and to_email:
            try:
                ctx = {
                    'company': x,
                    'datex': dat,
                    'user': uname,
                    'title': title,
                    'emaill': to_email,
                    'message': message,
                }
                message = get_template('job/mail-template.html').render(ctx)
                msg = EmailMessage(
                    subject,
                    message,
                    'settings.EMAIL_HOST_USER',
                    [to_email],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                print("Mail successfully sent")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/view_apply/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')


def mailsndfooter(request):
    if not request.user.is_authenticated:
        return redirect('/user-login/')
    if request.method == "POST":
        subject = "Footer user Query"
        message = request.POST['message']
        to_email = request.user.email
        message = message + """ 
        
        
        
        
Sending user is 
""" + to_email
        if subject and message and to_email:
            try:
                send_mail(subject, message, to_email, ['M.collections78600@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')
