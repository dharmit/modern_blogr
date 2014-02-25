from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authn_policy = AuthTktAuthenticationPolicy(
        settings.get('auth.secret'),
        hashalg='sha512',
        )
    authz_policy = ACLAuthorizationPolicy()

    session_factory = SignedCookieSessionFactory(
        settings.get('session.secret'),
        )

    config = Configurator(
        settings=settings,
        session_factory=session_factory,
        root_factory='modern_blogr.models.RootFactory'
        )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home:page', '/page/{page:\d+}')
    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    config.add_route('blog_action', '/blog/{action}')
    config.add_route('archive', '/archive/{year}/{month}')
    config.add_route('tag', '/tag/{tag_name}')
    config.add_route('tags', '/tags')
    config.add_route('about', '/about')
    config.scan()
    return config.make_wsgi_app()
