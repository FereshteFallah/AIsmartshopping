from django.shortcuts import render,redirect
from . models import Product,Category
from reviews.models import Comment
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper,Sum, FloatField, Case, When
# Create your views here.

'''
def home(request):
    products=Product.objects.all()
    return render(request,'products/home.html',{'products':products})
'''



'''
def home(request):
    products=Product.objects.all()
    # محصولات پرطرفدار بر اساس میانگین امتیاز (نظرات)
    popular_products = Product.objects.annotate(
        avg_score=Avg('comments__score')
    ).order_by('-avg_score')[:10]

    recommended_products = []
    if request.user.is_authenticated:
        # دسته‌های محصولات مثبت که کاربر نظر داده
        favorite_categories = Comment.objects.filter(
            user=request.user, sentiment='positive'
        ).values_list('product__category', flat=True).distinct()

        # پیشنهاد محصولاتی از این دسته‌ها که کاربر قبلاً نظر نداده
        recommended_products = Product.objects.filter(
            category__in=favorite_categories
        ).exclude(
            comments__user=request.user
        ).distinct()[:10]

    context = {
        'popular_products': popular_products,
        'recommended_products': recommended_products,
        'products':products
    }
    return render(request, 'products/home.html', context)


'''



'''
def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

'''



def home(request):
    # فقط محصولاتی که حداقل یک کامنت دارند
    annotated = Product.objects.annotate(
        total_comments=Count('comments'),
        positive_comments=Count('comments', filter=Q(comments__sentiment='positive'))
    ).filter(total_comments__gt=0)   # مهم: محصولاتی که کامنت ندارند حذف می‌شوند

    # محاسبه sentiment_score = (positive_comments / total_comments) * 10
    annotated = annotated.annotate(
        sentiment_score=ExpressionWrapper(
            10.0 * F('positive_comments') / F('total_comments'),
            output_field=FloatField()
        )
    )

    # محصولات پرطرفدار: مرتب‌شده بر اساس نمره و سپس تعداد کامنت برای رفع تساوی
    popular_products = annotated.order_by('-sentiment_score', '-total_comments')[:10]

    # پیشنهادهای شخصی‌سازی‌شده (مثل قبل) — اگر کاربر وارد شده باشد
    recommended_products = []
    if request.user.is_authenticated:
        favorite_categories = Comment.objects.filter(
            user=request.user, sentiment='positive'
        ).values_list('product__category', flat=True).distinct()

        recommended_products = Product.objects.filter(
            category__in=favorite_categories
        ).exclude(
            comments__user=request.user
        ).annotate(
            total_comments=Count('comments'),
            positive_comments=Count('comments', filter=Q(comments__sentiment='positive'))
        ).filter(total_comments__gt=0).annotate(
            sentiment_score=ExpressionWrapper(
                10.0 * F('positive_comments') / F('total_comments'),
                output_field=FloatField()
            )
        ).order_by('-sentiment_score', '-total_comments')[:10]

    context = {
        'popular_products': popular_products,
        'recommended_products': recommended_products,
        'products': Product.objects.all(),  # اگر لازم داری بفرست
    }
    return render(request, 'products/home.html', context)



def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=slug)
    reviews = product.comments.all()  # یا هر ارتباطی که کامنت‌ها رو به محصول وصل می‌کنه

    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            if text:
                Comment.objects.create(
                    product=product,
                    user=request.user,
                    content=text,
                )
            return redirect(request.path)  # صفحه را رفرش کن بعد از ارسال نظر
        else:
            return redirect('account_login')  # هدایت به صفحه ورود


    total_comments = reviews.count()
    positive_comments = reviews.filter(sentiment='positive').count()
    score = 0

    if total_comments > 0:
        score = round((positive_comments / total_comments) * 10, 1)

    stars = round(score / 2)
    context = {
        'product': product,
        'reviews': reviews,
        'sentiment_score': score,
        'stars': stars,
    }
    return render(request, 'products/product_detail.html', context)



def product_all(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/products.html', context)