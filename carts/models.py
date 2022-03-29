from django.db import models
from utilities.timestamp import TimeStamp

class Cart(TimeStamp):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def total_price(self):
        return self.quantity * self.product.price
    
    class Meta:
        db_table = 'carts'
        
        