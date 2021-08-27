--name: create_schema#
CREATE TABLE IF NOT EXISTS rolls (
    member_id INTEGER NOT NULL,
    member_nick TEXT,
    member_name TEXT,
    roll TEXT NOT NULL,
    tag TEXT,
    result TEXT NOT NULL,
    time real NOT NULL
);

CREATE TABLE IF NOT EXISTS user_vars (
    member_id INTEGER NOT NULL,
    var TEXT NOT NULL,
    val INTEGER NOT NULL,
    PRIMARY KEY (member_id, var)
);

CREATE TABLE IF NOT EXISTS guild_vars (
    member_id INTEGER NOT NULL,
    var TEXT not NULL,
    val INTEGER not NULL,
    PRIMARY KEY (var)
);

CREATE TABLE IF NOT EXISTS player_weapons (
    member_id INTEGER NOT NULL,
    player_tag text not null,
    weapon_name TEXT NOT NULL,
    weapon_class TEXT  NOT NULL,
    weapon_type TEXT NOT NULL,
    weapon_range INT NOT NULL,
    rof_single INT NOT NULL,
    rof_semi INT NOT NULL,
    rof_auto INT NOT NULL,
    damage_roll INT NOT NULL,
    damage_bonus int not null,
    damage_type text not null,
    pen int not null,
    clip int not null,
    reload_time real not null,
    PRIMARY KEY (member_id, player_tag)
);
