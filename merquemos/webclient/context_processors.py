from stock.models import Category, Store
from api.models import APIKey
from manager.models import City

def webclient_processor(request):
    categories = Category.objects.all()
    stores = Store.objects.all()
    cities = City.objects.all()
    web_api_key = APIKey.objects.get(name='Web client API Key')

    context = {
        'webclient_context_categories': categories,
        'webclient_context_stores': stores,
        'webclient_context_cities': cities,
        'webclient_context_web_auth_token': web_api_key
    }
    
    return context
