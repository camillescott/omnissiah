#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : __init__.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 26.08.2021

import logging
import os

from quart import Blueprint, current_app, redirect, url_for, render_template, request, session, g
from flask_discord import requires_authorization, Unauthorized

from ...combat import player_attack, COMBAT_ACTIONS
from ...items import ItemAvailability
from ...utils import redirect_url, SUCCESS, FAILURE
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
        weapon_instance = PlayerWeaponInstance(weapon_model, craftsmanship=Craftsmanship.Good)
        actions = [form.player_action.action.data]
        log.info(f'Weapon model: {weapon_model}')

        status, attack_ctx = player_attack(weapon_instance,
                                           form.test_characteristic.data,
                                           actions=actions,
                                           target_range=form.target_range.data)
        g.prev_attack = attack_ctx

        channels = current_app.bot.get_guild(session['active_server_id']).channels
        for c in channels:
            if c.name == 'dice':
                status_str = SUCCESS if status else FAILURE
                result = (
                    f'{current_app.discord.fetch_user().name} attacked using {weapon_model.name}: \n'
                    f'**Char value**: {form.test_characteristic.data}\n'
                    f'**Target range**: {form.target_range.data}\n'
                    f'**Weapon range**: {weapon_model.weapon_range}\n'
                    f'**Attack action**: {actions[0].name}\n'
                    f'**Attack roll**: {status_str}  {attack_ctx.test_str}\n'
                )
                if status:
                    result += (
                        f'**Total damage**: {attack_ctx.total_damage} {weapon_model.damage_type.value} @ pen {weapon_model.pen}\n'
                        f'**DoS**: {attack_ctx.attack_degrees}\n'
                        f'**Hits**: {attack_ctx.hits}\n'
                        f'**Locations**: {", ".join(attack_ctx.locations)}\n'
                        f'**Rolls**:\n'
                        f'{attack_ctx.damage_str}'
                    )
                await c.send(result)
    else:
        log.warning(f'Form failed validation: {form.errors}')

    return redirect(redirect_url())


@rolls.route("/roll/weapon")
@requires_authorization
async def roll_weapon():
    log = logging.getLogger()
    if g.get('prev_attack', False):
        log.info(f'Prev attack: {g["prev_attack"]}')
    form = WeaponAttackForm()
    return await render_template('roll_weapon.html',
                                 form=form,
                                 weapon_form=form.weapon)
