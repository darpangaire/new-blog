from django.urls import path
from . import views

urlpatterns = [
  path('stockpicker/',views.stockpicker_post,name = 'stockpicker'),
  path('stocktracker/',views.stocktracker_post,name = 'stocktracker'),
  
]


