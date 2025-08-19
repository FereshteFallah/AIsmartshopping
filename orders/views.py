from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Order, OrderItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

  
    order, created = Order.objects.get_or_create(user=request.user, status='pending')

  
    item, item_created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'price': product.price}
    )
    if not item_created:
        item.quantity += 1
        item.save()

    order.calculate_total_price()

    return redirect('cart_detail')



@login_required
def cart_detail(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    if order:
        for item in order.items.all():
            item.total_price = item.price * item.quantity
    return render(request, 'orders/cart_detail.html', {'order': order})
