from django.contrib import admin

from store.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = (('title', 'slug',), 'brand', 'description', 'price', 'quantity', 'image', 'category')
    prepopulated_fields = {'slug': ('title',)}


