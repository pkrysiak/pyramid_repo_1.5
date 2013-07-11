from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from allegro.lib import allegro_api, NoItemException as AllegroNoItemEx
from nokaut.lib import nokaut_api, NoItemException as NokautNoItemEx

from sqlalchemy.exc import DBAPIError
from sqlalchemy import and_

from .models import (
    DBSession,
    UsersTable,
    # SearchTable
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid
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



@view_config(route_name = 'login', renderer = 'pyramid_app:templates/login.mako', permission = 'all')
def login_view(request):
    resp = {
        'error' : False
    }
    if request.method == 'POST':
        login, passwd = request.POST.get('login'), request.POST.get('password')
        user = DBSession.query(UsersTable).filter(and_(UsersTable.username == login)).first()
        try:
            passwd = user.password
        except AttributeError:
            passwd = None
        # print '->>>>>>>>',user, passwd
        if user is None:
            resp['error'] = 'No such user..'
        elif passwd is None:
            resp['error'] = 'Wrong password..'
        else:
            headers = remember(request, user.id)
            print '------->',headers
            # cos tutaj
    return resp

@view_config(route_name = 'register', renderer = 'pyramid_app:templates/register.mako', permission = 'all')
def register_view(request):
    resp = {
        'error' : False
    }
    login, passwd, conf_passwd = request.POST.get('login'), request.POST.get('password'), request.POST.get('confirm_password')

    # import ipdb;ipdb.set_trace()
    if request.method == 'POST':
        log = DBSession.query(UsersTable).filter(UsersTable.username == login).first()
        data = [item.to_str() for item in DBSession.query(UsersTable).all()]
        print 'log' , log, data
        if passwd != conf_passwd:
            resp['error'] = 'Passwords does not match..'
            return resp
        elif len(passwd) < 4:
            resp['error'] = 'Passwords is too short..'
        elif len(login) < 4:
            resp['error'] = 'Login is too short..'
        elif log is not None:
            resp['error'] = 'Login alredy taken, try another one..'
        else:
            new_user = UsersTable(login, passwd, 'viewer')
            print new_user.id
            DBSession.add(new_user)
            user_id = DBSession.query(UsersTable).filter(UsersTable.username == new_user.username).first().id
            headers = remember(request, user_id)
            # cos tu dalej jeszcze trzeba
        return resp

    else:
        return resp

@view_config(route_name = 'user_list', renderer = 'pyramid_app:templates/user_list.mako')
def user_list_view(request):
    u_list = DBSession.query(UsersTable).all()
    users = [user.to_str() for user in u_list]
    print users

    return {'user_list': users}
