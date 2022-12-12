from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from store.models import Product, CategoryMPTT


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


# AJAX запрос для загрузки все варианты цвета и размера
def get_product(request, product_slug):
    if is_ajax(request):
        try:
            product = Product.objects.get(slug=product_slug)
        except ConnectionError as Error:
            raise ConnectionError("Link not Fount")
        return render(request, 'store/product_detail.html', context={'product': product})
    else:
        raise ConnectionError("Link not Fount")

# is_ajax(request) - проверка на AJAX запрос
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
