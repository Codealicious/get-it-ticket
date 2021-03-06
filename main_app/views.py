from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# import uuid
# import boto3
from .models import Ticket, Venue, Event, Business
from .forms import EventForm, TicketForm

# # Create your views here.
def index(request):
    return render(request,'home.html')

def signup(request):
    error_message =''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid sign up - try again'"
    form = UserCreationForm()
    context = {'form': form, 'error_message' : error_message}
    return render(request, 'registration/signup.html', context)


# Create your views here.

# BUSINESS ------------------------------------------------------------------------------

class BusinessCreate(LoginRequiredMixin, CreateView):
    model = Business
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BusinessDelete(LoginRequiredMixin, DeleteView):
    model = Business
    success_url = '/business/'

@login_required
def business_detail(request, business_id):
    business = Business.objects.get(id=business_id)
    # venues = Venue.objects.get(id=venue_id)
    # venues_business_doesnt_have = Venue.objects.exclude(id__in = business.venues.all().values_list('id'))

    # venues = Venues.all()?
    return render(request, 'business/detail.html', {
        'business': business, 
        # 'venues': venues 
    })



# VENUE ---------------------------------------------------------------------------------
class VenueCreate(LoginRequiredMixin, CreateView):
    model = Venue
    fields = ['name', 'capacity']

    def form_valid(self, form):
        # Assign the logged in user to the venue being created
        form.instance.user = self.request.user
        # Let CreateView's form_valid method do its thing
        return super().form_valid(form)

class VenueUpdate(LoginRequiredMixin, UpdateView):
    model = Venue
    fields = 'capacity'

class VenueDelete(LoginRequiredMixin, DeleteView):
    model = Venue
    success_url = '/business/'



# EVENT ---------------------------------------------------------------------------------
class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'date', 'description', 'ageRestrict', 'ticketCount', 'availability']

    def form_valid(self, form):
        # Assign the logged in user to the event being created
        form.instance.user = self.request.user
        # Let CreateView's form_valid method do its thing
        return super().form_valid(form)


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'date', 'description', 'ageRestrict', 'ticketCount', 'availability']

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/venue/events'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def venue_index(request):
    venue = Venue.objects.filter(user = request.user)
    return render(request, 'venue/index.html', {'venue': venue})

@login_required
def venue_detail(request, venue_id):
    venue = Venue.objects.get(id=venue_id)


    return render(request, 'venue/detail.html', {
        'venue': venue, 
        # 'event': eventdetails or all future events
    })

@login_required
def add_event(request, venue_id):
    form = EventForm(request.POST)

    if form.is_valid():
        new_event = form.save(commit=False)
        new_event.venue_id = venue_id
        new_event.save()
    return redirect('detail', venue_id=venue_id)