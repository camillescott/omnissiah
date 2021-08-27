#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : __main__.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 18.08.2021

import argparse
import json
import os
from pathlib import Path
import sys
import textwrap

from . import __version__, __splash__, __about__, __testing__
from .app import run_app
from .simulate import simulate
from .utils import EnumAction, default_log_file, default_database_dir


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass


def main():
    from .combat import COMBAT_ACTIONS
    from .items import ItemAvailability
    from .weapons import (WeaponClass, WeaponType, DamageType,
                         Craftsmanship)

    parser = argparse.ArgumentParser(
        description=f'{__splash__}\n{__about__}',
        formatter_class=CustomFormatter
    )
    subparsers = parser.add_subparsers()

    app_parser = subparsers.add_parser('app')
    app_parser.add_argument(
        '--secret-token',
        help='The secret token for the bot, '\
             'from the discord developer portal. '\
             'If you have set $OMNISSIAH_TOKEN, this '\
             'option will override that.'
    )
    app_parser.add_argument(
        '--database-dir',
        type=lambda p: Path(p).absolute(),
        default=default_database_dir(debug=__testing__),
        help='Directory for the bot databases. Default follows the '\
             'XDG specifiction.'
    )
    app_parser.add_argument(
        '--log',
        type=lambda p: Path(p).absolute(),
        default=default_log_file(debug=__testing__),
        help='Path to the log file. Default follows the '\
             'XDG specifiction.'
    )
    app_parser.add_argument(
        '--credentials-file',
        type=lambda p: Path(p).absolute()
    )
    app_parser.add_argument(
        '--client-id',
        type=int
    )
    app_parser.add_argument(
        '--client-secret',
    )
    app_parser.add_argument(
        '--secret-key'
    )
    app_parser.set_defaults(func=run_app)


    simulate_parser = subparsers.add_parser('simulate')
    simulate_parser.add_argument(
        '-BS',
        '--ballistic-skill',
        default=40,
        type=int
    )
    simulate_parser.add_argument(
        '--actions',
        nargs='+',
        choices=COMBAT_ACTIONS.keys()
    )
    simulate_parser.add_argument(
        '--target-range',
        default=10,
        type=int
    )
    simulate_parser.add_argument(
        '--name',
        default='RT Weapon',
    )
    simulate_parser.add_argument(
        '--availability',
        default=ItemAvailability.Scarce,
        action=EnumAction,
        type=ItemAvailability
    )
    simulate_parser.add_argument(
        '--weapon-class',
        default=WeaponClass.Pistol,
        action=EnumAction,
        type=WeaponClass
    )
    simulate_parser.add_argument(
        '--type',
        default=WeaponType.Las,
        type=WeaponType,
        action=EnumAction
    )
    simulate_parser.add_argument(
        '--range',
        default=20,
        type=int
    )
    simulate_parser.add_argument(
        '--rof-single',
        default=True,
        type=bool
    )
    simulate_parser.add_argument(
        '--rof-semi',
        default=0,
        type=int
    )
    simulate_parser.add_argument(
        '--rof-auto',
        default=0,
        type=int
    )
    simulate_parser.add_argument(
        '--damage-d10',
        default=1,
        type=int
    )
    simulate_parser.add_argument(
        '--damage-bonus',
        default=3,
        type=int
    )
    simulate_parser.add_argument(
        '--damage-type',
        default=DamageType.Energy,
        type=DamageType,
        action=EnumAction
    )
    simulate_parser.add_argument(
        '--pen',
        default=0,
        type=int
    )
    simulate_parser.add_argument(
        '--clip',
        default=10,
        type=int
    )
    simulate_parser.add_argument(
        '--reload-time',
        default=1.0,
        type=float
    )
    simulate_parser.add_argument(
        '--mass',
        default=2.0,
        type=float
    )
    simulate_parser.add_argument(
        '--craftsmanship',
        default=Craftsmanship.Common,
        type=Craftsmanship,
        action=EnumAction
    )
    simulate_parser.add_argument(
        '--n-trials',
        '-N',
        default=10000,
        type=int
    )
    simulate_parser.add_argument(
        '--plot',
        default='text',
        choices = ['text', 'image']
    )
    simulate_parser.set_defaults(func=simulate)

    args = parser.parse_args()
    args.func(args)


