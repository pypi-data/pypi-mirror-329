# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import patch

from wuttjamaican.testing import FileTestCase, ConfigTestCase

from asgiref.wsgi import WsgiToAsgi
from pyramid.config import Configurator
from pyramid.router import Router

from wuttaweb import app as mod
from wuttjamaican.conf import WuttaConfig


class TestWebAppProvider(TestCase):

    def test_basic(self):
        # nb. just normal usage here, confirm it does the one thing we
        # need it to..
        config = WuttaConfig()
        app = config.get_app()
        handler = app.get_web_handler()


class TestMakeWuttaConfig(FileTestCase):

    def test_config_path_required(self):

        # settings must define config path, else error
        settings = {}
        self.assertRaises(ValueError, mod.make_wutta_config, settings)

    def test_basic(self):

        # mock path to config file
        myconf = self.write_file('my.conf', '')
        settings = {'wutta.config': myconf}

        # can make a config okay
        config = mod.make_wutta_config(settings)

        # and that config is also stored in settings
        self.assertIn('wutta_config', settings)
        self.assertIs(settings['wutta_config'], config)


class TestMakePyramidConfig(TestCase):

    def test_basic(self):
        settings = {}
        config = mod.make_pyramid_config(settings)
        self.assertIsInstance(config, Configurator)


class TestMain(FileTestCase):

    def test_basic(self):
        global_config = None
        myconf = self.write_file('my.conf', '')
        settings = {'wutta.config': myconf}
        app = mod.main(global_config, **settings)
        self.assertIsInstance(app, Router)


def mock_main(global_config, **settings):

    wutta_config = mod.make_wutta_config(settings)
    pyramid_config = mod.make_pyramid_config(settings)

    pyramid_config.include('wuttaweb.static')
    pyramid_config.include('wuttaweb.subscribers')
    pyramid_config.include('wuttaweb.views')

    return pyramid_config.make_wsgi_app()


class TestMakeWsgiApp(ConfigTestCase):

    def test_with_callable(self):

        # specify config
        wsgi = mod.make_wsgi_app(mock_main, config=self.config)
        self.assertIsInstance(wsgi, Router)

        # auto config
        with patch.object(mod, 'make_config', return_value=self.config):
            wsgi = mod.make_wsgi_app(mock_main)
            self.assertIsInstance(wsgi, Router)

    def test_with_spec(self):

        # specify config
        wsgi = mod.make_wsgi_app('tests.test_app:mock_main', config=self.config)
        self.assertIsInstance(wsgi, Router)

        # auto config
        with patch.object(mod, 'make_config', return_value=self.config):
            wsgi = mod.make_wsgi_app('tests.test_app:mock_main')
            self.assertIsInstance(wsgi, Router)

    def test_invalid(self):
        self.assertRaises(ValueError, mod.make_wsgi_app, 42, config=self.config)


class TestMakeAsgiApp(ConfigTestCase):

    def test_with_callable(self):

        # specify config
        asgi = mod.make_asgi_app(mock_main, config=self.config)
        self.assertIsInstance(asgi, WsgiToAsgi)

        # auto config
        with patch.object(mod, 'make_config', return_value=self.config):
            asgi = mod.make_asgi_app(mock_main)
            self.assertIsInstance(asgi, WsgiToAsgi)

    def test_with_spec(self):

        # specify config
        asgi = mod.make_asgi_app('tests.test_app:mock_main', config=self.config)
        self.assertIsInstance(asgi, WsgiToAsgi)

        # auto config
        with patch.object(mod, 'make_config', return_value=self.config):
            asgi = mod.make_asgi_app('tests.test_app:mock_main')
            self.assertIsInstance(asgi, WsgiToAsgi)

    def test_invalid(self):
        self.assertRaises(ValueError, mod.make_asgi_app, 42, config=self.config)
