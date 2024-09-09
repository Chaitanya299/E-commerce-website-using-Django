from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Value, F, Func, Q
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, orderItem

# Create your views(action) here.
# request handler 
# action or views


def say_hello(request):
    
    queryset=Product.objects.order_by('-title')
   
    return render(request,'hello.html',{'name':'chaitu','products':list(queryset)})

  