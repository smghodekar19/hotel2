from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from HotelApp.models import Hotels
from HotelApp.models import Review
from HotelApp.models import Room
from django.views import generic
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse,reverse_lazy
from ManageHotels.models import Photo
from HotelApp.models import Proposal
from django.core.urlresolvers import reverse
from django.views import View
from django.db.models import Q



def home(request):
    return render(request,'HotelApp/home.html')

def userDash(request):
    return render(request,'HotelApp/userDash.html')
@login_required
def hotelindex(request):
    hotels_list = Hotels.objects.all()
    for hotel in hotels_list:
        hotel.thumbnail = Photo.objects.filter(hotel=hotel).first()
    context = {'Hotels': hotels_list}
    return render(request,'HotelApp/showhotels.html',context)

def regcomplete(request):
        link = reverse('HotelApp:userDash')
        return HttpResponseRedirect(link)

def hoteldetails(request, pk):

    #thehotel = Category.objects.filter(id = pk)[0]
    thehotel = Hotels.objects.get(id = pk)
    reviews = Review.objects.filter(hotel=thehotel)
    rooms = Room.objects.filter(hotel=thehotel)
    photos = Photo.objects.filter(hotel=thehotel)









    for room in rooms:
        room.spaceleft = 1
    current_user = request.user
    context = {'hotels': thehotel, 'reviews':reviews,'user':current_user,'rooms':rooms,'Photos':photos}
    return render(request, 'HotelApp/hoteldetails.html', context)


class reviewCreateView(CreateView):

    model = Review
    fields = ['comment','rating']
    #success_url = '/hotels/'
    def get_success_url(self):
        hotelid = self.kwargs['id']
        url = reverse('HotelApp:hoteldetails', args=[hotelid])
        return url
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel_id = self.kwargs['id']
        return super(reviewCreateView, self).form_valid(form)

class reviewUpdateView(UpdateView):

    model = Review
    fields = ['comment','rating']
    #success_url = '/hotels/'
    def get_success_url(self):
        reviewid = self.kwargs['pk']
        review = Review.objects.get(id = reviewid)
        hotel = review.hotel
        hotelid = hotel.id
        url = reverse('HotelApp:hoteldetails', args=[hotelid])
        return url
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(reviewUpdateView, self).form_valid(form)

class reviewDeleteView(DeleteView):
    model = Review
    def get_success_url(self):
        reviewid = self.kwargs['pk']
        review = Review.objects.get(id = reviewid)
        hotel = review.hotel
        hotelid = hotel.id
        url = reverse('HotelApp:hoteldetails', args=[hotelid])
        return url
class partnerCreateView(CreateView):

    model = Proposal
    fields = ['CompanyName','CompanyEmail','HQAddress','Vision']
    #success_url = '/hotels/'
    def get_success_url(self):
        url = reverse('HotelApp:userDash')
        return url
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(partnerCreateView, self).form_valid(form)

class hotelSearch(View):
    def get(self,request):
        return render(request, 'HotelApp/search.html')
    def post(self,request):
        Searchterm = request.POST.get("searchterm").title()
        NumTravelers = request.POST.get("numtravelers")

        if not Searchterm and not NumTravelers:
            hotels_list = Hotels.objects.all()
        elif Searchterm and not NumTravelers:
            hotels_list = Hotels.objects.filter(Q(City__contains=Searchterm) | Q(Country__contains=Searchterm)
            | Q(Address__contains=Searchterm))
        elif NumTravelers and not Searchterm:
            hotels_list = Hotels.objects.filter(room__Capacity__gte =  NumTravelers)
        elif Searchterm and NumTravelers:
            hotels_list = Hotels.objects.filter(Q(City__contains=Searchterm) | Q(Country__contains=Searchterm)
            | Q(Address__contains=Searchterm)).filter(room__Capacity__gte = NumTravelers)
        Range = request.POST.get("daterange")
        Rangesplit = Range.split(' to ')
        CheckIn = Rangesplit[0]
        CheckOut = Rangesplit[1]
        request.session['checkin'] = CheckIn
        request.session['checkout'] = CheckOut
        for hotel in hotels_list:
            hotel.thumbnail = Photo.objects.filter(hotel=hotel).first()
        context = {'hotels':hotels_list}
        return render(request, 'HotelApp/showhotels.html', context)
