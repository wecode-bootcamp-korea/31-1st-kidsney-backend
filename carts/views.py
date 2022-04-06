import json

from django.views import View
from django.http import JsonResponse

from products.models import Product, ProductSize, Size
from .models import Cart
from utilities.decorators import check_token
 
class CartView(View):
    @check_token
    def post(self, request):
        try:
            data         = json.loads(request.body)
            product_id   = request.GET.get('product-id')
            size         = Size.objects.get(size_tag = data['size'])
            quantity     = data['quantity']
            user         = request.user
            product      = Product.objects.get(id = product_id)
            product_size = ProductSize.objects.get(product = product, size = size)
            stock        = product_size.stock

            cart, is_created = Cart.objects.get_or_create(
                user         = user,
                product_size = product_size
            )
            
            if cart.quantity + quantity <= stock:
                cart.quantity += quantity
                cart.save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 201)

            if cart.quantity == 0:
                cart.delete()
            return JsonResponse({'message' : 'NOT_ENOUGH_STOCK'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ProductSize.DoesNotExist:
            return JsonResponse({'message' : 'SIZE_NOT_EXIST'}, status = 404)

    @check_token
    def get(self, request):
        user  = request.user
        carts = Cart.objects.filter(user = user)

        carts = [{
            'cart_id': cart.id,
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
   
    @check_token
    def delete(self, request):
        try:
            user    = request.user
            cart_id = request.GET.get('cart-id')
            if not cart_id:
                return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=404)

            Cart.objects.get(user = user, id = cart_id).delete()
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=404)
    
    @check_token
    def patch(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            cart_id  = request.GET.get('cart-id')
            quantity = data['quantity']
            
            if not cart_id:
                return JsonResponse({'message' : 'WRONG_URL'}, status = 404)
            if quantity < 1:
                return JsonResponse({'message' : 'SUB_ZERO_ERROR'}, status = 400)

            cart = Cart.objects.get(id = cart_id, user = user)
            if not quantity <= cart.product_size.stock:
                return JsonResponse({'message' : 'NOT_ENOUGH_STOCK'}, status = 400)

            cart.quantity = quantity
            cart.save()

            return JsonResponse({
                'message' : 'SUCCESS',
                'quantity' : cart.quantity
            }, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=404)