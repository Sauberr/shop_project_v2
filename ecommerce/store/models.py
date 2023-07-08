from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:

        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:list-category', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='un-branded')
    description = models.TextField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    class Meta:

        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product-info', args=[self.slug])




