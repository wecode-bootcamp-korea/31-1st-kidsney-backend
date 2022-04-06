import json

from django.views import View
from django.http import HttpResponse, JsonResponse

from products.models import Product, ProductSize, Size
from .models import Cart
from utilities.decorators import check_token
 
class PostCartView(View):
    @check_token
    def post(self, request, product_id):
        try:
            data         = json.loads(request.body)
            size         = Size.objects.get(size_tag = data['size'])
            quantity     = data['quantity']
            product      = Product.objects.get(id = product_id)
            product_size = ProductSize.objects.get(product = product, size = size)

            if not Cart.objects.filter(user = request.user, product_size = product_size).exists():
                Cart.objects.create(
                user         = request.user,
                product_size = product_size,
                quantity     = quantity
                )

                return HttpResponse(status=201)


            cart = Cart.objects.get(user = request.user, product_size = product_size)
            cart.quantity += quantity
            cart.save()
            
            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ProductSize.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status = 404)

class GetCartView(View):
    @check_token
    def get(self, request):
        user  = request.user
        carts = Cart.objects.filter(user = user)

        carts = [{
            'id': cart.id,
            'product': {
                'id'      : cart.product_size.product_id,
                'name'    : cart.product_size.product.name,
                'images'  : [image.image_url for image in cart.product_size.product.images.all()],
                'size'    : cart.product_size.size.size_tag,
                'quantity': cart.quantity,
                'stock'   : cart.product_size.stock,
                'price'   : cart.product_size.product.price  
            },
            'total_price' : cart.quantity*cart.product_size.product.price
        } for cart in carts]
        
        return JsonResponse({'carts' : carts}, status=200)

class UpdateCartView(View):
    @check_token
    def delete(self, request, cart_id):
        try:
            Cart.objects.get(user = request.user, id = cart_id).delete()
            return HttpResponse(status = 204)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=404)
    
    @check_token
    def patch(self, request, cart_id):
        try:
            data     = json.loads(request.body)
            user     = request.user
            quantity = data['quantity']
            size     = Size.objects.get(size_tag = data['size'])
            cart     = Cart.objects.get(id = cart_id, user = user)
            
            if quantity < 1:
                return JsonResponse({'message' : 'SUB_ZERO_ERROR'}, status = 400)

            cart.product_size = ProductSize.objects.get(product = cart.product_size.product, size = size)
            cart.quantity     = quantity
            cart.save()

            return HttpResponse(status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=404)