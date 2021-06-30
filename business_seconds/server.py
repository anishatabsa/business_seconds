"""
Pyramid server definition
business_seconds_server is defined as an entry point in setup.py, and is called
by PasteDeploy compatible wsgi servers, ie:
pserve ./configuration/pyramid/development.ini --reload
-or-
uwsgi --ini-paste ./configuration/pyramid/development.ini
"""
import logging

import pkg_resources
from pyramid.config import Configurator

from .controllers import \
    business_seconds_controller as business_seconds_controller

logger = logging.getLogger(__name__)
version = pkg_resources.get_distribution('business_seconds').version


def business_seconds_server(global_config, **settings):
    logger.debug(global_config)
    logger.debug(settings)
    config = Configurator(settings=settings)
    config.include('pyramid_openapi3')
    config.pyramid_openapi3_spec(
        './business_seconds/api_docs/swagger.yml',
        route='/api-docs/swagger.yml',
    )
    config.pyramid_openapi3_add_explorer(route='/api-docs')
    config.add_route('get_business_seconds', '/get_business_seconds')
    config.scan()

    # Hook a controller to the registry
    # config.registry.controller = c.Controller()
    config.registry.business_controller = (
        business_seconds_controller.BusinessSecondsController()
    )
    # Set service version
    config.registry.settings['service_version'] = version

    # use default exception tween factory in configuration.
    app = config.make_wsgi_app()
    return app


def patch_view_config_check_openapi():
    """
    Patches view_config to check that openapi=True was specified.
    If this isn't done, someone might forget to add it.
    """
    import pyramid.view

    view_config_orig = pyramid.view.view_config

    def view_config(**kwargs):
        if 'openapi' not in kwargs and 'context' not in kwargs:
            raise Exception('Must specify openapi=True!')
        return view_config_orig(**kwargs)

    pyramid.view.view_config = view_config


patch_view_config_check_openapi()
