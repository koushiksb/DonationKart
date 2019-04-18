from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from verifier.models import pending_request
from customer.models import request as req
from forum.models import forumdetails
from userlogin import Profile

def basic(request):
    return render(request, 'basic.html')

# def index(request):
#     if request.method == 'POST':
#         uname = request.POST.get('uname')
#         password = request.POST.get('pass')
#         admin = authenticate(username=uname, password=password)
#
#         if admin:
#             x = UserProfile.objects.get(prof=admin)
#             if admin.is_active and x.user_type == 'V':
#                 login(request,admin)
#                 return HttpResponseRedirect(reverse('admin_login:home'))
#             elif admin.is_active and x.user_type == 'C':
#                 login(request,admin)
#                 return HttpResponseRedirect(reverse('cus_login:home'))
#             else:
#                 return HttpResponse("Account has been diasabled!")
#         else:
#             return render(request, 'admin/main.html', {'err':'Invalid Login Details!'})
#
#     return render(request, 'admin/main.html')

@login_required
def home(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if value == 'Appoint':
                temp = req.objects.get(username = key)
                new_pr = pending_request(appointed_by = request.user, username = temp.username, request_header = temp.request_header, description = temp.description, amount = temp.amount, by_date = temp.by_date, pic = temp.pic, request_date = temp.request_date)
                new_pr.save()
                temp.delete()
            if value == 'Cancel':
                temp = req.objects.get(username = key)
                temp.delete()

    if request.method == 'GET':
        for key, value in request.GET.items():
            if value == 'Verify':
                temp = pending_request.objects.get(username = key)
                new_bd = forumdetails(username = temp.username, request_header = temp.request_header, description = temp.description, amount = temp.amount, by_date = temp.by_date, pic = temp.pic)
                new_bd.save()
                temp.delete()
            if value == 'Cancel':
                temp = pending_request.objects.get(username = key)
                temp.delete()

    current_user = request.user
    #cuser = UserProfile.objects.raw('''select * from appname_tablename where prof=%s''',[current_user])
    cuser = Profile.objects.filter(user = current_user).values()
    print(cuser)
    #new_requests = req.objects.raw('''select * from appname_tablename''')
    new_requests = req.objects.all()
    #pend_req = pending_request.objects.raw('''select * from appname_tablename where appointed_by=%s''',[current_user.username])
    pend_req = pending_request.objects.filter(appointed_by = current_user)
    return render(request, 'admin/home.html', {'user': current_user, 'c':cuser, 'requests':new_requests, 'request2':pend_req,})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login.home'))
