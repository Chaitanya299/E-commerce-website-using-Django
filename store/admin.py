from django.db.models.aggregates import Count
from django.contrib import admin, messages
from django.urls import reverse
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.http import HttpRequest
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'
    
    def lookups(self, request, model_admin):
        return[
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['collection']
    actions=['clear_inventory']
    search_fields = ['title']
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=[
        'collection',
        'last_update',
        InventoryFilter]
    list_display=[
        'title',
        'unit_price',
        'inventory_status',
        'collection_title']
    prepopulated_fields={
        'slug':['title']
        }
    
    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory <10:
            return 'Low'
        return 'ok'
    
    @admin.action(description='clear inventory')
    def clear_inventory(self,request,query_set):
        updated_count=query_set.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were sucessfuly updated.',  
            messages.ERROR
        )
           
@admin.register(models.customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields=['first_name','last_names']
    list_display=['first_name','last_name','membership','orders']
    list_editable=['membership']
    list_per_page=10
    ordering=['first_name','last_name']
    search_fields=['first_name','last_name']
    
    @admin.display(ordering='orders')
    def orders(self,customer):
        url=(
            reverse('admin:store_order_changelist')
            +'?'
            +urlencode({
                'customer__id':str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>',url,customer.orders)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )
    
class OrderItemInline(admin.TabularInline):
    autocomplete_fields=['Product']
    min_num=1
    max_num=10
    model=models.orderItem
    extra=0
    
@admin.register(models.Order)  
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    inlines=[OrderItemInline]
    list_display=['id','placed_at','customer'] 
    list_select_related=['customer']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
    search_fields=['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection): 
        url=(
            reverse('admin:store_product_changelist')
            +'?'
            +urlencode({
                'collection __id':str(collection.id)
            })
            )
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
         
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )