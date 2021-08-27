#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : __init__.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 27.08.2021

import logging
import os

from quart import (Blueprint, current_app, redirect, url_for, 
                   render_template, request, session, g)
from flask_discord import requires_authorization, Unauthorized

from ...combat import player_attack, COMBAT_ACTIONS
from ...items import ItemAvailability
from ...utils import redirect_url, SUCCESS, FAILURE
from ...weapons import (Craftsmanship, PlayerWeapon, PlayerWeaponInstance)

from ...forms import WeaponForm


armoury = Blueprint('armoury', __name__, template_folder='templates')


@armoury.route("/armoury/player/weapons/add", methods=['POST'])
@requires_authorization
async def player_add_weapon():
    log = logging.getLogger()
    form = WeaponForm()
    log.info(f'Add weapon: {form.data}')
    if form.validate():
        table = current_app.mongo.db['armoury-player-weapons']
        weapon_model = form.get_weapon_model()
        data = weapon_model.to_dict()
        data['user_id'] = session['user-id']

        result = await table.insert_one(data)
        log.info(f'{session.get("user-full-name")} added to armoury: {result}')
    else:
        log.warning(f'Form failed validation: {form.errors}')

    return redirect(redirect_url())


@armoury.route("/armoury/player/weapons")
@requires_authorization
async def player_weapons():
    log = logging.getLogger()
    form = WeaponForm()
    return await render_template('weapons.html',
                                  weapon_form=form)
