from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from customer.models import request
from customer.forms import request_form
from forum.models import forumdetails

@login_required
def home(request):
    form = request_form()
    x = forumdetails.objects.all()
    print(x)
    if request.method == 'POST':
        form = request_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse("Request sent sucessfully!")
        else:
            return render(request, 'customer/home.html',{'form':form,}, {'err':form.errors,})
    return render(request, 'customer/home.html', {'form':form, 'x':x,})
