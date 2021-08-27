#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : rest.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 18.08.2021

import logging
import os

from quart import Blueprint, current_app, redirect, url_for, render_template, request
from flask_discord import requires_authorization, Unauthorized


home = Blueprint('home', __name__)


@home.route('/')
async def index():
    return await render_template('base.html', discord=current_app.discord)


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


async def fetch_valid_guilds():
    user_guilds = current_app.discord.fetch_guilds()
    user_guilds = set((g.id for g in user_guilds))
    bot_guilds = list((g.id for g in current_app.bot.guilds))

    valid = []
    for bg in bot_guilds:
        if bg.id in user_guilds:
            valid.append(bg)

    return valid
