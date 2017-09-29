from stock.models import Category, Store
from manager.models import City

def webclient_processor(request):
    categories = Category.objects.all()
    stores = Store.objects.all()
    cities = City.objects.all()

    context = {
        'webclient_context_categories': categories,
        'webclient_context_stores': stores,
        'webclient_context_cities': cities
    }
    
    return context
