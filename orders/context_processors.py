# cart/context_processors.py
from .models import Order

def cart_item_count(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='pending').first()
        count = order.items.count() if order else 0
    else:
        count = 0
    return {'cart_item_count': count}
