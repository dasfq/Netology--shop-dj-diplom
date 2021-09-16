from django.contrib import admin
from .models import Category, Article, CustomUser, Review, Item, Cart, Order, CartInfo, OrderInfo


class CategoryAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

class ItemAdmin(admin.ModelAdmin):
    pass

class CartAdmin(admin.ModelAdmin):
    pass

class CartInfoAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    # list_display = ("date", 'user')
    # inlines = ["date", 'user', 'item']
    pass

class OrderInfoAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartInfo, CartInfoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
