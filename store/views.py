from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, FormView, CreateView

from store.models import Product, CategoryMPTT, ProductVariant, Size, Like, Ip
from store.forms import LikeForm


class HomeView(ListView):
    """Вывод главной страницы"""
    model = Product  # модель для вывода товаров
    context_object_name = 'products'  # имя объекта в контексте
    template_name = 'store/index.html'  # имя шаблона

    def get_context_data(self, **kwargs):  # метод для добавления дополнительных данных в контекст
        context = super().get_context_data(**kwargs)  # получение контекста
        context['products'] = Product.objects.order_by('-view')[0:16]  # 16 самых популярных товаров
        return context  # возвращение контекста


class ShopListView(HomeView):
    """Вывод всех продуктов"""
    template_name = 'store/shop.html'  # переопределю шаблон для вывода продуктов
    paginate_by = 16  # пагинация

    def get_queryset(self):
        """Переопеределю метод для вывода продуктов которые для продажи"""
        queryset = Product.objects.filter(is_active=True).order_by('-is_new')
        # is_active=True - продукты для продажи is_new=True - новые продукты
        return queryset


class ShopByCategoryListView(ShopListView):
    """Вывод всех продуктов по категориям"""

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дабавление дополнительных данных в context"""
        context = super(ShopByCategoryListView, self).get_context_data(**kwargs)  # получение контекста
        context['get_category_name'] = CategoryMPTT.objects.get(
            slug=self.kwargs['slug'])  # добавлю дополнительные данные
        return context  # возвращение контекста

    def get_queryset(self):  # переопределяю метод для вывода продуктов по категориям и для продажи
        """Переопеределю метод для вывода продуктов по категории которые для продажи"""
        queryset = Product.objects.filter(
            Q(category__slug=self.kwargs['slug']) | Q(category__parent__slug=self.kwargs['slug']),
            is_active=True).order_by('-is_new')  # is_active=True - продукты для продажи is_new=True - новые продукты
        return queryset


class ShopByBrandListView(ShopListView):  # вывод продуктов по бренду
    def get_queryset(self):  # переопределяю метод для вывода продуктов по бренду и для продажи
        queryset = Product.objects.filter(
            Q(brand__slug=self.kwargs['slug']))  # добавлю дополнительные данные
        return queryset  # возвращение контекста


class DetailProduct(View):
    """Вывод одного(отдельного) продукта"""

    def get(self, request, product_slug):
        """Плохой код надо исправить с DetailView"""
        try:
            """Не знаю как сделать мульти slug"""
            product = Product.objects.get(
                slug=product_slug,
            )
        except ConnectionError:
            raise ConnectionError("Link not Fount")
        return render(request, 'store/product_detail.html', context={'product': product, })


# AJAXs

def is_ajax(request):  # проверка на ajax запрос
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_like(request, product_id, ip_address):  # ajax запрос для добавления лайка
    if is_ajax(request):  # проверка на ajax запрос
        product = Product.objects.get(id=product_id)  # получаю продукт
        ip = Ip.objects.get_or_create(ip=ip_address)[0]  # получаю ip адресс
        like = Like.objects.get_or_create(product=product, ip=ip)  # добавляю лайк в базу данных
        return JsonResponse({'status': 'ok'})
    return HttpResponseNotAllowed('Method not allowed')


# ajax запрос для size в ProductVariant
def get_size(request, variant_id):
    if is_ajax(request):
        variant = ProductVariant.objects.get(id=variant_id)  # получаю вариант продукта
        size = variant.size.all().values()  # получаю все значения size
        return JsonResponse({'size': list(size)})  # возвращаю json
    else:
        # return HttpResponseBadRequest()  # если не ajax запрос то вернет 400
        variant = ProductVariant.objects.get(id=variant_id)  # получаю вариант продукта
        size = variant.size.all().values()  # получаю все значения size
        return JsonResponse({'size': list(size)})  # возвращаю json


# ajax запрос для получения цены у size
def get_price(request, size_id):
    print("AJAX")
    if is_ajax(request):
        size = Size.objects.get(id=size_id)
        price = size.price
        quantity = size.quantity
        return JsonResponse({'price': price, 'quantity': quantity})
    else:
        size = Size.objects.get(id=size_id)
        price = size.price
        quantity = size.quantity
        return JsonResponse({'price': price, 'quantity': quantity})
