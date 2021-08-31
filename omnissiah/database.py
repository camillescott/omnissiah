#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Camille Scott, 2021
# File   : database.py
# License: MIT
# Author : Camille Scott <camille.scott.w@gmail.com>
# Date   : 27.08.2021

import functools
import inspect
import logging
import types

from quart import current_app
from bson.objectid import ObjectId

from .utils import is_iterable


def use_mongo(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log = logging.getLogger() 
        log.info(f'wrapper: {func}')

        db = kwargs.get('db', current_app.mongo.db)
 
        func_instance = func(db, *args, **kwargs)
        if isinstance(func_instance, types.AsyncGeneratorType):
            log.info(f'{func}: AsyncGeneratorType')
            async def inner():
                async for result in func_instance:
                    yield result
        else:
            log.info(f'{func}: awaitable')
            async def inner():
                return await func_instance
        return inner()

    return wrapper


@use_mongo
async def query_armoury_player_weapons(db, user_id, **filters):
    from .weapons import PlayerWeapon

    weapons = db['armoury-player-weapons']
    query = {**{'user_id': int(user_id)}, **filters}
    cursor = weapons.find(query)
    
    async for weapon_data in cursor:
        _id = weapon_data.pop('_id')
        yield PlayerWeapon.from_dict(weapon_data), _id


@use_mongo
async def add_armoury_player_weapons(db, user_id, new_weapons):
    new_weapons = [new_weapons] if not is_iterable(new_weapons) else new_weapons
    data = (dict(user_id=int(user_id), **w.to_dict()) for w in new_weapons)

    weapons = db['armoury-player-weapons']
    result = await weapons.insert_many(data)
    
    return result


@use_mongo
async def delete_armoury_player_weapons(db, user_id, weapon_ids):
    weapon_ids = [ObjectId(weapon_ids)] if not is_iterable(weapon_ids) else \
                 [ObjectId(_id) for _id in weapon_ids]
    query = {'user_id': user_id, '_id': { '$in': weapon_ids }}
    
    weapons = db['armoury-player-weapons']
    result = await weapons.delete_many(query)

    return result

