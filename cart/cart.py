from menu.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0
            }
        self.cart[product_id]['quantity'] += quantity

        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id  in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.session.modified = True

    def get_products(self):
        products_ids = self.cart.keys()
        return Product.objects.filter(id__in=products_ids)

    def get_total_price(self):
        products = self.get_products()
        total = 0
        for product in products:
            total += (product.price * self.cart[str(product.id)]['quantity'])

        return total

