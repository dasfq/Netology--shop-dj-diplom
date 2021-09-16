from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
max_length = 20


class Category(models.Model):
    name = models.CharField(max_length=max_length, verbose_name='Имя')

    class Meta:
        verbose_name='Категория товара'
        verbose_name_plural='Категории товара'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, default="", verbose_name='Заголовок')
    sub_title = models.CharField(max_length=200, null=False, default="", verbose_name='Подзаголовок')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey(Category, default="", null=False, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name='Статья'
        verbose_name_plural='Статьи'

    def __str__(self):
        return self.title


class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(default="", max_length=max_length)
    email = models.EmailField(verbose_name="email address", unique=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Item(models.Model):
    name = models.CharField(max_length=max_length, verbose_name='Наименование')
    image = models.ImageField(max_length=max_length, verbose_name='Картинка')
    description = models.CharField(max_length=max_length, verbose_name='Описание')
    category = models.ManyToManyField(Category, verbose_name='Категория товаров')
    price = models.PositiveIntegerField(default=0, verbose_name="Цена")

    class Meta:
        verbose_name='Товар'
        verbose_name_plural='Товары'

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    stars = models.PositiveIntegerField(verbose_name='Рейтинг')
    text = models.CharField(max_length=200, null=True, verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, verbose_name="Отзывы")

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  verbose_name="Пользователь")
    item = models.ManyToManyField(Item, through="CartInfo", verbose_name='Товар')

    class Meta:
        verbose_name='Корзина'
        verbose_name_plural='Корзины'

    def __str__(self):
        return str(self.user)

    def make_order(self):
        # user = self.cart.user
        # order = Order.objects.create(user=user)
        pass


class CartInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Объект корзины')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name='Корзина-инфо'
        verbose_name_plural='Корзины-информация'

    def __str__(self):
        return str(self.cart) + '-' + str(self.item)


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, through='OrderInfo')


class OrderInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)