from django.db import models

class promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()
    #products
    
class collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product', on_delete=models.SET_NULL,null=True, related_name='+')

class Product(models.Model):
    
    title=models.CharField( max_length=255)
    slug=models.SlugField()
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(promotion)
  
class customer(models.Model):
    
    MEMBERSHIP_BRONZE='b'   
    MEMBERSHIP_SILVER='s'
    MEMBERSHIP_GOLD='g'
    
    MEMEBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'bronze'),
        (MEMBERSHIP_SILVER,'silver'),
        (MEMBERSHIP_GOLD,'gold'),
    ]
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMEBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    
    class Meta:
        db_table = 'store_customers'
        indexes=[
            models.Index(fields=['last_name','first_name'])
        ]
        
            
class order(models.Model):
    
    PAYEMENT_STATUS_PENDING='p'
    PAYEMENT_STATUS_COMPLETE='c'
    PAYEMENT_STATUS_FAILED='f'
    
    PAYEMENT_STATUS_CHOICES=[
        (PAYEMENT_STATUS_PENDING,'pending'),
        (PAYEMENT_STATUS_COMPLETE,'complete'),
        (PAYEMENT_STATUS_FAILED,'failed'),
    ]
    
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1,choices=PAYEMENT_STATUS_CHOICES,default=PAYEMENT_STATUS_PENDING)
    customer=models.ForeignKey(customer,on_delete=models.PROTECT)
     
class orderItem(models.Model):
    order=models.ForeignKey(order,on_delete=models.PROTECT)
    Product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    
class address(models.Model): 
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    
class cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    
class cartItem(models.Model):
    cart=models.ForeignKey(cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()