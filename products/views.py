from django.http import JsonResponse
from django.views import View

from .models import Product, Image, Character, Category, MainCategory, Size, ProductSize

class ProductsView(View):
    def get(self, request):
        # :8000/products?main=boy&sub=tops,pants,acc
        main = request.GET.get('main')
        subs = request.GET.get('sub')

        if subs == None:
            main_category = MainCategory.objects.get(title = main)
            categories    = Category.objects.filter(main_category = main_category)
            product_list  = []

            for category in categories:
                products = Product.objects.filter(category = category)
                product_list += [{
                    'id'           : product.id,
                    'name'         : product.name,
                    'price'        : product.price,
                    'images'       : [image.image_url for image in product.images.all()],
                    'detail'       : product.detail,
                    'character'    : product.character.name,
                    'product_sizes': [{
                        product_size.size.size_tag : product_size.stock
                    } for product_size in ProductSize.objects.filter(product = product)]
                } for product in products]

            return JsonResponse({'result' : product_list, "count" : len(product_list) }, status = 200)
        
        elif subs != 'none_sub':
            sub_lst = subs.split(',')
            sub_products = []
            
            for sub in sub_lst:
                sub_categories = Category.objects.filter(title = sub)
                for sub_category in sub_categories:
                    if sub_category in MainCategory.objects.get(title = main).categories.all():
                        sub_products += [{
                            'id'           : sub_product.id,
                            'name'         : sub_product.name,
                            'price'        : sub_product.price,
                            'images'       : [image.image_url for image in sub_product.images.all()],
                            'detail'       : sub_product.detail,
                            'character'    : sub_product.character.name,
                            'product_sizes': [{
                                product_size.size.size_tag : product_size.stock
                            } for product_size in ProductSize.objects.filter(product = sub_product)]
                        } for sub_product in Product.objects.filter(category = sub_category)]
                    
                    else:
                        return JsonResponse({'message' : 'IVALID_URL'}, status = 400)
                
            return JsonResponse({'result' : sub_products, "count" : len(sub_products) }, status = 200)