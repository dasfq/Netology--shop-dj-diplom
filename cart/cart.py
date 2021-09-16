from django.conf    import settings
from shop.models import Item
from decimal import Decimal

class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

    def add(self, item, quantity = 1, update_quantity = False):
        product_id = item.id


