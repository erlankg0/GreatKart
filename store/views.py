from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from store.models import Product, CategoryMPTT, ProductVariant, Brand, Size, Color


class HomeView(ListView):
    """Вывод главной страницы"""
    model = Product
    context_object_name = 'products'
    template_name = 'store/index.html'


class ShopListView(HomeView):
    """Вывод всех продуктов"""
    template_name = 'store/shop.html'
    paginate_by = 9

    def get_queryset(self):
        """Переопеределю метод для вывода продуктов которые для продажи"""
        queryset = Product.objects.filter(is_active=True).order_by(
            '-is_new')  # is_active=True - продукты для продажи is_new=True - новые продукты
        return queryset


def index(request):
    return render(request, 'store/forms.html')


class ShopByCategoryListView(ShopListView):
    """Вывод всех продуктов по категориям"""

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дабавление дополнительных данных в context"""
        context = super(ShopByCategoryListView, self).get_context_data(**kwargs)
        print(self.kwargs['slug'])
        context['get_category_name'] = CategoryMPTT.objects.get(
            slug=self.kwargs['slug'])  # добавлю дополнительные данные
        return context

    def get_queryset(self):  # переопределяю метод для вывода продуктов по категориям и для продажи
        """Переопеределю метод для вывода продуктов по категории которые для продажи"""
        queryset = Product.objects.filter(
            Q(category__slug=self.kwargs['slug']) | Q(category__parent__slug=self.kwargs['slug']),
            is_active=True).order_by('-is_new')  # is_active=True - продукты для продажи is_new=True - новые продукты
        return queryset


class ShopByBrandListView(ShopListView):
    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(brand__slug=self.kwargs['slug']))  # добавлю дополнительные данные
        return queryset


class DetailProduct(View):
    """Вывод одного(отдельного) продукта"""

    def get(self, request, product_slug):
        """Плохой код надо исправить с DetailView"""
        try:
            """Не знаю как сделать мульти slug"""
            product = Product.objects.get(
                slug=product_slug,
            )
        except ConnectionError as Error:
            raise ConnectionError("Link not Fount")
        return render(request, 'store/product_detail.html', context={'product': product})


def is_ajax(request):  # проверка на ajax запрос
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


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
