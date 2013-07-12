from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from allegro.lib import allegro_api, NoItemException as AllegroNoItemEx
from nokaut.lib import nokaut_api, NoItemException as NokautNoItemEx

from sqlalchemy import and_,desc

from .models import (
    DBSession,
    UsersTable,
    SearchTable
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

@view_config(route_name='home', renderer='pyramid_app:templates/search_box.mako')
def my_view(request):

    user_id =  authenticated_userid(request)
    return {'logged' : user_id}


@view_config(route_name = 'search', renderer = 'pyramid_app:templates/search.mako')
def res_view(request):
    search_phrase = request.GET.get('search_field')
    nokaut_key = request.registry.settings.get('nokaut.key')
    user_id =  authenticated_userid(request)

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

    if user_id is not None:
        prev = DBSession.query(SearchTable).filter(and_(SearchTable.search_id == user_id, SearchTable.search_content == search_phrase)).first()
        if prev is not None:
            prev.search_quantity += 1
        else:
            search = SearchTable(user_id,search_phrase, all_link or '#', all_price or 0, nok_link or '#', nok_price or 0, 0)
            DBSession.add(search)

    return {
            'logged': user_id,
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
    user_id =  authenticated_userid(request)
    user_hist = DBSession.query(SearchTable).filter(SearchTable.search_id == user_id).all()
    hist = [item.to_str() for item in user_hist]

    return {'logged' : user_id,
            'search_list': hist
    }

@view_config(route_name = 'top_search', renderer = 'pyramid_app:templates/top.mako')
def top_search_view(request):
    top = DBSession.query(SearchTable).order_by(desc(SearchTable.search_quantity))
    top_search = [item.to_str() for item in top[:3]]
    top_res = [(item[1], item[-1]) for item in top_search]
    user_id = authenticated_userid(request)

    return {'logged' : user_id,
            'top_search' : top_res
    }


@view_config(route_name = 'login', renderer = 'pyramid_app:templates/login.mako')
def login_view(request):
    resp = {
        'error' : False
    }
    if request.method == 'POST':
        login, passwd = request.POST.get('login'), request.POST.get('password')
        user = DBSession.query(UsersTable).filter(and_(UsersTable.username == login, UsersTable.password == passwd)).first()

        if user is None:
            resp['error'] = 'Wrong login or password..'
        else:
            headers = remember(request, user.id)
            return HTTPFound(location = '/', headers = headers)

    return resp

@view_config(route_name = 'logout', renderer = 'pyramid_app:templates/base.mako')
def logut_view(request):
    headers = forget(request)
    return HTTPFound(location = '/', headers = headers)


@view_config(route_name = 'register', renderer = 'pyramid_app:templates/register.mako')
def register_view(request):
    resp = {
        'error' : False
    }
    login, passwd, conf_passwd = request.POST.get('login'), request.POST.get('password'), request.POST.get('confirm_password')

    if request.method == 'POST':
        log = DBSession.query(UsersTable).filter(UsersTable.username == login).first()

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
            DBSession.add(new_user)
            user_id = DBSession.query(UsersTable).filter(UsersTable.username == new_user.username).first().id
            headers = remember(request, user_id)
            return  HTTPFound('/', headers = headers)
    else:
        return resp

@view_config(route_name = 'user_list', renderer = 'pyramid_app:templates/user_list.mako')
def user_list_view(request):
    """ ZROBIONE TYLKO W CELU PODGLADU ..
    """
    u_list = DBSession.query(UsersTable).all()
    users = [user.to_str() for user in u_list]
    history_ = DBSession.query(SearchTable).all()
    hist = [item.to_str() for item in history_]
    return {'user_list': users, 'hist': hist}
