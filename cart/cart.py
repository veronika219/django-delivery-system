from menu.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def get_total_items(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_cart(self):
        return self.cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}

        self.cart[product_id]["quantity"] += quantity
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)

        if product_id in self.cart:
            if quantity <= 0:
                self.remove(product_id)
            else:
                self.cart[product_id]["quantity"] = quantity
                self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop("cart", None)
        self.session.modified = True

    def get_products(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_item_total(self, product_id):
        product = Product.objects.get(id=product_id)
        return product.price * self.cart.get(str(product_id), {}).get("quantity", 0)

    def get_total_price(self):
        products = self.get_products()
        total = 0

        for product in products:
            total += product.price * self.cart[str(product.id)]["quantity"]

        return total

    def get_quantity(self, product_id):
        return self.cart.get(str(product_id), {}).get("quantity", 0)

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
