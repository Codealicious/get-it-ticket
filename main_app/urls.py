from django.urls import path
from . import views

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('user/<int:user_id>/businesses/', views.user_show_busnisses, name='business_admin'),
    path('business/', views.BusinessCreate.as_view(), name='business_create'),
    path('business/<int:business_id>/', views.business_detail, name='business_detail'),
    path('venue/create/<int:business_id>/', views.VenueCreate.as_view(), name='venue_create'),
    path('business/<int:business_id>/venue/<int:venue_id>/delete/', views.venue_delete, name='venue_delete'),
    path('business/<int:business_id>/venue/<int:venue_id>/', views.venue_detail, name='venue_detail'),
    path('business/<int:business_id>/venue/<int:venue_id>/event/create/', views.EventCreate.as_view(), name='event_create'),
    # path('event/<int:pk>/update/', views.EventUpdate.as_view(), name='event_update'),
    # path('event/<int:pk>/delete/', views.EventDelete.as_view(), name='event_delete'),
]

         