#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : __init__.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 26.08.2021

import logging
import os

from quart import Blueprint, current_app, redirect, url_for, render_template, request, session
from flask_discord import requires_authorization, Unauthorized

from ...combat import player_attack, COMBAT_ACTIONS
from ...items import ItemAvailability
from ...utils import fetch_valid_guilds, redirect_url
from ...weapons import (WeaponClass, WeaponType, DamageType, Craftsmanship,
                      PlayerWeapon, PlayerWeaponInstance)

from ...forms import WeaponAttackForm


rolls = Blueprint('rolls', __name__, template_folder='templates')

@rolls.route("/roll")
@requires_authorization
async def roll():
    return redirect(url_for("home.index"))


@rolls.route("/roll/weapon/submit", methods=['POST'])
@requires_authorization
async def submit_roll_weapon():
    log = logging.getLogger()
    form = WeaponAttackForm()
    log.info(f'Weapon Form: {form.data}')
    if form.validate():
        weapon_model = form.weapon.get_weapon_model()
        log.info(f'Weapon model: {weapon_model}')
    
        channels = current_app.bot.get_guild(session['active_server_id']).channels
        for c in channels:
            if c.name == 'dice':
                await c.send(f'{current_app.discord.fetch_user().name} added weapon: {weapon_model}')
    else:
        log.warning(f'Form failed validation: {form.errors}')

    return redirect(redirect_url())


@rolls.route("/roll/weapon")
@requires_authorization
async def roll_weapon():
    valid_guilds = await fetch_valid_guilds()
    form = WeaponAttackForm()
    return await render_template('roll_weapon.html',
                                 discord=current_app.discord,
                                 valid_guilds=valid_guilds,
                                 form=form)
