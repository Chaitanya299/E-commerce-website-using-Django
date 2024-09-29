from django.db import models
from django.core.validators import MinValueValidator

class promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()
    #products
    
class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']

class Product(models.Model): 
    
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    description=models.TextField(null=True, blank=True)
    unit_price=models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory=models.IntegerField(validators=[MinValueValidator(0)])
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(promotion,blank=True  )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']
  
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
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering=['first_name','last_name']
               
class Order(models.Model):
    
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
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
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