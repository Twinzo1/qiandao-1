#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<17175297.hk@gmail.com>
#         http://binux.me
# Created on 2012-12-15 16:16:38

import logging
import jinja2
import tornado.web
import tornado.websocket
from tornado.web import HTTPError

import config

__ALL__ = ['HTTPError', 'BaseHandler', 'BaseWebSocket', 'BaseUIModule', ]

class BaseHandler(tornado.web.RequestHandler):
    application_export = {}
    def __getattr__(self, key):
        if key in self.application_export:
            return getattr(self.application, key)
        super(BaseHandler, self).__getattr__(key)

    def render_string(self, template_name, **kwargs):
        try:
            template = self.application.jinja_env.get_template(template_name)
        except jinja2.TemplateNotFound:
            raise

        namespace = dict(
                static_url=self.static_url,
                xsrf_token=self.xsrf_token,

                handler=self,
                request=self.request,
                current_user=self.current_user,
                locale=self.locale,
                xsrf_form_html=self.xsrf_form_html,
                reverse_url=self.reverse_url
            )
        namespace.update(kwargs)

        return template.render(namespace)

class BaseWebSocket(tornado.websocket.WebSocketHandler):
    pass

class BaseUIModule(tornado.web.UIModule):
    pass