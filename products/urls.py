from django.urls import path
from products import views as product_views  


app_name = 'products'
urlpatterns = [  
    path('', product_views.home, name='home'),   
    path('<slug:category_slug>/<slug:slug>/', product_views.product_detail, name='product_detail'),
    
    ]

 
   