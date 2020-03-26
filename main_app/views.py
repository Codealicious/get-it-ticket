from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# import uuid
# import boto3
from .models import Ticket, Venue, Event, Business
from .forms import EventForm, TicketForm

# # Create your views here.

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

def user_show_busnisses(request, user_id):
    businesses = Business.objects.all().filter(user_id=user_id)
    return render(request, 'business/business_admin.html', {'businesses': businesses})

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
    venues = Venue.objects.all().filter(business_id=business_id)
    # venues = Venue.objects.exclude(id__in = business.venues.all().values_list('id'))

    # venues = Venues.all()?
    return render(request, 'business/detail.html', {
        'business': business, 
        'venues': venues, 
    })



# VENUE ---------------------------------------------------------------------------------
class VenueCreate(LoginRequiredMixin, CreateView):
    model = Venue
    fields = ['name', 'capacity']

    def form_valid(self, form):
        form.instance.business = Business.objects.get(id=self.kwargs["business_id"])
        return super(VenueCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('business_detail', kwargs={'business_id': self.kwargs["business_id"]})

class VenueUpdate(LoginRequiredMixin, UpdateView):
    model = Venue
    fields = 'capacity'

def venue_delete(request, business_id, venue_id):
    Venue.objects.get(id=venue_id).delete()
    return redirect('business_detail', business_id=business_id)


    




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
    events = Event.objects.all().order_by('date')
    return render(request,'home.html', {'events' : events})

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