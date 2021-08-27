#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : forms.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 27.08.2021


from flask_wtf import FlaskForm
from wtforms import (Form, StringField, FormField, SubmitField, IntegerField, 
                     SelectField, BooleanField, DecimalField, validators)
from wtforms.validators import DataRequired, ValidationError

from .items import ItemAvailability
from .weapons import (WeaponClass, WeaponType, DamageType, Craftsmanship,
                      PlayerWeapon, PlayerWeaponInstance)


class WeaponForm(FlaskForm):
    weapon_name = StringField('Weapon Name')
    weapon_class = SelectField('Weapon Class', 
                               choices=[wc.value for wc in WeaponClass],
                               coerce=lambda v: WeaponClass[v])
    weapon_type = SelectField('Weapon Type', 
                               choices=[wt.value for wt in WeaponType],
                               coerce=lambda v: WeaponType[v])
    damage_type = SelectField('Damage Type', 
                               choices=[dt.value for dt in DamageType],
                               coerce=lambda v: DamageType[v])
    availability = SelectField('Availability',
                               default='Common',
                               choices=[ia.name for ia in ItemAvailability],
                               coerce=lambda v: ItemAvailability[v])
    weapon_range = IntegerField('Weapon Range')
    rof_single = BooleanField('RoF Single', default=True)
    rof_semi = IntegerField('RoF Semi', [validators.NumberRange(min=0)])
    rof_auto = IntegerField('RoF Auto', [validators.NumberRange(min=0)])
    damage_roll = IntegerField('Damage Roll', [validators.NumberRange(min=1)])
    damage_bonus = IntegerField('Damage Bonus', [validators.NumberRange(min=0)])
    penetration = IntegerField('Pen', [validators.NumberRange(min=0)])
    clip = IntegerField('Clip', [validators.NumberRange(min=1)], default=5)
    reload_time = DecimalField('Reload Rounds', default=1)
    mass = DecimalField('Mass')

    def get_weapon_model(self):
        return PlayerWeapon(
            name = self.weapon_name.data,
            availability = self.availability.data,
            weapon_class = self.weapon_class.data,
            weapon_type = self.weapon_type.data,
            weapon_range = self.weapon_range.data,
            rof = (self.rof_single.data, self.rof_semi.data, self.rof_auto.data),
            damage_roll = self.damage_roll.data,
            damage_bonus = self.damage_bonus.data,
            damage_type = self.damage_type.data,
            pen = self.penetration.data,
            clip = self.clip.data,
            reload_time = self.reload_time.data,
            mass = self.mass.data
        )


class WeaponAttackForm(FlaskForm):
    weapon = FormField(WeaponForm)
    target_range = IntegerField('Target Range')
    test_characteristic = IntegerField('Test Characteristic')
