from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_app.security import groupfinder
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy import event
from .models import (
    DBSession,
    Base,
    )


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    event.listen(engine, 'connect', _fk_pragma_on_connect)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory='pyramid_app.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search','/search')
    config.add_route('history', '/history')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.scan()
    return config.make_wsgi_app()
