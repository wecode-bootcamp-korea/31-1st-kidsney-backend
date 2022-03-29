from django.db import models

from utilities.timestamp import TimeStamp
from users.models import User

class MainCategory(models.Model): 
    title = models.CharField(max_length=200)

    class Meta: 
        db_table = 'main_categories'

class Category(models.Model): 
    title         = models.CharField(max_length=200)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='categories')

    class Meta: 
        db_table = 'categories'

class Character(models.Model): 
    name = models.CharField(max_length=200)

    class Meta: 
        db_table = 'characters'

class Product(TimeStamp): 
    name      = models.CharField(max_length=200)
    price     = models.DecimalField()
    detail    = models.TextField()
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='products')

    class Meta: 
        db_table = 'products'

class Image(models.Model): 
    image_url = models.CharField(max_length=2000)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta: 
        db_table = 'images'

class Size(models.Model): 
    size_tag = models.CharField(max_length=100)

    class Meta: 
        db_table = 'sizes'

class ProductSize(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size    = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='products')
    stock   = models.IntegerField()

    class Meta: 
        db_table = 'products_sizes'

class Review(TimeStamp): 
    content = models.TextField()
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=Category, related_name='reviews')

    class Meta:
        db_table = 'reviews'