from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
import time
import datetime
import requests
from datetime import date
from django.core import serializers
import json
from django.core.files.storage import FileSystemStorage
import pytz
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from . decorators import logged_inn2, logged_inn3, logged_inn4
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
import tkinter as tk
from tkinter import messagebox
import shutil, os
from tkinter import *
from googletrans import Translator
from gtts import gTTS
from django.core.mail import send_mail

from learning import settings
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))
from geopy.geocoders import Nominatim
import cv2, os
from PIL import Image
import numpy as np
from django.utils.timezone import make_aware



def home(request):
    sdd = Category.objects.all()
    sd = []
    count = 0
    for i in sdd:
        if i.Category_title not in sd:
            sd.append(i.Category_title)
            count += 1
    return render(request,'tpp/index.html',{'sd':sd,'count':count,'sdd':sdd})


def logout(request):
    auth.logout(request)
    return redirect('home')


def reg_msg(request):
    messages.success(request, 'Please register to access course contents')
    return redirect('home')


def contact(request):
    m = Registration.objects.get(User_role = 'admin')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        t_a = request.POST.get('t_a')
        g = Guest_messages()
        g.Name = name
        g.Email = email
        g.Message_content = t_a
        g.save()
        messages.success(request, 'Message sent successfully. You will get reply through email.')
        return redirect('home')
    return render(request,'contact.html')


def news(request):
    page = requests.get('https://www.indiatoday.in/education-today')
    soup = BeautifulSoup(page.content,'html.parser')
    week = soup.find(class_ = 'story__grid')
    #wm = week.find(class_ = 'itg-listing')
    w = week.find_all('h2')
    ww = []
    lnk = []
    for x in w:
        k = x.a
        lnk.append(k['href'])
        ww.append(x.get_text())
    jhj = zip(ww,lnk)
    x = datetime.datetime.now()
    return render(request,'news.html',{'ww':jhj,'x':x})


def about(request):
    if Registration.objects.filter(User_role = 'admin').exists():
        pass
    else:
        messages.success(request,'Admin has to register. Then only about page is visible.')
        return redirect('home')
    df = Registration.objects.get(User_role = 'admin')
    gt = Registration.objects.filter(User_role = 'teacher')
    return render(request,'about.html',{'df':df,'gt':gt})


def register_st(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if w.user.email == email and w.User_role == 'student':
                messages.success(request, 'You have already registered. Please login')
                return redirect('register_st')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)

        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('register_st')

        user = User.objects.create_user(username=user_name, email=email, password=psw, first_name=first_name,last_name=last_name)
        user.save()

        reg = Registration()
        reg.Password = psw
        reg.Image = photo
        reg.User_role = 'student'
        reg.user = user
        reg.save()
        messages.success(request, 'You have successfully registered as student')
        return redirect('home')
    else:
        return render(request, 'register_student.html')


def register_tr(request):
    wtek = str(3)
    jej = 2000
    order_currency = 'INR'
    callback_url = 'http://' + str(get_current_site(request)) + "/pay_teacher_razor"
    notes = {'order-type': "Teacher registration fee", 'key': 'value'}
    razorpay_order = razorpay_client.order.create(
        dict(amount=jej * 100, currency=order_currency, notes=notes, receipt=wtek, payment_capture='0'))
    order_id = razorpay_order['id']
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        '''if float(fee) < 2000:
            messages.success(request, 'Please pay full registration fee')
            return redirect('register_tr')'''
        psw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('register_tr')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('register_tr')

        user = User.objects.create_user(username=user_name, email=email, password=psw, first_name=first_name,last_name=last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Qualification = qual
        t.Introduction_brief = intro
        t.Image = photo
        #t.Registration_fee = fee
        t.User_role = 'teacher_blocked'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered. Please wait for approval from admin to login')
        return redirect('home')
    else:
        return render(request, 'register_teacher.html',{'order_id': order_id, 'final_price': jej, 'razorpay_merchant_id': settings.razorpay_id,'callback_url': callback_url})


@csrf_exempt
def pay_teacher_razor(request):
    return HttpResponse('Please note that payment gateway will work only after verification of website. \
    This is a demo payment demonstration. Please go back and enter fee in input box and press "submit" button to proceed')


def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('home')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('adminn')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('adminn')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Image = photo
        t.User_role = 'admin'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
    else:
        return render(request, 'register_admin.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return render(request, 'login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, Password = password).exists():
            logs = Registration.objects.filter(user = user, Password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                teacher_email = value.user.email
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    cm = Registration.objects.get(id=request.session['logg'])
                    g = Enrollment.objects.filter(enrol_tea=cm)
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id=nwn)
                        df = Course.objects.filter(cou_reg=mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('admin_home')

                elif usertype == 'teacher':
                    request.session['logg'] = user_id
                    request.session['teacher'] = teacher_email
                    cm = Registration.objects.get(id = request.session['logg'])
                    g = Enrollment.objects.filter(enrol_tea = cm)
                    count = 0
                    for i in g:
                        count += 1
                    cm.Num_of_enrolled_students = count
                    mb = Feedback.objects.filter(Feed_tea_reg = cm)
                    cnn = 0
                    avs = []
                    for t in mb:
                        cnn += 1
                        avs.append(t.Rating_score)
                    aa = avs.count(5)
                    bb = avs.count(4)
                    cc = avs.count(3)
                    dd = avs.count(2)
                    ee = avs.count(1)
                    ff = [aa,bb,cc,dd,ee]
                    gg = max(ff)
                    if int(gg) == int(aa):
                        cm.Average_review_rating = 5
                    if int(gg) == int(bb):
                        cm.Average_review_rating = 4
                    if int(gg) == int(cc):
                        cm.Average_review_rating = 3
                    if int(gg) == int(dd):
                        cm.Average_review_rating = 2
                    if int(gg) == int(ee):
                        cm.Average_review_rating = 1
                    cm.Num_of_reviews = cnn
                    cm.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id = nwn)
                        df = Course.objects.filter(cou_reg = mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('teacher_home')

                elif usertype == 'student':
                    request.session['logg'] = user_id
                    g = Enrollment.objects.all()
                    mhp = Registration.objects.get(id = request.session['logg'])
                    dt = Enrollment.objects.filter(enrol_reg = mhp)

                    ggpp = []
                    for t in dt:
                        ksk = int(t.enrol_cou.id)
                        ggpp.append(ksk)

                    dgf = Course.objects.filter(id__in = ggpp)
                    cou_cmpltd = 0
                    for e in dgf:
                        mbt = 0
                        pas = 0
                        pas1 = 4
                        hdc = Chapter.objects.filter(cha_cou = e)
                        for t in hdc:
                            hdc1 = Content.objects.filter(cont_cha = t)
                            for c in hdc1:
                                if Learning_progress.objects.filter(Learn_p_reg = mhp, Learn_p_cnt = c, Status = 'C').exists():
                                    pas += 1
                            pas1 = Content.objects.filter(cont_cha = t).count()
                            if pas == pas1:
                                mbt += 1

                        ch_cnts = Chapter.objects.filter(cha_cou = e).count()

                        if ch_cnts == mbt:
                            cou_cmpltd += 1


                    mhp.Num_of_courses_completed = cou_cmpltd

                    pas = Learning_progress.objects.filter(Learn_p_reg = mhp, Status = 'P')
                    ggpp = []
                    for t in pas:
                        ksk = int(t.Learn_p_cnt.cont_cha.cha_cou.id)
                        ggpp.append(ksk)
                    dgf = Course.objects.filter(id__in=ggpp).count()

                    mhp.Num_of_courses_enrolled = dgf
                    mhp.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id=nwn)
                        df = Course.objects.filter(cou_reg = mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('student_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required
@logged_inn2
def admin_home(request):
    return render(request, "admin_home.html")


@login_required
@logged_inn3
def student_home(request):
    return render(request, "student_home.html")


@login_required
@logged_inn4
def teacher_home(request):
    seww = Registration.objects.get(id = request.session['logg'])
    stzz1 = Enrollment.objects.filter(enrol_tea = seww, notify='new')
    count = 0
    for e in stzz1:
        count += 1
    return render(request, 'teacher_home.html', {'count': count,'seww':seww})


def add_blog(request):
    if request.method == 'POST':
        nam = request.POST.get('nam')
        c_b = request.POST.get('c_b')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        b = Blogs()
        b.Name = nam
        b.Blog_content = c_b
        b.Image = photo
        b.Approval_status = 'Rejected'
        b.save()
        messages.success(request, 'Blog added successfully. Please wait for approval')
        return redirect('home')
    return render(request,'add_blog.html')


def blogs_admin(request):
    dm = Blogs.objects.all()
    return render(request,'blogs_admin.html',{'dm':dm})


def blog_approves(request,id):
    sas = Blogs.objects.get(id=id)
    sas.Approval_status = 'Approved'
    sas.save()
    return redirect('blogs_admin')


def blog_rejects(request, id):
    sas = Blogs.objects.get(id=id)
    sas.Approval_status = 'Rejected'
    sas.save()
    return redirect('blogs_admin')


def blog_delete(request, id):
    Blogs.objects.get(id=id).delete()
    return redirect('blogs_admin')


def view_blog(request):
    dc = Blogs.objects.filter(Approval_status = 'Approved')
    return render(request,'display_blog.html',{'dc':dc})


def update_pr_tr(request):
    bb = Registration.objects.get(id = request.session['logg'])
    rfy = bb.user.pk
    um = User.objects.get(id = rfy)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('update_pr_tr')


        passwords = make_password(pasw)
        u = User.objects.get(id = rfy)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.first_name = f_name
        u.last_name = l_name
        u.save()

        user = auth.authenticate(username = user_name, password = pasw)
        auth.login(request, user)


        b = bb.id
        m = int(b)
        request.session['logg'] = m

        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
    return render(request, 'update_pr_tr.html', {'bb': bb,'um':um})


def upl_cer(request):
    bc = Enrollment.objects.filter(Course_completion_status = 'Completed')
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        stu_id = int(stu_id)
        mrt = Enrollment.objects.get(id = stu_id)
        cert = request.FILES['cert']
        fs = FileSystemStorage()
        fs.save(cert.name,cert)
        if mrt.Certificate != '':
            messages.success(request, 'Please delete old certificate of student')
            return redirect('admin_home')
        mrt.Certificate = cert
        mrt.save()
        messages.success(request, 'Certificate uploaded successfully')
        return redirect('admin_home')

    return render(request,'upload_cert.html',{'bc':bc})


def block(request):
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request,'block.html',{'t_reg':t_reg,'s_reg':s_reg})


def blocks(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher_blocked'
    klk.save()
    return redirect('block')


def blocks1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student_blocked'
    klk.save()
    return redirect('block')


def allows(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher'
    klk.save()
    return redirect('block')


def allows1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student'
    klk.save()
    return redirect('block')


def feedbak(request):
    se = Feedback.objects.all()
    return render(request,'feedbak.html',{'se':se})


def delete_feedback(request, id):
    Feedback.objects.get(id=id).delete()
    return redirect('feedbak')


def m_m(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request,'message.html',{'bb':bb})


def del_msg_admin(request,id):
    Messages.objects.get(id = id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('m_m')


def reply_msg_admin(request,id):
    pa = Messages.objects.get(id = id)
    toto = int(pa.From_reg.id)
    p_to = Registration.objects.get(id = toto)
    p = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Message_content = msg_cont
        pa1.From_reg = p
        pa1.To_reg = p_to
        pa1.save()
        messages.success(request, 'Message reply successful')
        return redirect('m_m')
    return render(request,'reply_msg_admin.html',{'pa':pa})


def sent_msg_admin(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = int(to_em)
        reg_to = Registration.objects.get(id = ddp)
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Message_content = msg_cont
        nm.From_reg = p
        nm.To_reg = reg_to
        nm.save()
        messages.success(request, 'Message sent successfully')
        return redirect('m_m')
    return render(request,'sent_msg_admin.html',{'kk':kk})


def g_m(request):
    bb = Guest_messages.objects.all()
    return render(request,'guest_message.html',{'bb':bb})


def delete_g_msg(request,id):
    Guest_messages.objects.get(id=id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('g_m')


def reply_g_msg(request, id):
    yt = Guest_messages.objects.get(id = id)
    if request.method == 'POST':
        email = "devuzzdevika2@gmail.com"
        t_a = request.POST.get('t_a')
        emk = str(yt.Email)
        send_mail('Message reply from elearn website', t_a, email, [emk], fail_silently=False)
        redd = '/reply_g_msg/'+str(yt.id)
        messages.success(request, 'Email reply to guest done successfully')
        return redirect(redd)
    return render(request,'reply_g_msg.html',{'yt':yt})


def subject_ad(request):
   dd = Subject.objects.all()
   gt = Registration.objects.all()
   sub_nam = []
   cou_nam = []
   tea_em = []
   tea_fn = []
   tea_ln = []
   cou_brf = []
   c_d = []
   c_n = []
   c_f = []
   lan = []
   c_id = []
   for i in dd:
       sub_nam.append(i.Subject_title)
       cou_nam.append(i.Course_title)
       cou_brf.append(i.Course_brief)
       c_d.append(i.Course_duration)
       c_n.append(i.Num_of_chapters)
       c_f.append(i.Course_fee)
       lan.append(i.Language)
       c_id.append(i.id)
       for t in gt:
           if t == i.Sub_reg:
               tea_em.append(t.Email)
               tea_fn.append(t.First_name)
               tea_ln.append(t.Last_name)
   lenn = len(sub_nam)
   for z in range(lenn):
       kpk = len(sub_nam)
       r = int(z)
       r += 1
       try:
           a = sub_nam[z]
           b = cou_nam[z]
           c = tea_em[z]
       except:
           break

       for k in range(lenn):
           if int(r) >= int(kpk):
               continue
           try:
               if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c:
                   del sub_nam[r]
                   del cou_nam[r]
                   del tea_em[r]
                   del tea_fn[r]
                   del tea_ln[r]
                   del cou_brf[r]
                   del c_d[r]
                   del c_n[r]
                   del c_f[r]
                   del lan[r]
                   del c_id[r]
                   r -= 1
               r += 1
           except:
               break
   grg = zip(sub_nam,cou_nam,tea_em,tea_fn,tea_ln,cou_brf,c_d,c_n,c_f,lan,c_id)
   return render(request,'sub_ad.html',{'grg':grg})


def edit_subject1(request, id, idd, idt, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    ftf = Registration.objects.get(Email = idt)
    gh1 = Subject.objects.filter(Subject_title = id, Course_title = idd, Sub_reg = ftf)
    gh = Subject.objects.get(id = pkm)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        n_c = request.POST.get('n_c')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        for k in gh1:
            k.Subject_title = sub
            k.Course_title = cou
            k.Course_brief = c_b
            k.Course_duration = c_d
            k.Num_of_chapters = n_c
            k.Course_fee  = c_f
            k.Language  = lan
            k.save()
        messages.success(request, 'Subject edited successfully')
        return redirect('subject_ad')
    return render(request,'edit_subject1.html',{'gh':gh,'ftf':ftf})


def delete_subject1(request, id, idd, idt):
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    ftf = Registration.objects.get(Email=idt)
    Subject.objects.filter(Subject_title=id, Course_title=idd, Sub_reg=ftf).delete()
    messages.success(request, 'Subject deleted successfully')
    return redirect('subject_ad')


def chapter_ad(request):
    dd = Subject.objects.all()
    gt = Registration.objects.all()
    sub_nam = []
    cou_nam = []
    ch_tit = []
    n_o_a = []
    tea_em = []
    tea_fn = []
    tea_ln = []
    c_id = []
    for i in dd:
        sub_nam.append(i.Subject_title)
        cou_nam.append(i.Course_title)
        ch_tit.append(i.Chapter_title)
        n_o_a.append(i.Num_of_assignments)
        c_id.append(i.id)
        for t in gt:
            if t == i.Sub_reg:
                tea_em.append(t.Email)
                tea_fn.append(t.First_name)
                tea_ln.append(t.Last_name)
    lenn = len(sub_nam)
    for z in range(lenn):
        kpk = len(sub_nam)
        r = int(z)
        r += 1
        try:
            a = sub_nam[z]
            b = cou_nam[z]
            c = tea_em[z]
            d = ch_tit[z]
        except:
            break
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                    del sub_nam[r]
                    del cou_nam[r]
                    del ch_tit[r]
                    del n_o_a[r]
                    del tea_em[r]
                    del tea_fn[r]
                    del tea_ln[r]
                    del c_id[r]
                    r -= 1
                r += 1
            except:
                break
    grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
    return render(request, 'chap_ad.html', {'grg1': grg1})


def edit_chapter1(request, id, idd, idt, idk, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    idk = str(idk)
    ftf = Registration.objects.get(Email=idk)
    gh1 = Subject.objects.filter(Subject_title=id, Course_title=idd, Chapter_title = idt, Sub_reg=ftf)
    gh = Subject.objects.get(id=pkm)

    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        for k in gh1:
            k.Subject_title = sub
            k.Course_title = cou
            k.Chapter_title = c_tt
            k.Num_of_assignments = n_s
            k.save()
        messages.success(request, 'Chapter edited successfully')
        return redirect('chapter_ad')
    return render(request, 'edit_chapter1.html', {'gh': gh, 'ftf': ftf})


def delete_chapter1(request, id, idd, idt, idk):
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    idk = str(idk)
    ftf = Registration.objects.get(Email=idk)
    Subject.objects.filter(Subject_title=id, Course_title=idd, Chapter_title=idt, Sub_reg=ftf).delete()
    messages.success(request, 'Chapter deleted successfully')
    return redirect('chapter_ad')


def ch_co_ad(request):
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    return render(request, 'cont_ad.html', {'gt':gt,'dm':dm})


def edit_content1(request, id):
    gh1 = Subject.objects.get(id=id)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_n1 = request.POST.get('c_n')
        s = request.POST.get('s')
        time = request.POST.get('time')
        s1 = request.POST.get('s1')
        cont_typ = request.POST.get('cont_typ')
        textt = request.POST.get('textt')
        gh1.Subject_title = sub
        gh1.Course_title = cou
        gh1.Chapter_title = c_n1
        gh1.Chapter_text_content = textt
        if cont_typ == 1:
            gh1.Chapter_Content_type = 'Image'
        if cont_typ == 2:
            gh1.Chapter_Content_type = 'Text'
        if cont_typ == 3:
            gh1.Chapter_Content_type = 'Video'
        gh1.Chapter_Content_Is_mandatory  = s
        gh1.Chapter_Content_Time_required_in_sec  = time
        gh1.Chapter_Content_Is_open_for_free  = s1
        gh1.save()
        messages.success(request, 'Chapter content edited successfully')
        return redirect('ch_co_ad')
    return render(request, 'edit_content1.html', {'gh1': gh1})


def delete_content1(request,id):
    Subject.objects.get(id=id).delete()
    messages.success(request, 'Chapter content deleted successfully')
    return redirect('ch_co_ad')


def st_pr(request):
    vc = Registration.objects.get(id = request.session['logg'])
    dd = Learning_progress.objects.filter(Learn_p_tea_reg = vc)
    return render(request,'student_progress.html',{'dd':dd})


def ch_p11(request):
    th = Registration.objects.get(id = request.session['logg'])
    trp = th.user.pk
    u = User.objects.get(id = trp)
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        passwords = make_password(new_pass)
        u.password = passwords
        u.save()

        th.Password = new_pass
        th.save()
        messages.success(request, 'Password changed successfully. Login again with new password.')
        return redirect('logout')
    return render(request, 'change_pass1.html', {'th': th})


def cat_admin(request):
    mkk = Category.objects.all()
    return render(request,'cat_admin.html',{'mkk':mkk})


def add_cat_admin(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        imgg = request.FILES['imgg']
        fs = FileSystemStorage()
        fs.save(imgg.name, imgg)
        gh = Category()
        gh.Category_title = cat
        gh.Image = imgg
        gh.save()
        messages.success(request, 'Course category added successfully')
        return redirect('cat_admin')
    return render(request,'add_cat_admin.html')


def edit_cat_admin(request, id):
    gh = Category.objects.get(id = id)
    if request.method == 'POST':
        try:
            imgg = request.FILES['imgg']
            fs = FileSystemStorage()
            fs.save(imgg.name,imgg)
            cat = request.POST.get('cat')
            gh.Category_title = cat
            gh.Image = imgg
            gh.save()
        except:
            imgg1 = request.POST.get('imgg1')
            cat = request.POST.get('cat')
            gh.Category_title = cat
            gh.Image = imgg1
            gh.save()
        messages.success(request, 'Course category edited successfully')
        return redirect('cat_admin')
    return render(request, 'edit_cat_admin.html', {'gh': gh})


def delete_cat_admin(request, id):
    Category.objects.get(id = id).delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('cat_admin')


def course_tr(request):
    dd = Course.objects.filter(cou_reg = request.session['logg'])
    return render(request,'course_tr.html',{'dd':dd})


def edit_course_tr(request, id):
    mkm = Category.objects.all()
    gh = Course.objects.get(id = id)
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat = int(cat)
        yky = Category.objects.get(id = cat)
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        gh.Course_title = cou
        gh.Course_brief = c_b
        gh.Course_duration = c_d
        gh.Course_fee  = c_f
        gh.Language  = lan
        gh.cou_cat = yky
        gh.save()
        messages.success(request, 'Course edited successfully')
        return redirect('course_tr')
    return render(request,'edit_course_tr.html',{'gh':gh,'mkm':mkm})


def delete_course_tr(request, id):
    Course.objects.get(id = id).delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('course_tr')


def add_course_tr(request):
    hrb = Registration.objects.get(id = request.session['logg'])
    mkm = Category.objects.all()
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat = int(cat)
        bbt = Category.objects.get(id = cat)
        cou_tit = request.POST.get('cou_tit')
        c_b1 = request.POST.get('c_b1')
        c_d1 = request.POST.get('c_d1')
        c_f1 = request.POST.get('c_f1')
        lang = request.POST.get('lang')

        if Course.objects.filter(cou_reg = hrb, Course_title = cou_tit).exists():
            messages.success(request, 'Course already exists')
            return redirect('course_tr')

        cdt = Course()
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_b1
        cdt.Course_duration = c_d1
        cdt.Course_fee = c_f1
        cdt.Language = lang
        cdt.cou_reg = hrb
        cdt.cou_cat = bbt
        cdt.save()

        cou_st_date = request.POST.get('cou_st_date')
        cou_end_date = request.POST.get('cou_end_date')

        cmk = Course_st_stop()
        cmk.start_date = cou_st_date
        cmk.end_date = cou_end_date
        cmk.cou_st_stop_cou = cdt
        cmk.save()

        messages.success(request, 'Course added successfully')
        return redirect('course_tr')
    return render(request,'add_course_tr.html',{'mkm':mkm})


def chapter_tr(request, id):
    id = int(id)
    request.session['teacher_course'] = id
    hh = Chapter.objects.filter(cha_cou = id)
    return render(request, 'chap_tr.html', {'hh': hh})


def edit_chapter_tr(request, id):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    gh = Chapter.objects.get(id = id)
    if request.method == 'POST':
        c_tt = request.POST.get('c_tt')
        gh.Chapter_title = c_tt
        gh.save()
        messages.success(request, 'Chapter edited successfully')
        redd = '/chapter_tr/'+str(kkp.id)
        return redirect(redd)
    return render(request,'edit_chapter_tr.html',{'gh':gh,'kkp':kkp})


def delete_chapter(request, id):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    Chapter.objects.get(id = id).delete()
    messages.success(request, 'Chapter deleted successfully')
    redd = '/chapter_tr/' + str(kkp.id)
    return redirect(redd)


def add_chapter(request):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    if request.method == 'POST':
        c_tt = request.POST.get('c_tt')
        if Chapter.objects.filter(cha_cou = kkp, Chapter_title = c_tt).exists():
            messages.success(request, 'Chapter already exists')
            redd = '/chapter_tr/' + str(kkp.id)
            return redirect(redd)

        cdt = Chapter()
        cdt.Chapter_title = c_tt
        cdt.cha_cou = kkp
        cdt.save()

        messages.success(request, 'Chapter added successfully')
        redd = '/chapter_tr/' + str(kkp.id)
        return redirect(redd)
    return render(request,'add_chapter.html',{'kkp':kkp})


def ch_co_tr(request, id):
    id = int(id)
    request.session['teacher_chapter'] = id
    idm = request.session['teacher_course']
    idm = int(idm)
    mm1 = Content.objects.filter(cont_cha = id)
    return render(request, 'cont_tr.html', {'mm1': mm1,'idm':idm})


def edit_content(request, id):
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    tt_chapt = Chapter.objects.get(id = tt_chapt1)
    gh = Content.objects.get(id = id)
    if request.method == 'POST':
        try:
            c_t = request.POST.get('c_t')
            up_cont = request.FILES['up_cont']
            upp = str(up_cont)
            imm = ['.jpeg','.jpg','.png']
            vid = ['.mov','.mp4','.wmv','.avi','.avchd','.flv','.f4v','.swf','.mkv','.webm','.mpeg4']
            nbg = 0

            for i in imm:
                if upp.endswith(i):
                    nbg += 1
                    gh.Chapter_Content_type = 'Image'

            for i in vid:
                if upp.endswith(i):
                    nbg += 1
                    gh.Chapter_Content_type = 'Video'

            if nbg == 0:
                gh.Chapter_Content_type = 'File'

            fs = FileSystemStorage()
            fs.save(up_cont.name, up_cont)

            gh.Chapter_Content = up_cont
            gh.Chapter_text_content = c_t
            gh.save()
            redd = '/ch_co_tr/'+str(tt_chapt1)
            messages.success(request, 'Chapter content edited successfully')
            return redirect(redd)

        except:
            c_t = request.POST.get('c_t')
            u_con = request.POST.get('u_con')
            u_con_typ = request.POST.get('u_con_typ')
            gh.Chapter_Content = u_con
            gh.Chapter_text_content = c_t
            gh.Chapter_Content_type = u_con_typ
            gh.save()
            redd = '/ch_co_tr/' + str(tt_chapt1)
            messages.success(request, 'Chapter content edited successfully')
            return redirect(redd)
    return render(request, 'edit_content.html', {'gh': gh,'tt_chapt':tt_chapt})


def delete_content(request, id):
    Content.objects.get(id = id).delete()
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    redd = '/ch_co_tr/' + str(tt_chapt1)
    messages.success(request, 'Chapter content deleted successfully')
    return redirect(redd)


def add_ch_con(request):
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    tt_chapt = Chapter.objects.get(id=tt_chapt1)
    if request.method == 'POST':
        c_t = request.POST.get('c_t')
        up_cont = request.FILES['up_cont']
        fs = FileSystemStorage()
        fs.save(up_cont.name, up_cont)

        upp = str(up_cont)
        imm = ['.jpeg', '.jpg', '.png']
        vid = ['.mov', '.mp4', '.wmv', '.avi', '.avchd', '.flv', '.f4v', '.swf', '.mkv', '.webm', '.mpeg4']

        cdt = Content()
        nbg = 0
        for i in imm:
            if upp.endswith(i):
                nbg += 1
                cdt.Chapter_Content_type = 'Image'

        for i in vid:
            if upp.endswith(i):
                nbg += 1
                cdt.Chapter_Content_type = 'Video'

        if nbg == 0:
            cdt.Chapter_Content_type = 'File'

        cdt.Chapter_Content = up_cont
        cdt.Chapter_text_content = c_t
        cdt.cont_cha = tt_chapt
        cdt.save()
        redd = '/ch_co_tr/' + str(tt_chapt1)
        messages.success(request, 'Chapter content added successfully')
        return redirect(redd)
    return render(request,'add_chapter_content.html',{'tt_chapt':tt_chapt})


def notiffy(request):
    stzz = Enrollment.objects.filter(enrol_tea = request.session['logg'])
    for y in stzz:
        if y.notify == 'new':
            y.notify = None
            y.save()
    return redirect('teacher_home')


def stu_buk_acc(request):
    stzz = Enrollment.objects.filter(enrol_tea = request.session['logg'])
    return render(request,'stu_buk_acc.html',{'stzz':stzz})


def stu_delete(request, id):
    Enrollment.objects.get(id = id).delete()
    messages.success(request, 'Enrolled student deleted successfully')
    return redirect('stu_buk_acc')


def stu_accept(request, id):
    sas = Enrollment.objects.get(id = id)
    sas.Teacher_response = 'Accepted'
    sas.save()
    return redirect('stu_buk_acc')


def stu_reject(request, id):
    sas = Enrollment.objects.get(id=id)
    sas.Teacher_response = 'Rejected'
    sas.save()
    return redirect('stu_buk_acc')


def sched_test_t1(request):
    kk = Category.objects.all()
    return render(request,'sched_test_t1.html',{'kk':kk})


def sched_ex_cat(request):
    ghg = request.POST.get('catt')
    ghg = int(ghg)
    kk = Category.objects.get(id = ghg)
    dkd = Course.objects.filter(cou_cat = kk)
    return render(request, 'sched_test_t2.html', {'dkd': dkd})


def sched_test(request):
    couu = request.POST.get('couu')
    couu = int(couu)
    jdj = Course.objects.get(id = couu)
    sew = Registration.objects.get(id = request.session['logg'])
    stz = Enrollment.objects.filter(enrol_tea = sew, Teacher_response = 'Accepted', enrol_cou = jdj)
    regi_stds = []
    for e in stz:
        gwp = int(e.id)
        czp = Enrollment.objects.get(id = gwp)
        dsb = Exam_register.objects.filter(ex_reg_cou=jdj, ex_reg_tea=sew, ex_reg_st_enroll = czp)
        for t in dsb:
            asw = int(t.ex_reg_st.id)
            regi_stds.append(asw)
    stz = Enrollment.objects.filter(enrol_reg__in = regi_stds)
    return render(request,'sched_test.html',{'stz':stz})


def sched_test1(request):
    numbb = request.POST.get('numbb')
    nmbb = int(numbb)
    request.session['exam_start'] =  request.POST.get('dtt')
    request.session['exam_stop'] =  request.POST.get('stt')

    drts = request.session['exam_start']
    drtd = drts.replace('T', ' ')
    time_zone = pytz.timezone('Asia/Calcutta')
    drtd = datetime.datetime.strptime(drtd, "%Y-%m-%d %H:%M")
    drtd = time_zone.localize(drtd)

    drts1 = request.session['exam_stop']
    drtd1 = drts1.replace('T', ' ')
    drtd1 = datetime.datetime.strptime(drtd1, "%Y-%m-%d %H:%M")
    drtd1 = time_zone.localize(drtd1)

    k = request.POST.getlist('scd')
    for edd in k:
        edd = int(edd)
        mkkp = Enrollment.objects.get(id = edd)

        stz = Registration.objects.get(id = mkkp.enrol_reg.id)
        kmkk = Exam.objects.filter(Exam_reg_st = stz)
        for yp in kmkk:
            nkm = yp.Time_start
            cpp = nkm.replace(tzinfo=pytz.utc).astimezone(time_zone)
            if (cpp > drtd) and (cpp < drtd1):
                messages.success(request, "Slot already booked")
                return redirect('sched_test')
            pw = yp.Time_stop
            jkm = pw.replace(tzinfo=pytz.utc).astimezone(time_zone)

            if (jkm > drtd) and (jkm < drtd1):
                messages.success(request, "Slot already booked")
                return redirect('sched_test')

            if (cpp > drtd) and (jkm < drtd1):
                messages.success(request, "Slot already booked")
                return redirect('sched_test')



    request.session['cc'] = nmbb
    request.session['stu_for_test'] = k
    return render(request,'sched_test2.html')


def sched_test3(request):
    email = 'devuzzdevika2@gmail.com'
    m = request.session['stu_for_test']
    ques = request.POST.get('ques')
    op1 = request.POST.get('op1')
    op2 = request.POST.get('op2')
    op3 = request.POST.get('op3')
    ans = request.POST.get('ans')
    c = request.session['cc']
    if c>0:
        for i in m:
            stz = Enrollment.objects.get(id = i)
            szw = int(stz.enrol_tea.id)
            tea_regg = Registration.objects.get(id = szw)
            szct = int(stz.enrol_cou.id)
            cou_regg = Course.objects.get(id = szct)
            szst = int(stz.enrol_reg.id)
            stu_regg = Registration.objects.get(id = szst)
            fd = Exam()
            fd.Option1 = op1
            fd.Option2 = op2
            fd.Option3 = op3
            fd.Correct_answer = ans
            fd.Question = ques

            drts = request.session['exam_start']
            print(drts)
            print(type(drts))
            drtd = drts.replace('T',' ')
            print(drtd)
            print(type(drtd))
            time_zone = pytz.timezone('Asia/Calcutta')
            print(time_zone)
            print(type(time_zone))
            drtd = datetime.datetime.strptime(drtd,"%Y-%m-%d %H:%M")
            print(drtd)
            print(type(drtd))
            mg = time_zone.localize(drtd)
            print(mg)
            print(type(mg))
            fd.Time_start = time_zone.localize(drtd)

            drts1 = request.session['exam_stop']
            drtd1 = drts1.replace('T', ' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd1 = datetime.datetime.strptime(drtd1, "%Y-%m-%d %H:%M")
            fd.Time_stop = time_zone.localize(drtd1)
            fd.Exam_reg_st = stu_regg
            fd.Exam_reg_tea = tea_regg
            fd.Exam_cou = cou_regg
            fd.save()
        c -= 1
        request.session['cc'] = c
        if c == 0:
            for t in m:
                skm = Enrollment.objects.get(id=t)
                to_email = skm.enrol_reg.user.email
                strr_timg = request.session['exam_start']
                strr_timg = strr_timg.replace('T', ' ')
                stpp_timg = request.session['exam_stop']
                stpp_timg = stpp_timg.replace('T', ' ')
                mkmp = "Exam scheduled for subject " + skm.enrol_cou.cou_cat.Category_title + " (course - " + skm.enrol_cou.Course_title + "). Time starts at " + strr_timg + " and ends by " + stpp_timg + "."
                send_mail('Exam scheduled', mkmp, email, [to_email], fail_silently=False)
            messages.success(request, 'Exam scheduled successfully')
            return redirect('teacher_home')
        return render(request,'sched_test2.html')
    else:
        for t in m:
            skm = Enrollment.objects.get(id=t)
            to_email = skm.Student_email
            strr_timg = request.session['exam_start']
            stpp_timg = request.session['exam_stop']
            mkmp = "Exam scheduled for subject "+skm.Subject_name+" (course - "+skm.Course_name+". Time starts at "+strr_timg+" and ends by "+stpp_timg+"."
            send_mail('Exam scheduled', mkmp, email, [to_email], fail_silently=False)
        messages.success(request, 'Exam scheduled successfully')
        return redirect('teacher_home')


def delete_test(request):
    fg = Exam.objects.filter(Exam_reg_tea = request.session['logg'])
    return render(request, 'delete_test.html', {'fg': fg})


def delete_test1(request, id):
    Exam.objects.get(id = id).delete()
    messages.success(request, 'Exam deleted successfully')
    return redirect('delete_test')


def exam_result(request):
    gt = Exam_results.objects.filter(Exam_res_reg_tea = request.session['logg'])
    return render(request,'exam_result.html',{'gt':gt})


def delete_ex_re(request, id):
    Exam_results.objects.get(id=id).delete()
    return redirect('exam_result')


def m_m1(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request, 'msg1.html', {'bb': bb})


def del_msg_teacher(request,id):
    Messages.objects.get(id = id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('m_m1')


def reply_msg_teacher(request,id):
    pa = Messages.objects.get(id=id)
    toto = int(pa.From_reg.id)
    p_to = Registration.objects.get(id=toto)
    p = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Message_content = msg_cont
        pa1.From_reg = p
        pa1.To_reg = p_to
        pa1.save()
        messages.success(request, 'Message reply successful')
        return redirect('m_m1')
    return render(request,'reply_msg_teacher.html',{'pa':pa})


def sent_msg_teacher(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = int(to_em)
        reg_to = Registration.objects.get(id=ddp)
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Message_content = msg_cont
        nm.From_reg = p
        nm.To_reg = reg_to
        nm.save()
        messages.success(request, 'Message sent successfully')
        return redirect('m_m1')
    return render(request,'sent_msg_teacher.html',{'kk':kk})


def atten(request):
    h = Registration.objects.get(id = request.session['logg'])
    ss = Enrollment.objects.filter(Teacher_email = h.Email)
    if request.method == 'POST':
        atn = request.POST.get('atn')
        atn1 = request.POST.get('atn1')
        dw = Enrollment.objects.get(id = atn)
        dw.Attendance = atn1
        dw.save()
        messages.success(request, 'Attendance given')
        return redirect('teacher_home')
    return render(request,'atten.html',{'ss':ss})


def st_book_courses(request):
    st = Registration.objects.get(id = request.session['logg'])
    buk = Enrollment.objects.filter(enrol_reg = st)
    return render(request, 'st_book_courses.html',{'buk':buk,'st':st})


def acc_chapter(request, id):
    gh = Enrollment.objects.get(id = id)
    if gh.Teacher_response == 'To be expected' or gh.Teacher_response == 'Rejected' or gh.Payment_status != 'paid':
        messages.success(request, 'Your payment is pending or wait for teacher\'s approval')
        return redirect('student_home')
    request.session['acc_cha_teacher'] = t_id = int(gh.enrol_tea.id)
    nn = Registration.objects.get(id = t_id)
    request.session['tch_idd'] = nn.id
    cou_idd = int(gh.enrol_cou.id)
    thr = Course.objects.get(id = cou_idd)
    fd = Chapter.objects.filter(cha_cou = thr)
    return render(request, 'acc_chapter1.html', {'fd':fd})


def acc_chapter1(request):
    mnm = Registration.objects.get(id = request.session["logg"])
    sz1 = request.POST.get('cha')
    request.session['cou_ch_nme'] = chtw = int(sz1)
    sz = Chapter.objects.get(id = chtw)
    sz_cnt = Content.objects.filter(cont_cha = sz)
    mj = Learning_progress.objects.filter(Learn_p_reg = mnm)
    return render(request, 'acc_chapter2.html', {'sz_cnt': sz_cnt,'mj':mj})


def compp(request):
    cco = Registration.objects.get(id = request.session['acc_cha_teacher'])
    mnm = Registration.objects.get(id = request.session["logg"])
    idd = request.POST.getlist('id')
    comm = request.POST.getlist('comm')
    ggt = zip(idd,comm)
    for i,h in ggt:
        dvt = int(i)
        dvt1 = Content.objects.get(id=dvt)
        if Learning_progress.objects.filter(Learn_p_cnt = dvt1).exists():
            pk = Learning_progress.objects.filter(Learn_p_cnt = dvt1)
            for t in pk:
                t.Status = h
                t.save()
        else:
            pk = Learning_progress()
            pk.Status = h
            pk.Learn_p_reg = mnm
            pk.Learn_p_tea_reg = cco
            pk.Learn_p_cnt = dvt1
            pk.save()
    messages.success(request, 'Learning progress updated')
    return redirect('student_home')


def stu_sub_selnew(request):
    sne = Category.objects.all()
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat1 = int(cat)
        request.session['st_bk_category'] = cat1
        cc = Course.objects.filter(cou_cat =cat1)
        return render(request,'st_sub_selnew2.html',{'cc':cc})
    return render(request, 'st_sub_selnew1.html',{'snew':sne})


def stu_sub_selnew1(request):
    sne = Category.objects.get(id = request.session['st_bk_category'])
    cou = request.POST.get('cou')
    cou1 = int(cou)
    request.session['st_bk_course'] = cou1
    cse = Course.objects.get(id = cou1)
    c_tit = str(cse.Course_title)
    cse = Course.objects.filter(cou_cat = sne, Course_title = c_tit)
    return render(request, 'st_sub_selnew3.html', {'cse': cse})


def stu_buk_teacher(request, id):
    id = int(id)
    dh = Registration.objects.get(id = request.session['logg'])
    cou = Course.objects.get(id = id)
    id_tea = int(cou.cou_reg.id)
    nm = Registration.objects.get(id = id_tea)
    if Enrollment.objects.filter(enrol_reg = dh, enrol_tea = nm, enrol_cou = cou).exists():
        messages.success(request, 'You have already booked this course')
        return redirect('student_home')

    spp = Enrollment()
    spp.enrol_reg = dh
    spp.enrol_tea = nm
    spp.enrol_cou = cou
    spp.Teacher_response = 'To be expected'
    spp.notify = 'new'
    spp.save()

    messages.success(request, 'You have successfully booked a course')
    return redirect('student_home')



def pay_student(request):
    ds = Enrollment.objects.filter(enrol_reg = request.session['logg'], Teacher_response = 'Accepted')
    msk = []
    for t in ds:
        c_f = float(t.enrol_cou.Course_fee)
        if c_f > 0:
            hh = int(t.id)
            msk.append(hh)
    ds = Enrollment.objects.filter(id__in = msk)
    return render(request, 'pay_student.html', {'ds': ds})


def pay_stud_cours(request, id):
    id = int(id)
    tgt = Enrollment.objects.get(id=id)
    if tgt.Payment_status == 'paid':
        messages.success(request, 'You have already paid')
        return redirect('pay_student')
    wtek = str(7)
    jej = tgt.enrol_cou.Course_fee
    jej = float(jej)
    order_currency = 'INR'
    callback_url = 'http://' + str(get_current_site(request)) + "/pay_teacher_razor"
    notes = {'order-type': "Student book fee", 'key': 'value'}
    razorpay_order = razorpay_client.order.create(
        dict(amount=jej * 100, currency=order_currency, notes=notes, receipt=wtek, payment_capture='0'))
    order_id = razorpay_order['id']
    return render(request, 'pay_stud_cours.html', {'order_id': order_id, 'final_price': jej, 'razorpay_merchant_id': settings.razorpay_id, 'callback_url': callback_url,'tgt': tgt})


def stu_buk_teacherr(request, id):
    id = int(id)
    tgt = Enrollment.objects.get(id = id)
    if tgt.Payment_status == 'paid':
        messages.success(request, 'You have already paid')
        return redirect('pay_student')
    if request.method == 'POST':
        paid = request.POST.get('paid')
        paid = float(paid)
        if float(tgt.enrol_cou.Course_fee) > paid:
            messages.success(request, 'Please pay full amount')
            return render(request,'paid.html',{'tgt':tgt})
        tgt.Payment_status = 'paid'
        tgt.save()

        kmwe = 'You have paid for the course '+tgt.enrol_cou.cou_cat.Category_title+'('+tgt.enrol_cou.Course_title+')'
        messages.success(request, kmwe)
        return redirect('student_home')
    return render(request,'paid.html',{'tgt':tgt})


def do_cer(request):
    sr = Enrollment.objects.filter(enrol_reg = request.session['logg']).exclude(Certificate = '')
    return render(request,'do_cer.html',{'sr':sr})


def del_cer(request):
    df = Enrollment.objects.all().exclude(Certificate = '')
    return render(request,'del_cer.html',{'df':df})


def delete_cert(request, id):
    m = Enrollment.objects.get(id = id)
    m.Certificate = None
    m.save()
    messages.success(request, 'Deleted certificate')
    return redirect('del_cer')


def update_pr_st(request):
    b = Registration.objects.get(id = request.session['logg'])
    mjm = b.user.pk
    um = User.objects.get(id = mjm)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')

        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'update_pr_st.html', {'b': b, 'um': um})


        passwords = make_password(psw)
        u = User.objects.get(id = mjm)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.first_name = f_name
        u.last_name = l_name
        u.save()

        user = auth.authenticate(username = user_name, password = psw)
        auth.login(request, user)

        bb = b.id
        m = int(bb)
        request.session['logg'] = m

        try:
            photo = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            b.Image = photo
            b.Password = psw
            b.user = u
            b.save()
            messages.success(request, 'Profile updated')
            return redirect('student_home')
        except:
            photo = request.POST.get('imgg')
            b.Password = psw
            b.Image = photo
            b.user = u
            b.save()
            messages.success(request, 'Profile updated')
            return redirect('student_home')
    return render(request, 'update_pr_st.html', {'b': b,'um':um})


def feedback(request):
    dd = Registration.objects.get(id = request.session['logg'])
    ds = Enrollment.objects.filter(enrol_reg = dd)
    if request.method == 'POST':
        couu = request.POST.get('couu')
        couu = int(couu)
        hdp = Enrollment.objects.get(id = couu)
        tea_regc = int(hdp.enrol_tea.id)
        tea_regc = Registration.objects.get(id = tea_regc)
        cou_regc = int(hdp.enrol_cou.id)
        cou_regc = Course.objects.get(id = cou_regc)
        score = request.POST.get('scorr')
        text_feed = request.POST.get('text_feed')
        qw = Feedback()
        qw.Feedback_text = text_feed
        qw.Rating_score = score
        qw.Feed_reg = dd
        qw.Feed_tea_reg = tea_regc
        qw.Feed_cou = cou_regc
        qw.save()
        messages.success(request, 'Thank you for your valuable feedback')
        return redirect('student_home')
    return render(request,'feedback.html',{'ds':ds})


def ch_p(request):
    th = Registration.objects.get(id = request.session['logg'])
    trp = th.user.pk
    u = User.objects.get(id=trp)
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        passwords = make_password(new_pass)
        u.password = passwords
        u.save()

        th.Password = new_pass
        th.save()
        messages.success(request, 'Password changed successfully. Login again with new password.')
        return redirect('logout')
    return render(request,'change_pass.html',{'th':th})


def ch_p_admin(request):
    th = Registration.objects.get(id = request.session['logg'])
    trp = th.user.pk
    u = User.objects.get(id=trp)
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        passwords = make_password(new_pass)
        u.password = passwords
        u.save()

        th.Password = new_pass
        th.save()
        messages.success(request, 'Password changed successfully. Login again with new password.')
        return redirect('logout')
    return render(request, 'ch_p_admin.html', {'th': th})


def ex_not(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg_st = hh)
    kk = []
    for i in fg:
        bb = i.Time_start
        print(bb)
        print(type(bb))
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        print(cpp)
        print(type(cpp))
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        print(bbn)
        print(type(bbn))
        if bbn not in kk:
            kk.append('Category')
            kk.append(i.Exam_cou.cou_cat.Category_title)
            kk.append('Course name')
            kk.append(i.Exam_cou.Course_title)
            kk.append('Start time')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('Stop time')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
    return render(request,'ex_not.html',{'kk':kk})


def start_test(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg_st = hh)
    fgc = timezone.now()
    hj = []
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        nbn = nb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        nbnn = nbn.strftime("%Y-%B-%d %I:%M:%S %p")
        nbnn1 = nbn.strftime("%b %d, %Y %H:%M:%S")

        mrtt = nb - zz
        mrtt = mrtt.total_seconds()
        mrtt = int(mrtt)
        mrtt *= 1000
        if fgc>zz and fgc<nb:
            nb = Exam.objects.filter(Exam_reg_st = hh, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                if i.Lock == 'locked':
                    messages.success(request, 'You have already attended the exam')
                    return redirect('student_home')
            for i in nb:
                hj.append(i.Correct_answer)
                request.session['teec'] = int(i.Exam_reg_tea.id)
                request.session['ssub'] = int(i.Exam_cou.id)
                request.session['student'] = int(i.Exam_reg_st.id)
                gg = str(nbnn)
            request.session['exam_id'] = hj
            return render(request,'start_test.html',{'nb':nb,'gg':gg,'nbnn1':nbnn1,'mrtt':mrtt})
    messages.success(request, 'No exam is scheduled now')
    return redirect('student_home')


def save_exam(request):
    end_time = request.POST.get('end_time')
    edr = datetime.datetime.strptime(end_time, '%Y-%B-%d %I:%M:%S %p')
    b = datetime.datetime.now()
    bb = b.strftime('%Y-%B-%d %H:%M:%S')
    edr1 = datetime.datetime.strptime(bb, '%Y-%B-%d %H:%M:%S')
    if edr < edr1:
        messages.success(request, 'You have timed out')
        return redirect('student_home')
    correct_answers = request.POST.getlist('exx3')
    answers = request.POST.getlist('exx')
    print(correct_answers)
    print (answers)
    if len(correct_answers) != len(answers):
        messages.success(request, 'Your exam attempt failed due to selecting multiple or no answers')
        return redirect('student_home')
    count = 0
    count1 = 0
    for i in correct_answers:
        count1 += 1
    for i,j in zip(correct_answers,answers):
        if i == j:
            count += 1
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg_st = hh)
    fgc = timezone.now()
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        if fgc > zz and fgc < nb:
            nb = Exam.objects.filter(Exam_reg_st = hh, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                i.Lock = 'locked'
                i.save()
    ddd = Exam_results()
    ddd.Exam_res_reg_st = hh
    tchy = Registration.objects.get(id = request.session['teec'])
    ddd.Exam_res_reg_tea = tchy
    ccve = Course.objects.get(id = request.session['ssub'])
    ddd.Exam_res_cou = ccve
    ddd.Total_marks = count1
    ddd.Acquired_marks = count
    avg = 100 * float(count)/float(count1)
    if avg >= 80:
        ddd.Grade = 'A'
    elif avg < 80 and avg >= 50 :
        ddd.Grade = 'B'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    else:
        ddd.Grade = 'Failed'
    ddd.Time_stop = b
    ddd.save()
    messages.success(request, 'You have successfully finished your exam')
    return redirect('student_home')


def exam_result1(request):
    gt = Exam_results.objects.filter(Exam_res_reg_st = request.session['logg'])
    return render(request,'exam_result1.html',{'gt':gt})


def m_m2(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request, 'msg2.html', {'bb': bb})


def del_msg_student(request,id):
    Messages.objects.get(id = id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('m_m2')


def reply_msg_student(request,id):
    pa = Messages.objects.get(id = id)
    toto = int(pa.From_reg.id)
    p_to = Registration.objects.get(id=toto)
    p = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Message_content = msg_cont
        pa1.From_reg = p
        pa1.To_reg = p_to
        pa1.save()
        messages.success(request, 'Message reply successful')
        return redirect('m_m2')
    return render(request,'reply_msg_student.html',{'pa':pa})


def sent_msg_student(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = int(to_em)
        reg_to = Registration.objects.get(id=ddp)
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Message_content = msg_cont
        nm.From_reg = p
        nm.To_reg = reg_to
        nm.save()
        messages.success(request, 'Message sent successfully')
        return redirect('m_m2')
    return render(request,'sent_msg_student.html',{'kk':kk})


def adm_prof(request):
    gtt = Registration.objects.get(id = request.session['logg'])
    return render(request, 'adm_prof.html',{'gtt':gtt})


def del_admin(request, id):
    bb1 = Registration.objects.get(id = id)
    bb1 = bb1.user.pk
    User.objects.get(id = bb1).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return redirect('home')


def edit_admin(request):
    bb1 = Registration.objects.get(User_role = 'admin')
    rtrk = bb1.user.pk
    um = User.objects.get(id = rtrk)
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        em = request.POST.get('em')
        psw = request.POST.get('psw')

        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username=um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'update_admin.html', {'bb1': bb1, 'um': um})

        passwor = make_password(psw)
        df = Registration.objects.get(id=request.session['logg'])
        kmk = df.user.pk
        kmk = User.objects.get(id = kmk)
        kmk.username = user_name
        kmk.first_name = first
        kmk.last_name = last
        kmk.password = passwor
        kmk.email = em
        kmk.save()

        user = auth.authenticate(username = user_name, password = psw)
        auth.login(request, user)

        dcd = Registration.objects.get(User_role = 'admin')
        b = dcd.id
        m = int(b)
        request.session['logg'] = m

        dcd = Registration.objects.get(id = request.session['logg'])
        dcd.Password = psw
        dcd.user = kmk
        dcd.save()

        messages.success(request, 'You have successfully updated your profile')
        return redirect('adm_prof')
    return render(request, 'update_admin.html',{'bb1':bb1,'um':um})


def abb(request):
    amm = Registration.objects.get(User_role = 'admin')
    if request.method == 'POST':
        abbt = request.POST.get('abbt')
        idd = request.POST.get('idd')
        adc = Registration.objects.get(id = idd)
        adc.About_website = abbt
        adc.save()
        messages.success(request, 'Content added successfully')
        return redirect('admin_home')
    return render(request,'about_content.html',{'amm':amm})


def pass_req(request):
    dd = Requests.objects.all()
    return render(request,'pass_req.html',{'dd':dd})


def pass_req1(request, id):
    ff = Requests.objects.get(id = id)
    passwords = make_password(ff.New_password)
    print(passwords)
    u = User.objects.get(email = ff.Email)
    u.password = passwords
    u.save()

    tt = Registration.objects.get(Email=ff.Email)
    tt.Password = ff.New_password
    tt.save()
    Requests.objects.get(id=id).delete()
    dd = Requests.objects.all()
    return render(request, 'pass_req.html', {'dd': dd})


def admin(request):
    return render(request,'admin.html')


def translate_language(request):
    choices = ["Hindi", "Malayalam", "German", "French"]
    if request.method == 'POST':
        global convert
        n1 = request.POST.get('quer')
        n3 = request.POST.get('ch')
        n2 = Translator()

        if n3 == "Hindi":
            convert = "hi"

        elif n3 == "Malayalam":
            convert = "ml"

        elif n3 == "German":
            convert = "de"

        elif n3 == "French":
            convert = "fr"

        text_translate = n2.translate(n1, dest=convert)
        text_translate = text_translate.text
        return render(request, 'translate.html', {'ch': choices,'trk':text_translate})
    else:
        return render(request,'translatee.html', {'ch': choices})


def news_let(request):
    emm = request.POST.get('emm')
    kmk = Newsletter.objects.filter(Email = emm)
    for t in kmk:
        if t.Email == emm:
            messages.success(request, 'You have already subscribed for newsletter')
            return redirect('home')
    N = Newsletter()
    N.Email = emm
    N.save()
    messages.success(request, 'You have successfully subscribed for newsletter')
    return redirect('home')


def cou_comp_st_tea(request):
    nbn = Enrollment.objects.filter(enrol_tea = request.session['logg'])
    return render(request,'cou_comp_st_tea.html', {'nbn': nbn})


def cou_com_tea(request,id):
    sas = Enrollment.objects.get(id = id)
    sas.Course_completion_status = 'Completed'
    sas.save()
    return redirect('cou_comp_st_tea')


def cou_n_com_tea(request, id):
    sas = Enrollment.objects.get(id = id)
    sas.Course_completion_status = 'Pending'
    sas.save()
    return redirect('cou_comp_st_tea')


def pay_teacher(request):
    ds = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    return render(request,'pay_teacher.html',{'ds':ds})


def face_template1(request):
    bb = Enrollment.objects.filter(enrol_reg = request.session['logg'])
    return render(request,'face_template1.html',{'bb':bb})


def face_template2(request):
    latt = request.POST.get('latt')
    longg = request.POST.get('longg')
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.reverse(latt + "," + longg)
    except:
        messages.success(request, 'Please wait for 30 seconds to identify location and then submit')
        return redirect('face_template1')
    request.session['place_of_atten'] = str(location)
    b = request.POST.get('coursse')
    try:
        request.session['couss'] = b = int(b)
    except:
        messages.success(request, 'Please register for a course')
        return redirect('face_template1')
    sbb = Enrollment.objects.get(id = b)
    return render(request,'face_template.html',{'sbb':sbb})


def TakeImages(request):
    if request.method == 'POST':
        sbb = Enrollment.objects.get(id = request.session['couss'])
        nam = request.POST.get('name')
        em = request.POST.get('em')
        serial = 0
        try:
            exists = User.objects.get(first_name = nam, email = em)
            if exists:
                reader1 = User.objects.all()
                for k in reader1:
                    serial = serial + 1
                serial = (serial // 2)
        except:
            messages.success(request, 'Email or name is incorrect')
            return render(request, 'face_template.html',{'sbb':sbb})
        name = str(nam)
        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "C:\\Users\\User\\Desktop\\PROJECTS\\devika_project_normalized\\learning\\learn\\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    km = User.objects.get(first_name = name, email = em)
                    serial = km.id
                    cv2.imwrite("C:\\Users\\User\\Desktop\\PROJECTS\\devika_project_normalized\\learning\\learn\\TrainingImage\\" + name + "." + str(serial) + "." + str(km.email) + "." + str(sampleNum) + ".jpg",gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()

            recognizer = cv2.face_LBPHFaceRecognizer.create()
            faces, ID = getImagesAndLabels("C:\\Users\\User\\Desktop\\PROJECTS\\devika_project_normalized\\learning\\learn\\TrainingImage")
            recognizer.train(faces, np.array(ID))
            recognizer.save("C:\\Users\\User\\Desktop\\PROJECTS\\devika_project_normalized\\learning\\learn\\Trainner.yml")


            messages.success(request, 'Images taken')
            return render(request, 'face_template.html',{'sbb':sbb})
        else:
            if (name.isalpha() == False):
                messages.success(request, 'Not correct name')
                return render(request, 'face_template.html',{'sbb':sbb})


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def TrackImages(request):
    sbb = Enrollment.objects.get(id = request.session['couss'])
    tea_regb = int(sbb.enrol_tea.id)
    tea_regb = Registration.objects.get(id = tea_regb)
    # check_haarcascadefile()
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    try:
        recognizer.read("C:\\Users\\User\\Desktop\\PROJECTS\\devika_project_normalized\\learning\\learn\\Trainner.yml")
    except:
        messages.success(request, 'Person cannot be identified. Please take images.')
        return render(request, 'face_template.html',{'sbb':sbb})
    harcascadePath = "C:\\Users\\User\\Desktop\\PROJECTS\\devika_project_normalized\\learning\\learn\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            serial = int(serial)
            if (conf < 50):
                try:
                    df = User.objects.get(id=serial)
                    svtz = Registration.objects.filter(user=df)
                    hrtd = 2
                    for s in svtz:
                        hrtd = int(s.id)
                        hrtd = Registration.objects.get(id=hrtd)
                        break
                except:
                    messages.success(request, 'Your ID has been updated. Please take images')
                    return render(request, 'face_template.html',{'sbb':sbb})

                ghy = df.first_name +' '+df.last_name
                ghy = str(ghy)

                today = datetime.date.today()
                if Attendance.objects.filter(atten_stud = hrtd, atten_tea = tea_regb, atten_enroll = sbb, Date_tim__date = today).exists():
                    messages.success(request, 'You have already taken attendance today')
                    return render(request, 'face_template.html',{'sbb':sbb})

                kmk = Attendance()
                kmk.Attendance_done_location = request.session['place_of_atten']
                kmk.atten_stud = hrtd
                kmk.atten_tea = tea_regb
                kmk.atten_enroll = sbb
                bb = ghy
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
                if (cv2.waitKey(1) == ord('q')):
                    kmk.save()
                    cam.release()
                    cv2.destroyAllWindows()
                    messages.success(request, 'Attendance taken')
                    return render(request, 'face_template.html',{'sbb':sbb})
            else:
                Id = 'Unknown'
                bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
    messages.success(request, 'Failed to take attendance. Please be available in front of camera.')
    return render(request, 'face_template.html',{'sbb':sbb})


def view_stud_attendance(request):
    at = Attendance.objects.filter(atten_stud = request.session['logg'])
    return render(request, 'view_stud_attendance.html', {'at':at})



def live_class(request):
    gg = Registration.objects.get(id = request.session['logg'])
    livv = Live.objects.filter(liv_tea = gg)
    return render(request,'live_class.html',{'livv':livv})


def edit_live(request, id):
    frf = Registration.objects.get(id = request.session['logg'])
    id = int(id)
    ccf = Live.objects.get(id = id)
    couu = Course.objects.filter(cou_reg = frf)
    cou_idd = []
    for t in couu:
        gf = int(t.id)
        cou_idd.append(gf)
    enr = Enrollment.objects.filter(enrol_cou__in = cou_idd, enrol_tea = frf)
    if request.method == 'POST':
        couph = request.POST.get('couph')
        couph = int(couph)
        couph = Enrollment.objects.get(id = couph)
        link = request.POST.get('link')
        date = request.POST.get('date')
        ccf.link = link
        ccf.ldate = date
        ccf.enrol = couph
        ccf.liv_tea = frf
        ccf.save()
        messages.success(request, 'Live class edited')
        return redirect('live_class')
    return render(request,'edit_live.html',{'ccf':ccf,'enr':enr})


def delete_live(request, id):
    Live.objects.get(id = id).delete()
    messages.success(request, 'Live class deleted')
    return redirect('live_class')


def add_live(request):
    frf = Registration.objects.get(id=request.session['logg'])
    cco = Course.objects.filter(cou_reg = frf)
    if request.method == 'POST':
        couph = request.POST.get('couph')
        couph = int(couph)
        couph = Course.objects.get(id = couph)
        enrr = Enrollment.objects.filter(enrol_tea = frf, enrol_cou = couph)
        link = request.POST.get('link')
        timm = request.POST.get('timm')
        for t in enrr:
            cc = Live()
            cc.link = link
            cc.ldate = timm
            cc.enrol = t
            cc.liv_tea = frf
            cc.save()
        messages.success(request, 'Live class has been added')
        return redirect('live_class')
    return render(request,'add_live.html',{'cco':cco})



def view_live(request):
    ftr = Registration.objects.get(id = request.session['logg'])
    trg = Enrollment.objects.filter(enrol_reg = ftr)
    zzm = []
    for e in trg:
        thg = int(e.id)
        zzm.append(thg)
    livv = Live.objects.filter(enrol__in = zzm)
    return render(request,'view_live.html',{'livv':livv})


def view_cat(request):
    cat = Category.objects.all()
    return render(request,'view_cat.html',{'cat':cat})


def view_cou(request,id):
    cou = Subject.objects.filter(id=id)
    return render(request,'view_cou.html',{'cou':cou})


def reg_course(request,id):
    cou = Subject.objects.filter(id=id)
    return render(request,'reg_course.html',{'cou':cou})



def assignment(request):
    kk = Registration.objects.get(id=request.session['logg'])
    mbm = Assignment.objects.filter(teacher_reg = kk)
    return render(request,'assignment.html',{'mbm':mbm})


def add_assignment(request):
    gttf = Registration.objects.get(id = request.session['logg'])
    tft = Course.objects.filter(cou_reg = gttf)
    if request.method == 'POST':
        cn = request.POST.get('cn')
        cn = int(cn)
        cn = Course.objects.get(id = cn)
        at = request.POST.get('at')
        photo = request.FILES['q']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        m = request.POST.get('m')
        sd = request.POST.get('sd')
        ed = request.POST.get('ed')
        pass_perc = request.POST.get('pass_perc')
        cc= Assignment()
        cc.assign_course = cn
        cc.assignment_topic = at
        cc.assignment_upload = photo
        cc.total_marks = m
        cc.start_date = sd
        cc.teacher_reg = gttf
        cc.submission_date = ed
        cc.pass_percent = pass_perc
        cc.save()
        messages.success(request, 'Assignment has been added')
        return redirect('assignment')
    return render(request,'add_assignment.html',{'tft':tft})


def edit_assignment(request, id):
    id = int(id)
    ccf = Assignment.objects.get(id = id)
    gttf = Registration.objects.get(id = request.session['logg'])
    tft = Course.objects.filter(cou_reg = gttf)
    if request.method == 'POST':
        cn = request.POST.get('cn')
        cn = int(cn)
        sds = Course.objects.get(id = cn)
        at = request.POST.get('at')
        m = request.POST.get('m')
        sd = request.POST.get('sd')
        ed = request.POST.get('ed')
        pass_perc = request.POST.get('pass_perc')
        try:
            photo = request.FILES['q']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            ccf.assign_course = sds
            ccf.assignment_topic = at
            ccf.assignment_upload = photo
            ccf.total_marks = m
            ccf.start_date = sd
            ccf.teacher_reg = gttf
            ccf.submission_date = ed
            ccf.pass_percent = pass_perc
            ccf.save()
            messages.success(request, 'Assignment has been edited')
            return redirect('assignment')
        except:
            photo1 = request.POST.get('q1')
            ccf.assign_course = sds
            ccf.assignment_topic = at
            ccf.assignment_upload = photo1
            ccf.total_marks = m
            ccf.start_date = sd
            ccf.teacher_reg = gttf
            ccf.submission_date = ed
            ccf.pass_percent = pass_perc
            ccf.save()
            messages.success(request, 'Assignment has been edited')
            return redirect('assignment')
    return render(request,'edit_assignment.html',{'tft':tft,'ccf':ccf})


def delete_assignment(request, id):
    Assignment.objects.get(id = id).delete()
    messages.success(request, 'Assignment deleted')
    return redirect('assignment')


def upload_assi_tea(request):
    kk = Registration.objects.get(id=request.session['logg'])
    gbv = Assignment.objects.filter(teacher_reg = kk)
    gg = []
    for k in gbv:
        k = int(k.id)
        gg.append(k)
    mbm = Assignment_result.objects.filter(asssi_res_assi__in = gg)
    return render(request, 'upload_assi_tea.html', {'mbm': mbm})


def add_mark_assi_tea(request, id):
    mbm = Assignment_result.objects.get(id = id)
    if request.method == 'POST':
        mrk = request.POST.get('mrk')
        mrk = float(mrk)
        tot = float(mbm.asssi_res_assi.total_marks)
        if mrk > tot:
            messages.success(request, 'Assignment mark must not be more than total marks')
            return render(request, 'add_mark_assi_tea.html',{'mbm':mbm})
        tot_acq_percent = (mrk/tot)*100
        tot_acq_percent = round(tot_acq_percent,2)
        mbm.acquired_marks = mrk
        mbm.acquired_pass_percent = tot_acq_percent
        mbm.save()
        messages.success(request, 'Assignment mark added')
        return redirect('upload_assi_tea')
    return render(request, 'add_mark_assi_tea.html',{'mbm':mbm})


def delete_assignment_upload(request, id):
    Assignment_result.objects.get(id = id).delete()
    messages.success(request, 'Assignment result deleted')
    return redirect('upload_assi_tea')


def assi_st(request):
    kmk = Registration.objects.get(id = request.session['logg'])
    kmk1 = Enrollment.objects.filter(enrol_reg = kmk)
    ksdr = []
    for w in kmk1:
        dbr = int(w.enrol_cou.id)
        ksdr.append(dbr)
    kmk2 = Course.objects.filter(id__in = ksdr)
    zz2 = []
    for d in kmk2:
        d = int(d.id)
        zz2.append(d)
    a_st = Assignment.objects.filter(assign_course__in = zz2)
    if request.method == 'POST':
        ress = request.FILES['ress']
        fs = FileSystemStorage()
        fs.save(ress.name, ress)
        topp = request.POST.get('topp')
        topp = int(topp)
        sws = Assignment.objects.get(id = topp)
        today = datetime.datetime.today().date()
        if today > sws.submission_date:
            messages.success(request, 'Assignment submission date is over')
            return redirect('assi_st')
        if Assignment_result.objects.filter(asssi_res_assi = sws, asssi_res_st = kmk).exists():
            messages.success(request, 'Assignment already uploaded')
            return redirect('assi_st')
        vf = Assignment_result()
        vf.assignment_upload_ans = ress
        vf.asssi_res_assi = sws
        vf.asssi_res_st = kmk
        vf.save()
        messages.success(request, 'Assignment uploaded successfully')
        return redirect('student_home')
    return render(request, 'assi_st.html', {'a_st': a_st})


def exam_reg_stu(request):
    cct = Category.objects.all()
    return render(request, 'exam_reg_stu.html', {'cct': cct})


def exam_reg_stu1(request):
    ghg = request.POST.get('cat')
    ghg = int(ghg)
    kk = Category.objects.get(id = ghg)
    cse = Course.objects.filter(cou_cat = kk)
    return render(request, 'exam_reg_stu1.html', {'cse': cse})


def exam_reg_stu2(request, id):
    couh = Course.objects.get(id = id)
    catt = couh.cou_cat.pk
    tea = int(couh.cou_reg.id)
    rtr = Registration.objects.get(id = tea)
    if catt:
        pass
    else:
        messages.success(request, 'Category not existing')
        return redirect('exam_reg_stu')
    hwh = Registration.objects.get(id = request.session['logg'])

    bb = Assignment.objects.filter(assign_course = couh, teacher_reg = rtr)
    for v in bb:
        vbb = Assignment_result.objects.filter(asssi_res_assi = v, asssi_res_st = hwh)
        for s in vbb:
            if float(s.acquired_pass_percent) < float(v.pass_percent):
                messages.success(request, 'You have not passed all assignments of this teacher to register for exam')
                return redirect('exam_reg_stu')

    hhss = 0
    if Course_st_stop.objects.filter(cou_st_stop_cou = couh).exists():
        msa = Course_st_stop.objects.filter(cou_st_stop_cou  = couh)
        for k in msa:
            if Enrollment.objects.filter(enrol_reg = hwh, enrol_tea = rtr, enrol_cou = couh).exists():
                dtpe = Enrollment.objects.filter(enrol_reg = hwh, enrol_tea = rtr, enrol_cou = couh)
                for w in dtpe:
                    w = int(w.id)
                    hhss = Enrollment.objects.get(id=w)
                stt_ddp = k.start_date
                stop_ddp = k.end_date
                difference = stop_ddp - stt_ddp
                num_of_days = difference.days
                nsu = Attendance.objects.filter(atten_stud = hwh, atten_enroll = hhss).count()
                atn_percent = (nsu / num_of_days) * 100
                if atn_percent < 60:
                    messages.success(request, 'Your attendance percent is below 60%')
                    return redirect('exam_reg_stu')

    try:
        ed = Exam_register()
        ed.ex_reg_st = hwh
        ed.ex_reg_tea = rtr
        ed.ex_reg_cou = couh
        ed.ex_reg_st_enroll = hhss
        ed.save()
    except:
        messages.success(request, 'Cannot register for exam because you have not enrolled for this course')
        return redirect('exam_reg_stu')
    messages.success(request, 'Exam registration successful')
    return redirect('student_home')


def atten_admin(request):
    pkm = Attendance.objects.all()
    return render(request,'atten_admin.html',{'pkm':pkm})


def attendance_between_date_admin(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        pkm = Attendance.objects.filter(Date_tim__range = [start_date, end_date])
        return render(request,'atten_admin.html',{'pkm':pkm})
    else:
        messages.success(request, 'Please select start and stop dates')
        return redirect('atten_admin')


def delete_atten_admin(request, id):
    Attendance.objects.get(id = id).delete()
    messages.success(request, 'Attendance deleted successfully')
    return redirect('atten_admin')


def atten_tea(request):
    kmk = Registration.objects.get(id = request.session['logg'])
    pkm = Attendance.objects.filter(atten_tea = kmk)
    return render(request, 'atten_tea.html', {'pkm': pkm})


def attendance_between_date_teacher(request):
    kmk = Registration.objects.get(id=request.session['logg'])
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        pkm = Attendance.objects.filter(Date_tim__range = [start_date, end_date], atten_tea = kmk)
        return render(request, 'atten_tea.html', {'pkm': pkm})
    else:
        messages.success(request, 'Please select start and stop dates')
        return redirect('atten_tea')


def pay_admin(request):
    pkm = Enrollment.objects.all()
    return render(request, 'pay_admin.html', {'pkm': pkm})


def payment_between_date_admin(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        pkm = Enrollment.objects.filter(Enrollment_date__range=[start_date, end_date])
        return render(request, 'pay_admin.html', {'pkm': pkm})
    else:
        messages.success(request, 'Please select start and stop dates')
        return redirect('pay_admin')


def courses_admin(request):
    pkm = Course.objects.all()
    pkmd = Course_st_stop.objects.all()
    return render(request, 'courses_admin.html', {'pkm': pkm,'pkmd':pkmd})


def course_between_date_admin(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        pkmd = Course_st_stop.objects.filter(start_date = start_date,end_date = end_date)
        gtg = []
        for e in pkmd:
            m = int(e.cou_st_stop_cou.id)
            gtg.append(m)
        pkm = Course.objects.filter(id__in = gtg)
        return render(request, 'courses_admin.html', {'pkm': pkm,'pkmd':pkmd})
    else:
        messages.success(request, 'Please select start and stop dates')
        return redirect('courses_admin')






