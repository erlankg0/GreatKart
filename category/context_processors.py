from category.models import Category


def get_categories_context(request):
    """Context Processors"""
    categories = Category.objects.all()
    return dict(categories=categories)
