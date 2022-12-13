from store.models import CategoryMPTT, Product, Size, Brand

"""Context processors"""


def get_categories_context_mptt(request):
    """get categories"""
    categories = CategoryMPTT.objects.all()
    return dict(categories_mptt=categories)


def get_sizes(request):
    sizes = Size.objects.all()
    return dict(sizes=sizes)


def get_brands(request):
    brands = Brand.objects.all()
    return dict(brands=brands)


def get_products(request):
    """get products """
    products = Product.objects.order_by('sold')
    return dict(products=products)


def get_current_ip(request):
    # получить текущий ip адрес
    ip = request.META['REMOTE_ADDR']
    return dict(ip=ip)
