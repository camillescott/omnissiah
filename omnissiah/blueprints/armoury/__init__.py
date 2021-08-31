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

from ... import database
from ...combat import player_attack, COMBAT_ACTIONS
from ...items import ItemAvailability
from ...utils import redirect_url, SUCCESS, FAILURE
from ...weapons import (Craftsmanship, PlayerWeapon, PlayerWeaponInstance)

from ...forms import WeaponForm


armoury = Blueprint('armoury', __name__, template_folder='templates')


@armoury.route("/armoury/player/weapons")
@requires_authorization
async def player_weapons():
    log = logging.getLogger()
    form = WeaponForm()
    player_weapons = [(d, _id) async for d, _id in database.query_armoury_player_weapons(session['user-id'])]
    log.info(f'player weapons: {player_weapons}')
    return await render_template('weapons.html',
                                 player_weapons=player_weapons,
                                 weapon_form=form)


@armoury.route("/armoury/player/weapons/add", methods=['POST'])
@requires_authorization
async def player_add_weapon():
    log = logging.getLogger()
    form = WeaponForm()
    log.info(f'Add weapon: {form.data}')
    if form.validate():
        weapon_model = form.get_weapon_model()
        result = await database.add_armoury_player_weapons(session['user-id'], weapon_model)

        log.info(f'{session.get("user-full-name")} added to armoury: {result.inserted_ids}')
    else:
        log.warning(f'Form failed validation: {form.errors}')

    return redirect(redirect_url())


@armoury.route("/armoury/player/weapons/delete", methods=['POST'])
@requires_authorization
async def player_delete_weapon():
    log = logging.getLogger()
    form = await request.form
    weapon_id = form['weapon-id']
    result = await database.delete_armoury_player_weapons(session['user-id'], weapon_id)

    return redirect(redirect_url())
