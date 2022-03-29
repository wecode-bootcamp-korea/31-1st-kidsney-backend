from django.db import models
from utilities.timestamp import TimeStamp

class User(TimeStamp):
    first_name    = models.CharField(max_length=50)
    last_name     = models.CharField(max_length=30)
    email         = models.CharField(max_length=50, unique=True)
    password      = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    phone_number  = models.CharField(max_length=25)
    
    class Meta:
        db_table = 'users'
        
class Address(models.Model):
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    location       = models.CharField(max_length=150)
    detail_address = models.CharField(max_length=100)
    zip_code       = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'addresses'
        
class Wishlist(models.Model):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'wishlists'
        # constraints = [models.UniqueConstraint(
        #     fields = ['user', 'product'],
        #     name = 'wishlists_user_product_unq'
            
        #     )
        # ] 
        
        