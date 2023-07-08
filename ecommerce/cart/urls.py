from django.urls import include, path

from cart.views import cart_add, cart_delete, cart_summary, cart_update, cart_clear

app_name = 'cart'

urlpatterns = [
    path('', cart_summary, name='cart-summary'),
    path('add/', cart_add, name='cart-add'),
    path('delete/', cart_delete, name='cart-delete'),
    path('update/', cart_update, name='cart-update'),
    path('clear/', cart_clear, name='cart-clear'),
]