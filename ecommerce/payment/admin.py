from django.contrib import admin

from payment.models import ShippingAddress, Order, OrderItem


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    fields = ('full_name', 'address1', 'city', 'address2', 'state', 'zipcode', 'user'  )
    search_fields = ('full_name',)
    ordering = ('full_name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    fields = ('full_name', 'email', 'shipping_address', 'amount_paid', 'date_ordered', 'user')
    readonly_fields = ('date_ordered',)
    search_fields = ('full_name',)
    ordering = ('full_name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order',)
    fields = ('order', 'product', 'quantity', 'price', 'user')
    search_fields = ('order',)
    ordering = ('order',)
