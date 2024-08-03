from django.urls import path 
from . import views     # importing view function from current folder

urlpatterns=[
    path('hello/',views.say_hello)  #url configuration  
]
