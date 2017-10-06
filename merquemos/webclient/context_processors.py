from adjacent import get_connection_parameters

from api.models import APIKey
from manager.models import City
from stock.models import Category, Store

def webclient_processor(request):
    categories = Category.objects.filter(parent=None)
    stores = Store.objects.all()
    cities = City.objects.all()
    web_api_key = APIKey.objects.get(name='Web client API Key')
    centrifugo_params = get_connection_parameters(request.user)

    context = {
        'webclient_context_categories': categories,
        'webclient_context_stores': stores,
        'webclient_context_cities': cities,
        'webclient_context_web_auth_token': web_api_key,
        'webclient_context_centrifugo_params': centrifugo_params
    }
    
    return context
