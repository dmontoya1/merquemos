from stock.models import Category, Store

def webclient_processor(request):
    categories = Category.objects.all()
    stores = Store.objects.all()

    context = {
        'webclient_context_categories': categories,
        'webclient_context_stores': stores
    }
    
    return context
