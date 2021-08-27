#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : rest.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 18.08.2021

import logging
import os








    @app.route("/me/")
    @requires_authorization
    async def me():
        user = discord.fetch_user()
        return f"""
        <html>
            <head>
                <title>{user.name}</title>
            </head>
            <body>
                <img src='{user.avatar_url}' />
                {user.fetch_guilds()}
                {user.id}
                {user.guilds}
            </body>
        </html>"""

    @app.route("/me/guilds/")
    @requires_authorization
    async def user_guilds():
        guilds = discord.fetch_guilds()
        bot_guilds = set([g.id for g in app.bot.guilds])

        result = []
        for g in guilds:
            role = '[ADMIN] ' if g.permissions.administrator else ''
            has_bot = ' (has bot)' if g.id in bot_guilds else ''
            if has_bot:
                channels =','.join([channel.name for channel in app.bot.get_guild(g.id).channels])
            else:
                channels = ''
            result.append(f'{role}{g.name} {g.id}{has_bot} [{channels}]')

        return "<br />".join(result)

    @app.route("/me/valid-guilds/")
    @requires_authorization
    async def valid_guilds():
        return {'guilds': [str(g) for g in session.get("valid_guilds")]}

    '''
    @app.route('/roll/<int:guild_id>/<string:channel_name>/<string:roll>')
    @requires_authorization
    async def roll_in_guild(guild_id, channel_name, roll):
        from .utils import d100
        log = logging.getLogger()
        log.info(f'roll_in_guild: {guild_id} {channel_name}')
        channels = app.bot.get_guild(guild_id).channels
        for c in channels:
            if c.name == channel_name:
                await c.send(f'{roll} -> {d100()}')
    '''
