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
    valid = await fetch_valid_guilds()
    return await render_template('base.html',
                                 discord=current_app.discord,
                                 valid_guilds=valid)


@home.route("/login/")
async def login():
    log = logging.getLogger()

    #session['valid_guilds'] = list(valid)
    #log.info(f'bot guilds: {app.bot.guilds}')
    #log.info(f'User guilds: {user_guilds}')
    #log.info(f'Valid guilds: {valid}')
    return current_app.discord.create_session()


@home.route("/logout/")
async def logout():
    current_app.discord.revoke()
    return redirect(url_for(".index"))


@home.route("/callback/")
async def callback():
    current_app.discord.callback()
    return redirect(url_for(".index"))


@home.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@home.route('/set-server', methods=['POST'])
async def set_server():
    log = logging.getLogger()
    log.info('Do set-server')
    form = await request.form
    session['active_server_id'] = int(form['server-id'])
    valid = await fetch_valid_guilds()
    session['active_server_name'] = valid[int(form['server-id'])].name
    log.info(f'{current_app.discord.fetch_user()} set server to {session["active_server_id"]}')
    return redirect(redirect_url())

