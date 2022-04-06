import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from utilities.decorators import check_token
from products.models import *

class MainProductView(View):
    def get(self, request):
        main_category = request.GET.get('main', None)
        sorting       = request.GET.get('order-by', 'latest')
        categories    = request.GET.getlist('sub', None)
        characters    = request.GET.getlist('character', None)
        offset        = int(request.GET.get('offset', 0))
        limit         = int(request.GET.get('limit', 8))

        sorting_dict = {
            'low-price' : 'price',
            'high-price': '-price',
            'latest'    : '-pk'
        }

        q = Q()
        if main_category:
            q &= Q(category__main_category__title=main_category)
        if categories:
            q &= Q(category__title__in=categories)
        if characters:
            q &= Q(character__name__in=characters)
            
        filtered_products = Product.objects.filter(q)
        products          = filtered_products.order_by(sorting_dict[sorting])[offset:offset+limit]
        total_count       = filtered_products.count()

        product_list = [{
            'id'           : product.id,
            'name'         : product.name,
            'price'        : product.price,
            'images'       : [image.image_url for image in product.images.all()],
            'detail'       : product.detail,
            'character'    : product.character.name,
            'stock'        : [{
                product_size.size.size_tag : product_size.stock
            } for product_size in product.sizes.all()]
        } for product in products] 

        return JsonResponse({'result' : product_list, 'count' : total_count}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)

            result = {
                'id'           : product.id,
                'name'         : product.name,
                'price'        : product.price,
                'images'       : [image.image_url for image in product.images.all()],
                'detail'       : product.detail,
                'character'    : product.character.name,
                'stock': [{
                    product_size.size.size_tag: product_size.stock
                } for product_size in ProductSize.objects.filter(product = product)],
                'reviews' : [{
                    'review_id' : review.id,
                    'user'      : {
                        'first_name': review.user.last_name,
                        'last_name' : review.user.first_name,
                        'email'     : review.user.email
                        },
                    'content'   : review.content,
                    'created_at': review.created_at
                }for review in product.reviews.all()]
            }
        
            return JsonResponse({'result' : result}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=404)
    
    @check_token
    def post(self, request, product_id):
        try:
            data    = json.loads(request.body)
            product = Product.objects.get(id = product_id)
            user    = request.user

            Review.objects.create(
                user    = user,
                product = product,
                content = data['content']
            )

            return JsonResponse({'message' : 'CREATED'}, status=201)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=404)        
    
    @check_token
    def delete(self, request, product_id):
        review_id = request.GET.get('review-id', None)
        user      = request.user
        reviews   = Review.objects.filter(id = review_id, product_id =product_id ,user = user)

        if not reviews.exists():
            return JsonResponse({'message' : 'REVIEW_NOT_EXIST'}, status = 404)
        
        reviews.delete()
        return JsonResponse({'message' : 'SUCCESS'}, status = 204)