#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : __init__.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 26.08.2021

import logging
import os

from quart import Blueprint, current_app, redirect, url_for, render_template
from flask_discord import requires_authorization, Unauthorized


sheets = Blueprint('sheets', __name__)


@sheets.route("/character-sheets")
@requires_authorization
async def character_sheets():
    return redirect(url_for(".index"))


@sheets.route("/ship-sheets")
@requires_authorization
async def ship_sheets():
    return redirect(url_for(".index"))
