from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from allegro.lib import allegro_api, NoItemException as AllegroNoItemEx
from nokaut.lib import nokaut_api, NoItemException as NokautNoItemEx

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    UsersTable,
    SearchTable
    )


@view_config(route_name='home', renderer='pyramid_app:templates/base.mako')
def my_view(request):
    # try:
    #     one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response('db not working', content_type='text/plain', status_int=500)
    return {}


@view_config(route_name = 'search', renderer = 'pyramid_app:templates/search.mako')
def res_view(request):
    search_phrase = request.GET.get('search_field')
    nokaut_key = request.registry.settings.get('nokaut.key')

    try :
        all = allegro_api(search_phrase)
    except AllegroNoItemEx:
        all = (None, None)

    try:
        nok = nokaut_api(search_phrase,nokaut_key)
    except NokautNoItemEx:
        nok = (None, None)

    nok_price, nok_link = nok[1], nok[0]
    all_price, all_link = all[1], all[0]

    if (nok_price == None and all_price == None) or (nok_price == all_price):
        all_mode, nok_mode = '', ''
    elif nok_price != None and all_price == None:
        all_mode, nok_mode = '', 'win'
    elif nok_price == None and all_price != None:
        all_mode, nok_mode = 'win', ''
    else :
        if all_price < nok_price:
            all_mode, nok_mode = 'win', ''
        elif all_price > nok_price:
            all_mode, nok_mode = '', 'win'

    return {
            'product_name' : search_phrase,
            'allegro_link' : all_link,
            'nokaut_link' : nok_link,
            'allegro_price' : all_price,
            'nokaut_price' : nok_price,
            'allegro_price_mode' : all_mode,
            'nokaut_price_mode' : nok_mode
        }

@view_config(route_name = 'history', renderer = 'pyramid_app:templates/history.mako')
def history_view(request):
    return {'search_list': [('name1','price1','link1'),('name2','price2','link2'),('name3','price3','link3')]}

@view_config(route_name = 'login', renderer = 'pyramid_app:templates/login.mako')
def login_view(request):
    print request
    return {}

@view_config(route_name = 'register', renderer = 'pyramid_app:templates/register.mako')
def register_view(request):
    if request.method == 'POST':
        print request.GET.get('login'), request.GET.get('password'), request.GET.get('confirm_password')

    return {}

