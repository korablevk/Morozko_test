from decimal import Decimal
from products.models import ProductProxy


class Cart:

    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get('session_key')

        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']  # Рассчитываем итоговую сумму
            yield item


    def add(self, product, quantity=1):
        """
        Добавляет продукт в корзину, если его там еще нет.
        Если продукт уже в корзине, ничего не делает.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}

        self.session.modified = True


    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True


    def update(self, cart_id, quantity):
        if cart_id in self.cart:
            self.cart[cart_id]['quantity'] = quantity
            self.save()


    def save(self):
        self.session.modified = True


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
