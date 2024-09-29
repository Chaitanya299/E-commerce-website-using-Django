from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from store.models import Collection, Product, orderItem, Order, customer

# Create your views(action) here.
# request handler 
# action or views


def say_hello(request):
    
    queryset=Product.objects.raw('select * from store_product')
        
    return render(request,'hello.html',{'name':'chaitu','result': list(queryset)})
