from datetime import datetime
from mongoengine import *


class LobbyUser(EmbeddedDocument):
    username = StringField(required=True)
    is_ready = BooleanField(default=False)


class RaceInfo(EmbeddedDocument):
    race = StringField(required=True)
    username = StringField(default='')

    hero_name = StringField()
    hero_defence_modifier = IntField(default=0)
    hero_attack_modifier = IntField(default=0)
    hero_harvest_modifier = IntField(default=0)

    harvest_count = IntField(default=0)
    harvest_collection_rate = IntField(default=1)

    deployment_default = IntField(default=1)
    deployment_total = IntField(default=0)
    deployment_infantry_count = IntField(default=0)
    deployment_ranged_count = IntField(default=0)
    deployment_tanks_count = IntField(default=0)

    units = ListField()


class Game(Document):
    name = StringField(max_length=60, required=True, unique=True)
    player_count = IntField(required=True)
    active_races = ListField(required=True)

    round = IntField(default=1)
    phase = StringField(default='orders')
    phase_waiting_on = ListField()
    active_player = StringField(default='')
    units = ListField()
    rounds_max_number = IntField(default=3)

    uuids = ListField()
    geoengineers = EmbeddedDocumentField(RaceInfo)
    settlers = EmbeddedDocumentField(RaceInfo)
    kingdomwatchers = EmbeddedDocumentField(RaceInfo)
    periplaneta = EmbeddedDocumentField(RaceInfo)
    reduviidae = EmbeddedDocumentField(RaceInfo)
    guardians = EmbeddedDocumentField(RaceInfo)

    races_to_commit = ListField()
    races_to_deploy = ListField()

    chat_log = ListField()
    game_log = ListField()

    display_open_modal = ListField()

    is_lobby_open = BooleanField(default=True)
    lobby_status = ListField(EmbeddedDocumentField(LobbyUser))
    created_at = DateTimeField(default=datetime.now())


class GameModel:
    def __init__(self, host='localhost', port=27017, db_name='animus'):
        connect(db_name, host=host, port=port)

    @staticmethod
    def create_game(game_name, player_count=2):
        geoengineers = RaceInfo(race='geoengineers')
        settlers = RaceInfo(race='settlers')
        kingdomwatchers = RaceInfo(race='kingdomwatchers')
        periplaneta = RaceInfo(race='periplaneta')
        reduviidae = RaceInfo(race='reduviidae')
        guardians = RaceInfo(race='guardians')

        if player_count == 2:
            active_races = ['geoengineers', 'settlers']
            kingdomwatchers = None
            periplaneta = None
            reduviidae = None
            guardians = None
            units = get_base_units(player_count=player_count)
        elif player_count == 3:
            active_races = ['geoengineers', 'settlers', 'kingdomwatchers']
            periplaneta = None
            reduviidae = None
            guardians = None
            units = get_base_units(player_count=player_count)
        elif player_count == 4:
            active_races = ['geoengineers', 'settlers', 'kingdomwatchers', 'periplaneta']
            reduviidae = None
            guardians = None
            units = get_base_units(player_count=player_count)
        elif player_count == 5:
            active_races = ['geoengineers', 'settlers', 'kingdomwatchers', 'periplaneta', 'reduviidae']
            guardians = None
            units = get_base_units(player_count=player_count)
        else:
            active_races = ['geoengineers', 'settlers', 'kingdomwatchers', 'periplaneta', 'reduviidae', 'guardians']
            units = get_base_units(player_count=player_count)

        return Game(
            name=game_name,
            player_count=player_count,
            active_races=active_races,
            geoengineers=geoengineers,
            settlers=settlers,
            kingdomwatchers=kingdomwatchers,
            periplaneta=periplaneta,
            reduviidae=reduviidae,
            guardians=guardians,
            units=units
        ).save()


def get_base_map():
    return {
        "map":
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                [0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0],
                [0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 0],
                [0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 3, 0],
                [0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0],
                [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 1, 1, 3, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 1, 1, 1, 1, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
    }


def get_base_units(player_count=2):
    if player_count == 2:
        return [
            {
                "posX": 4,
                "posY": 3,
                "index": 76,
                "race": "geoengineers",
                "infantry": 1,
                "ranged": 1,
                "tanks": 1,
                "order": "notSet"
            },
            {
                "posX": 4,
                "posY": 2,
                "index": 52,
                "race": "geoengineers",
                "infantry": 2,
                "ranged": 2,
                "tanks": 4,
                "order": "notSet"
            },
            {
                "posX": 5,
                "posY": 2,
                "index": 53,
                "race": "settlers",
                "infantry": 1,
                "ranged": 2,
                "tanks": 1,
                "order": "notSet"
            },
            {
                "posX": 5,
                "posY": 3,
                "index": 77,
                "race": "settlers",
                "infantry": 0,
                "ranged": 0,
                "tanks": 1,
                "order": "notSet"
            }
        ]
    else:
        return None


def get_game_by_name(game_name):
    game = Game.objects.filter(name=game_name)
    if len(game) > 0:
        return game[0]
    else:
        return []


def get_games_available_to_join():
    return [game.name for game in Game.objects(is_lobby_open=True)]


def lock_in_race_if_available(game_name, race, player):
    game = Game.objects.filter(name=game_name)[0]
    race = race.lower()
    if game[race]['username'] == '':
        game[race]['username'] = player
        game.save()
        return True
    else:
        return False


def hero_selected(race, hero_type, game_name, player_name):
    game = Game.objects.filter(name=game_name)[0]

    lobby_lock_in = LobbyUser(username=player_name, is_ready=True)
    game['lobby_status'].append(lobby_lock_in)

    race = race.lower()
    game[race]['hero_name'] = player_name + '_' + hero_type
    if hero_type == 'attack':
        game[race]['hero_attack_modifier'] = 1
    elif hero_type == 'defence':
        game[race]['hero_attack_modifier'] = -1
        game[race]['hero_defence_modifier'] = 3
    else:
        game[race]['hero_harvest_modifier'] = 2
    game.save()


def all_races_are_claimed(game_name):
    game = Game.objects.filter(name=game_name)[0]
    return len(game['lobby_status']) == game['player_count']


def close_lobby(game_name):
    game = Game.objects.filter(name=game_name)[0]
    game['is_lobby_open'] = False
    game.save()


def get_players_race(game_name, player_name):
    game_doc = get_game_by_name(game_name)
    for race in game_doc['active_races']:
        if game_doc[race]['username'] == player_name:
            return race
    return None
