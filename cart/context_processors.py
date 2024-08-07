from .cart import Cart

def cart(request):
    if request.user.is_authenticated:
        return {'cart': Cart(request)}
    else:
        return {'cart': list()}