from store.models import CategoryMPTT


def get_categories_context_mptt(request):
    """Context Processors"""
    categories = CategoryMPTT.objects.all()
    return dict(categories_mptt=categories)
