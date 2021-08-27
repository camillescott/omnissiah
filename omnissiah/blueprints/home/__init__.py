#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : rest.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 18.08.2021

import logging
import os

from quart import Blueprint, current_app, redirect, url_for, render_template, request, session
from flask_discord import requires_authorization, Unauthorized

from ...utils import fetch_valid_guilds, redirect_url


home = Blueprint('home', __name__)


@home.route('/')
async def index():
    return await render_template('base.html')


@home.route("/login/")
async def login():
    return current_app.discord.create_session()


@home.route("/logout/")
async def logout():
    current_app.discord.revoke()
    return redirect(url_for(".index"))


@home.route("/callback/")
async def callback():
    log = logging.getLogger()
    log.info('Discord callback')
    discord = current_app.discord
    discord.callback()

    valid_guilds = await fetch_valid_guilds()
    session['valid-guilds'] = valid_guilds
    session['user-avatar-url'] = discord.fetch_user().avatar_url 
    session['user-name' ] = discord.fetch_user().name
    session['user-id'] = discord.fetch_user().id
    session['user-disc'] = discord.fetch_user().discriminator
    session['user-full-name'] = str(discord.fetch_user())

    return redirect(url_for(".index"))


@home.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("home.login"))


@home.route('/set-server', methods=['POST'])
async def set_server():
    log = logging.getLogger()
    log.info('Do set-server')
    form = await request.form
    session['active-server-id'] = int(form['server-id'])
    valid = session.get('valid-guilds')
    session['active-server-name'] = valid[form['server-id']]
    log.info(f'{current_app.discord.fetch_user()} set server to {session["active-server-id"]}')
    return redirect(redirect_url())


@home.app_context_processor
async def navbar_args():
    return {'discord': current_app.discord}
