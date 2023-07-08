from django.urls import path

from store.views import list_category, product_info, store

app_name = 'store'

urlpatterns = [
    # Store main page
    path('', store, name='store'),
    # Individual page
    path('product/<slug:product_slug>/', product_info, name='product-info'),
    # Individual category
    path('search/<slug:category_slug>/', list_category, name='list-category'),

]