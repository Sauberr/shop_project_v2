from django.shortcuts import get_object_or_404, render

from store.models import Category, Product


def store(request):
    context = {'title': 'IGUS'}

    q = request.GET.get('q')
    context['my_products'] = Product.objects.filter(title__icontains=q) if q else Product.objects.all()

    return render(request, 'store/store.html', context)


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html',
                  {'category': category, 'products': products, 'title': 'Clothes'})


def product_info(request, product_slug):
    context = {
        'product': get_object_or_404(Product, slug=product_slug),
        'title': 'Detail page'
    }
    return render(request, 'store/product-info.html', context)





