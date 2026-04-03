from decimal import Decimal
from products.models import Product
from coupons.models import Coupon


class Cart(object):
    """ User Cart """

    def __init__(self, request):
        """ Initializing Cart """
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def save(self):
        """ Saving Cart in session """
        self.session['cart'] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity):
        """ Adding product to Cart """
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity,
            }
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def update(self, product_id, quantity):
        """ Update the quantity of products in Cart """
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def remove(self, product_id):
        """ Removing a product from Cart """
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ Iterating over products """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_quantity = self.cart[str(product.id)]['quantity']
            item = {
                'product': product,
                'quantity': product_quantity,
                'total_price': product.price * product_quantity,
            }
            yield item

    def __len__(self):
        """ Total number of items """
        return sum(value['quantity'] for value in self.cart.values())

    def get_total_price(self):
        """ Getting a total price of product """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return sum((product.price * self.cart[str(product.id)]['quantity']
                    for product in products), Decimal('0.00'))

    @property
    def coupon(self):
        """ Getting a coupon from the database """
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """ Getting a cost of the discount """
        if self.coupon:
            return (self.get_total_price()
                    * self.coupon.discount
                    / Decimal('100.00'))
        return Decimal('0.00')

    def get_total_cost(self):
        """ Getting a total cost taking into the discount """
        return round(self.get_total_price() - self.get_discount(), 2)

    def clear(self):
        """ Clearing Cart """
        del self.session['cart']
        self.session.modified = True
