#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : app.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 25.08.2021

import asyncio
import logging
import os
import yaml

import quart.flask_patch
from quart.flask_patch import request, session
from quart import Quart, Blueprint, redirect, url_for, render_template, g, flash, current_app
from quart_motor import Motor

from zardoz.cli import build_bot

import flask_discord
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from . import __version__


def callback(self):
    """A method which should be always called after completing authorization code grant process
    usually in callback view.
    It fetches the authorization token and saves it flask
    `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ object.
    """
    error = request.form.get("error")
    if error:
        if error == "access_denied":
            raise exceptions.AccessDenied()
        raise exceptions.HttpException(error)

    state = session.get("DISCORD_OAUTH2_STATE", str())
    token = self._fetch_token(state)
    self.save_authorization_token(token)

DiscordOAuth2Session.callback = callback


def build_app(args):

    app = Quart(__name__)
    app.secret_key = args.secret_key
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true" 
    app.config["DISCORD_CLIENT_ID"] = args.client_id
    app.config["DISCORD_CLIENT_SECRET"] = args.client_secret
    app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback" # URL to your callback endpoint.
    app.config["DISCORD_BOT_TOKEN"] = ''  # Required to access BOT resources.
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/omnissiah-database"

    discord = DiscordOAuth2Session(app)
    app.discord = discord

    mongo = Motor(app)
    app.mongo = mongo

    return app


def run_app(args):

    if args.credentials_file:
        with args.credentials_file.open() as fp:
            creds = yaml.safe_load(fp)
            args.secret_token = creds['bot_token']
            args.client_id = creds['discord_client_id']
            args.client_secret = creds['discord_client_secret']
            args.secret_key = creds['app_secret_key']

    app = build_app(args)
    # register blueprints
    from .blueprints.home import home
    from .blueprints.sheets import sheets
    from .blueprints.rolls import rolls
    from .blueprints.armoury import armoury

    app.register_blueprint(home)
    app.register_blueprint(sheets)
    app.register_blueprint(rolls)
    app.register_blueprint(armoury)

    @app.before_serving
    async def startup():

        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        bot, DB = build_bot(args,
                            token_name='OMNISSIAH_TOKEN',
                            prefix='o',
                            loop=loop)

        @bot.event
        async def on_ready():
            log = logging.getLogger()
            log.info(f'Ready: member of {bot.guilds}')
            log.info(f'Users: {bot.users}')

        @bot.command(name='about', help='Project info.')
        async def about(ctx):
            msg = f'version: {__version__}\n'\
                  f'source: https://github.com/camillescott/omnissiah/releases/tag/v{__version__}\n'\
                  f'active installs: {len(bot.guilds)}'
            await ctx.message.reply(msg)

        async def runner(bot, *args, **kwargs):
            try:
                await bot.start(*args, **kwargs)
            finally:
                if not bot.is_closed():
                    await bot.close()

        app.bot = bot
        loop.create_task(bot.start(args.secret_token))

    @app.after_serving
    async def shutdown():
        if not app.bot.is_closed():
            await app.bot.close()

    app.run('0.0.0.0', 5000, use_reloader=True, debug=True)
 
