from django.urls import path
from . import views



urlpatterns = [
  path('',views.homepage,name='home'),
  path('category/<str:category>/',views.category_list,name="category"),
  path('product/<slug:slug>/',views.post_content,name='post_content'),
]





