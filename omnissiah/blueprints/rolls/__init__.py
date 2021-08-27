#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : __init__.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 26.08.2021

import logging
import os

from quart import Blueprint, current_app, redirect, url_for, render_template, request
from flask_discord import requires_authorization, Unauthorized

from ...combat import player_attack, COMBAT_ACTIONS
from ...items import ItemAvailability
from ...weapons import (WeaponClass, WeaponType, DamageType, Craftsmanship,
                      PlayerWeapon, PlayerWeaponInstance)


rolls = Blueprint('rolls', __name__, template_folder='templates')

@rolls.route("/roll")
@requires_authorization
async def roll():
    return redirect(url_for("home.index"))


@rolls.route("/roll/weapon/submit", methods=['POST'])
@requires_authorization
async def submit_roll_weapon():
    log = logging.getLogger()
    form = await request.form
    weapon_type = form['weapon_type']
    log.info(f'Weapon Form: {form}')

    weapon_model = PlayerWeapon(
        name = form['weapon_name'],
        availability=ItemAvailability.Common,
        weapon_class=WeaponClass[form['weapon_class']],
        weapon_type=WeaponType[form['weapon_type']],
        weapon_range=form['weapon_range'],
        rof = (True if form['rof_single'] == 'on' else False,
               form['rof_semi'],
               form['rof_auto']),
        damage_roll=form['damage_roll'],
        damage_bonus=form['damage_bonus'],
        damage_type=DamageType[form['damage_type']],
        pen=form['penetration'],
        clip=10,
        reload_time=1,
        mass=2
    )
    
    channels = current_app.bot.get_guild(750948331710054430).channels
    for c in channels:
        if c.name == 'dice':
            await c.send(f'{current_app.discord.fetch_user().name} added weapon: {weapon_model}')

    return redirect(url_for('home.index'))


@rolls.route("/roll/weapon")
@requires_authorization
async def roll_weapon():
    return await render_template('roll_weapon.html',
                                 discord=current_app.discord,
                                 weapon_classes=WeaponClass,
                                 weapon_types=WeaponType,
                                 damage_types=DamageType)
