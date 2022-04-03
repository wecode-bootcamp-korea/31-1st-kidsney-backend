import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

from products.models import *

class MainProductView(View):
    def get(self, request):
        try:
            main_category = request.GET.get('main', None)
            category      = request.GET.getlist('sub', None)
            sorting       = request.GET.get('order-by', 'latest')
            character     = request.GET.getlist('character', None)
            page          = request.GET.get('page', 1)
            
            sorting_dict = {
                'low-price' : 'price',
                'high-price': '-price',
                'latest' : '-pk'
            }

            q = Q()
            if main_category:
                q &= Q(category__main_category__title=main_category)
            if category:
                q &= Q(category__title__in=category)
            if character:
                q &= Q(character__name__in=character)
          
            products    = Product.objects.filter(q).order_by(sorting_dict[sorting])
            total_count = len(products)
            
            paginator = Paginator(products, 8)
            page_obj  = paginator.page(page)
            

            product_list = [{
                'id'           : product.id,
                'name'         : product.name,
                'price'        : product.price,
                'images'       : [image.image_url for image in product.images.all()],
                'detail'       : product.detail,
                'character'    : product.character.name,
                'product_sizes': [{
                    product_size.size.size_tag : product_size.stock
                } for product_size in ProductSize.objects.filter(product = product)]
            } for product in page_obj]
           
            return JsonResponse({'result' : product_list, 'count' : total_count}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=400)
        except EmptyPage:
            return JsonResponse({'message' : 'PAGE_NOT_EXIST'}, status=400)