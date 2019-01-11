from adjacent import get_connection_parameters

from api.models import APIKey
from manager.models import City, State
from stock.models import Category, Store

def webclient_processor(request):
    categories = Category.objects.filter(parent=None, is_active=True)
    stores = Store.objects.filter(is_active=True)
    cities = City.objects.filter(is_active=True)
    states = State.objects.all()
    try:
        web_api_key = APIKey.objects.get(name='Web client API Key')
    except: 
        web_api_key = None
    centrifugo_params = get_connection_parameters(request.user)

    context = {
        'webclient_context_categories': categories,
        'webclient_context_stores': stores,
        'webclient_context_states': states,
        'webclient_context_cities': cities,
        'webclient_context_web_auth_token': web_api_key,
        'webclient_context_centrifugo_params': centrifugo_params
    }
    
    return context
