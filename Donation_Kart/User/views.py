from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .models import Event,Events_Supported,Cart,Donation
from userlogin.models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request,'User/home.html')

@login_required(login_url='login')
def events(request):
    eventslist=Events_Supported.objects.all()
    eventsset=[]
    for e in eventslist:
        eventsset.append(e.type)
    #eventslist=list(set(eventsset))
    events_eme = Event.objects.filter(completed=False).filter(verified=True).order_by('enddate')
    events_eme_list=[]
    for e in events_eme:
        dlist=[]
        dlist.append(e)
        donated_quantity=0
        for d in Donation.objects.filter(event_id=e.eventid):
            donated_quantity+=d.Quantity
        dlist.append(donated_quantity)
        dlist.append(e.requestedquantity)
        dlist.append(100-int(e.itemsremaining)*100/e.requestedquantity)
        dlist.append(e.requestedquantity-donated_quantity)
        events_eme_list.append(tuple(dlist))
    events_eme_list[:12]
    return render(request,'User/events.html',context={'eventslist':eventslist,'events':events_eme_list})


@login_required(login_url='login')
def cart(request):
    user=request.user
    if(request.POST):
        eventID=int(request.POST['eventid'])
        quantity=int(request.POST['quantity'])
        event=0
        for e in Event.objects.filter(eventid=eventID):
            event=e
        cartlist=Cart.objects.filter(user=user)
        flag=0
        for c in cartlist:
            if c.event==event:
                #quantity+=c.Quantity
                #amount=200
                #Cart.objects.filter(user=user).filter(event=event).update(Quantity=quantity)
                #Cart.objects.filter(user=user).filter(event=event).update(amount=amount)
                flag=1
        if flag==0:
            amount=quantity*event.costperitem
            Cart.objects.create(event=event,user=request.user,Quantity=quantity,amount=amount)
    cartcost=0
    cartlist=list()
    for c in Cart.objects.filter(user=user):
        for e in Event.objects.filter(completed=False).filter(verified=True):
            if c.event==e:
                cartlist.append([c,e])
                cartcost+=c.Quantity*e.costperitem
    #print(cartlist)
    count=len(cartlist)

    return render(request,'User/cart.html',context={'cartlist':cartlist,'count':count,'cartcost':cartcost})

@login_required(login_url='login')
def delete(request,id):
    event=0
    for e in Event.objects.filter(eventid=id):
        event=e
    cartItems = Cart.objects.filter(user=request.user,event=event)
    cartItems.delete()
    return cart(request)

@login_required(login_url='login')
def filter(request,id):
    type=id
    events_fil = Event.objects.filter(completed=False).filter(verified=True).filter(type=type)
    events_fil_list=[]
    for e in events_fil:
        dlist=[]
        dlist.append(e)
        donated_quantity=0
        for d in Donation.objects.filter(event_id=e.eventid):
            donated_quantity+=d.Quantity
        dlist.append(donated_quantity)
        dlist.append(e.requestedquantity)
        dlist.append(100-int(e.itemsremaining)*100/e.requestedquantity)
        dlist.append(e.requestedquantity-donated_quantity)
        events_fil_list.append(tuple(dlist))
    return render(request,'User/filter.html',context={'events':events_fil_list})

@login_required(login_url='login')
def proceed(request):
    user=request.user
    count=Cart.objects.filter(user=user).count()
    if count and payment(request):
        for c in Cart.objects.filter(user=user):
            for e in Event.objects.filter(completed=False).filter(verified=True):
                if c.event==e:
                    itemsremaining=e.itemsremaining-c.Quantity
                    Event.objects.filter(eventid=e.eventid).update(itemsremaining=itemsremaining)
                    Cart.objects.filter(user=user).delete()
                    return home(request)
    return cart(request)


def payment(request):
    return True
