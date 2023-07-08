from django.urls import include, path

from payment.views import *

app_name = 'payment'

urlpatterns = [
    path('payment-success/', payment_success, name='payment-success'),
    path('payment-failed/', payment_failed, name='payment-failed'),
    path('checkout/', checkout, name='checkout'),
    path('complete_order/', complete_order, name='complete-order'),
]