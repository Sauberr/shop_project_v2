from decimal import Decimal

from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        self.coupon = None
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def apply_coupon(self, coupon_code):
        if coupon_code == 'sauberr':
            self.coupon = coupon_code

    def remove_coupon(self):
        self.coupon = None

    def get_discounted_total(self):
        total = self.get_total()
        if self.coupon == 'sauberr':
            discount = Decimal('0.8')
            return total * discount
        return total

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        product_quantity = qty
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

