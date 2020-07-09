import os
import sys

import json
import random
import pygame

from pygame.locals import *

SCREEN_FILL: (253, 253, 253)

class Move():
    def __init__(self, move_id): 
        dir_py = os.path.dirname(__file__)
        rel_path = 'data/movedex.json'
        with open(os.path.join(dir_py, rel_path), 'r') as f_movedex:
            dic_movedex = json.load(f_movedex)
            self.moveID = move_id
            self.name = dic_movedex[move_id]['name']
            self.type = dic_movedex[move_id]['type']
            self.category = dic_movedex[move_id]['category']
            self.turns = dic_movedex[move_id]['turns']
            self.power = dic_movedex[move_id]['power']
            self.accuracy = dic_movedex[move_id]['accuracy']
            self.priority = dic_movedex[move_id]['priority']
            self.pps = dic_movedex[move_id]['pps']
            self.max_pps = dic_movedex[move_id]['pps']
            self.stats_user = dic_movedex[move_id]['stats_user']
            self.stats_foe = dic_movedex[move_id]['stats_foe']
            self.status_user = dic_movedex[move_id]['status_user']
            self.status_foe = dic_movedex[move_id]['status_foe']
            self.hp_user = dic_movedex[move_id]['hp_user']
            self.hp_foe = dic_movedex[move_id]['hp_foe']
    
    def spendPP(self):
        self.pps -= 1
    
    def __str__(self):
        return """Move(
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}', 
    '{}',
    '{}', 
    '{}', 
    '{}'
)""".format(self.moveID, self.name, self.type, self.category, self.turns, self.power,self.accuracy, self.priority, self.pps, self.stats_user, self.stats_foe, self.status_user, self.status_foe, self.hp_user, self.hp_foe)

class Pokemon():
    def __init__(self, pid):
        dir_py = os.path.dirname(__file__)
        rel_path = 'data/pokedex.json'
        with open(os.path.join(dir_py, rel_path), 'r') as f_pokedex:
            dic_pokedex = json.load(f_pokedex)
            self.p_id = dic_pokedex[pid]['pid']
            self.name = dic_pokedex[pid]['name']
            self.main_type = dic_pokedex[pid]['mainType']
            self.sec_type = dic_pokedex[pid]['secType']
            self.moveset = []
            self.moveset.append(Move(dic_pokedex[pid]['moveset'][0]))
            self.moveset.append(Move(dic_pokedex[pid]['moveset'][1]))
            self.moveset.append(Move(dic_pokedex[pid]['moveset'][2]))
            self.moveset.append(Move(dic_pokedex[pid]['moveset'][3]))
            self.HP = ((dic_pokedex[pid]['baseHP']*2 + 31 + 21)+110)  #omitted level * and / because every pokemon is lvl100, and 100/100=0
            self.ATT = ((dic_pokedex[pid]['baseAtt']*2 + 31 + 21) + 5)  #omitted level because every pokemon is lvl100 and omited nature for the sake of simplicity
            self.DEF_ = ((dic_pokedex[pid]['baseDef']*2 + 31 + 21) + 5)  #omitted level because every pokemon is lvl100 and omited nature for the sake of simplicity
            self.SP_ATT = ((dic_pokedex[pid]['baseSpAtt']*2 + 31 + 21) + 5)  #omitted level because every pokemon is lvl100 and omited nature for the sake of simplicity
            self.SP_DEF = ((dic_pokedex[pid]['baseSpDef']*2 + 31 + 21) + 5)  #omitted level because every pokemon is lvl100 and omited nature for the sake of simplicity
            self.SPEED = ((dic_pokedex[pid]['baseSpe']*2 + 31 + 21) + 5)  #omitted level because every pokemon is lvl100 and omited nature for the sake of simplicity
        self.ko = False
        self.current_hp = self.HP
        self.current_att = self.ATT
        self.current_def = self.DEF_
        self.current_sp_att = self.SP_ATT
        self.current_sp_def = self.SP_DEF
        self.current_speed = self.SPEED
        self.stage_att = 0
        self.stage_def = 0
        self.stage_sp_att = 0
        self.stage_sp_def = 0
        self.stage_speed = 0
        self.accuracy = 1.0
        self.evasion = 1.0
        self.stage_accuracy = 0
        self.stage_evasion = 0
        self.status_list = []
        self.status_turns = []

    def __str__(self):
        return """#{}: {}
KO: {}
{} / {}

HP: {}/{}
Att: {}/{}  {}
Def: {}/{}  {}
Sp Att: {}/{}  {}
Sp Def: {}/{}  {}
Speed: {}/{}  {}

Accu: {}  {}
Eva: {}  {}

Status: {}
Turns:  {}

Moves: {}
""".format(self.p_id, self.name, self.ko, self.main_type, self.sec_type, self.current_hp, self.HP, self.current_att, self.ATT, self.stage_att, self.current_def, self.DEF_, self.stage_def, self.current_sp_att, self.SP_ATT, self.stage_sp_att, self.current_sp_def, self.SP_DEF, self.stage_sp_def, self.current_speed, self.SPEED, self.stage_speed, self.accuracy, self.stage_accuracy, self.evasion, self.stage_evasion, self.status_list, self.status_turns, self.moveset)
 
def build_team_user(chosen_pokemon):
    team_user = []
    counter = 0
    for i in chosen_pokemon: 
        if i != 0: 
            team_user.append(Pokemon(str(chosen_pokemon[counter])))
        counter += 1
    return team_user

def build_team_foe(chosen_pokemon):
    team_foe: list = []
    list_foe: list = []
    list_pokemons = [3, 6, 9, 26, 62, 65, 68, 76, 78, 91, 94, 97, 112, 113, 115, 127, 130, 131, 134, 135, 136, 143, 144, 145, 146, 149, 150, 151]
    for pok in chosen_pokemon: 
        if pok != 0:
            list_foe.append(pok)
    num_pokemons = len(list_foe)
    list_foe = random.sample(list_pokemons, num_pokemons)
    for i in range(num_pokemons): 
        team_foe.append(Pokemon(str(list_foe[i])))
    return [list_foe, team_foe]

def is_combat_possible(team_user, team_foe):
    count_u = 0
    count_f = 0
    for i in team_user:
        if i.current_hp <= 0: i.ko = True
    for i in team_foe:
        if i.current_hp <= 0: i.ko = True
    for i in team_user:
        if i.ko == False:
            count_u += 1
    for i in team_foe:
        if i.ko == False:
            count_f += 1
    if count_u > 0 and count_f > 0:     # both teams have a usable pokemon
        return 0
    elif count_u > 0:       # user wins
        return 1
    elif count_f > 0:       # foe wins
        return 2
    else: return 3          # no team has a usable pokemon

def battle_menu_main(menu_choice):
    menu_choice = int(input())
    return menu_choice

def battle_menu_moves(team_user, active_user, team_foe, active_foe):
    menu_choice = int(input())-1
    return menu_choice

def battle_menu_team(team_user, active_user):
    menu_choice = int(input())
    return menu_choice

def battle_dead_team(team_user, active_user):
    menu_choice = int(input())
    return menu_choice

def choose_attack_foe():
    random_number = random.randint(1, 16000)   #random with small ranges doesn't feel really random
    if random_number < 4001: 
        return 0
    elif random_number < 8001:
        return 1
    elif random_number < 12001:
        return 2
    else: return 3

def attacking_both(combat, attack_user):
    random_number: int
    attack_foe = choose_attack_foe()
    if combat['team_user_objs'][combat['active_user']].moveset[attack_user].priority < combat['team_foe_objs'][combat['active_foe']].moveset[attack_foe].priority: 
        return {'attacks': [attack_user, attack_foe],
        'user_first': False, 
        'user_shift': False, 
        'shifts_to': 0,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}
    elif combat['team_user_objs'][combat['active_user']].moveset[attack_user].priority > combat['team_foe_objs'][combat['active_foe']].moveset[attack_foe].priority: 
        return {'attacks': [attack_user, attack_foe],
        'user_first': True, 
        'user_shift': False, 
        'shifts_to': 0,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}
    elif combat['team_user_objs'][combat['active_user']].moveset[attack_user].priority == combat['team_foe_objs'][combat['active_foe']].moveset[attack_foe].priority: 
        if 3 in combat['team_user_objs'][combat['active_user']].status_list:
            combat['team_user_objs'][combat['active_user']].current_speed = combat['team_user_objs'][combat['active_user']].current_speed*0.5
        if 3 in combat['team_foe_objs'][combat['active_foe']].status_list:
            combat['team_foe_objs'][combat['active_foe']].current_speed = combat['team_foe_objs'][combat['active_foe']].current_speed*0.5
        if combat['team_user_objs'][combat['active_user']].current_speed > combat['team_foe_objs'][combat['active_foe']].current_speed: 
            return {'attacks': [attack_user, attack_foe],
        'user_first': True, 
        'user_shift': False, 
        'shifts_to': 0,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}
        elif combat['team_user_objs'][combat['active_user']].current_speed < combat['team_foe_objs'][combat['active_foe']].current_speed: 
            return {'attacks': [attack_user, attack_foe],
        'user_first': False, 
        'user_shift': False, 
        'shifts_to': 0,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}
        elif combat['team_user_objs'][combat['active_user']].current_speed == combat['team_foe_objs'][combat['active_foe']].current_speed: 
            random_number = random.randint(1, 6000)
            if random_number < 3001:
                return {'attacks': [attack_user, attack_foe],
        'user_first': True, 
        'user_shift': False, 
        'shifts_to': 0,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}
            else: return {'attacks': [attack_user, attack_foe],
        'user_first': False, 
        'user_shift': False, 
        'shifts_to': 0,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}

def attacking_shift(combat, chosen_pokemon):
    random_number: int
    attack_foe = choose_attack_foe()
    return {'attacks': [0, attack_foe],
        'user_first': True, 
        'user_shift': True, 
        'shifts_to': chosen_pokemon,
        'turn': 1,
        'text_onscreen': False,
        'text_message': combat['attacking']['text_message']}

def attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks):
    damage: int = 0
    list_types: list = ["bug", "dark", "dragon", "electric", "fairy", "fighting","fire","flying","ghost","grass","ground","ice","normal","poison","psychic","rock","steel","water"]
    type_: str = ''

    if attacker == 0: 
        if team_user[active_user].moveset[attacks[attacker]].power != None: 
            if team_user[active_user].moveset[attacks[attacker]].category == 'Physical': 
                damage = (40 * team_user[active_user].moveset[attacks[attacker]].power * team_user[active_user].current_att/team_foe[active_foe].current_def)/50 + 2
            elif team_user[active_user].moveset[attacks[attacker]].category == 'Special':
                damage = (40 * team_user[active_user].moveset[attacks[attacker]].power * team_user[active_user].current_sp_att/team_foe[active_foe].current_sp_def)/50 + 2
            if random.random() < 0.08:
                damage = damage*2
            damage = round(damage*(1 - (random.random()/4)))
            if team_user[active_user].moveset[attacks[attacker]].type == team_user[active_user].main_type:
                damage = damage*1.5
            elif team_user[active_user].sec_type != None:
                if team_user[active_user].moveset[attacks[attacker]].type == team_user[active_user].sec_type:
                    damage = damage*1.5
            type_ = '' + team_user[active_user].moveset[attacks[attacker]].type + '_against'
            damage = damage*types_table[type_][list_types.index(team_foe[active_foe].main_type)]
            if team_foe[active_foe].sec_type != None:
                damage = damage*types_table[type_][list_types.index(team_foe[active_foe].sec_type)]
            if 1 in team_user[active_user].status_list:
                damage = damage*0.5
            damage = int(round(damage))
            team_foe[active_foe].current_hp -= damage
            if team_foe[active_foe].current_hp < 0: 
                team_foe[active_foe].current_hp = 0
    if attacker == 1: 
        if team_foe[active_foe].moveset[attacks[attacker]].power != None: 
            if team_foe[active_foe].moveset[attacks[attacker]].category == 'Physical': 
                damage = (40 * team_foe[active_foe].moveset[attacks[attacker]].power * team_foe[active_foe].current_att/team_user[active_user].current_def)/50 + 2
            elif team_foe[active_foe].moveset[attacks[attacker]].category == 'Special':
                damage = (40 * team_foe[active_foe].moveset[attacks[attacker]].power * team_foe[active_foe].current_sp_att/team_user[active_user].current_sp_def)/50 + 2
            if random.random() < 0.08:
                damage = damage*2
            damage = round(damage*(1 - (random.random()/4)))
            if team_foe[active_foe].moveset[attacks[attacker]].type == team_foe[active_foe].main_type:
                damage = damage*1.5
            if team_foe[active_foe].sec_type != None:
                if team_foe[active_foe].moveset[attacks[attacker]].type == team_foe[active_foe].sec_type:
                    damage = damage*1.5
            type_ = '' + team_foe[active_foe].moveset[attacks[attacker]].type + '_against'
            damage = damage*types_table[type_][list_types.index(team_user[active_user].main_type)]
            if team_user[active_user].sec_type != None:
                damage = damage*types_table[type_][list_types.index(team_user[active_user].sec_type)]
            if 1 in team_user[active_user].status_list:
                damage = damage*0.5
            damage = int(round(damage))
            team_user[active_user].current_hp -= damage
            if team_user[active_user].current_hp < 0: 
                team_user[active_user].current_hp = 0
        
    return [team_user, team_foe, damage]

def attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks):
    i: int = 0
    if attacker == 0:
        if team_user[active_user].moveset[attacks[attacker]].status_user != None:
            i = 0
            while i < len(team_user[active_user].moveset[attacks[attacker]].status_user['affected']): 
                if random.random() <= team_user[active_user].moveset[attacks[attacker]].status_user['probability'][i]:
                    if team_user[active_user].moveset[attacks[attacker]].status_user['affected'][i] not in team_user[active_user].status_list:
                        team_user[active_user].status_list.append(team_user[active_user].moveset[attacks[attacker]].status_user['affected'][i])
                        if team_user[active_user].moveset[attacks[attacker]].status_user['turns'] != None:
                            team_user[active_user].status_turns.append(team_user[active_user].moveset[attacks[attacker]].status_user['turns'][i])
                        else: team_user[active_user].status_turns.append(random.randint(2,5))
                i += 1
        if team_user[active_user].moveset[attacks[attacker]].status_foe != None:
            i = 0
            while i < len(team_user[active_user].moveset[attacks[attacker]].status_foe['affected']): 
                if random.random() <= team_user[active_user].moveset[attacks[attacker]].status_foe['probability'][i]:
                    if team_user[active_user].moveset[attacks[attacker]].status_foe['affected'][i] not in team_foe[active_foe].status_list:
                        team_foe[active_foe].status_list.append(team_user[active_user].moveset[attacks[attacker]].status_foe['affected'][i])
                        if team_user[active_user].moveset[attacks[attacker]].status_foe['turns'] != None:
                            team_foe[active_foe].status_turns.append(team_user[active_user].moveset[attacks[attacker]].status_foe['turns'][i])
                        else: team_user[active_user].status_turns.append(random.randint(2,5))
                i += 1
    if attacker == 1:
        if team_foe[active_foe].moveset[attacks[attacker]].status_user != None:
            i = 0
            while i < len(team_foe[active_foe].moveset[attacks[attacker]].status_user['affected']): 
                if random.random() <= team_foe[active_foe].moveset[attacks[attacker]].status_user['probability'][i]:
                    if team_foe[active_foe].moveset[attacks[attacker]].status_user['affected'][i] not in team_foe[active_foe].status_list:
                        team_foe[active_foe].status_list.append(team_foe[active_foe].moveset[attacks[attacker]].status_user['affected'][i])
                        if team_foe[active_foe].moveset[attacks[attacker]].status_user['turns'] != None: 
                            team_foe[active_foe].status_turns.append(team_foe[active_foe].moveset[attacks[attacker]].status_user['turns'][i])
                        else: team_foe[active_foe].status_turns.append(random.randint(2,5))
                i += 1
        if team_foe[active_foe].moveset[attacks[attacker]].status_foe != None:
            i = 0
            while i < len(team_foe[active_foe].moveset[attacks[attacker]].status_foe['affected']): 
                if random.random() <= team_foe[active_foe].moveset[attacks[attacker]].status_foe['probability'][i]:
                    if team_foe[active_foe].moveset[attacks[attacker]].status_foe['affected'][i] not in team_user[active_user].status_list:
                        team_user[active_user].status_list.append(team_foe[active_foe].moveset[attacks[attacker]].status_foe['affected'][i])
                        if team_foe[active_foe].moveset[attacks[attacker]].status_foe['turns'] != None:
                            team_user[active_user].status_turns.append(team_foe[active_foe].moveset[attacks[attacker]].status_foe['turns'][i])
                        else: team_user[active_user].status_turns.append(random.randint(2,5))
                i += 1
    return [team_user, team_foe]

def attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt):
    if attacker == 0:
        if team_user[active_user].moveset[attacks[attacker]].hp_user != None:
            if team_user[active_user].moveset[attacks[attacker]].hp_user[0] == 0:
                team_user[active_user].current_hp += damage_dealt*team_user[active_user].moveset[attacks[attacker]].hp_user[1]
            if team_user[active_user].moveset[attacks[attacker]].hp_user[0] == 1:
                team_user[active_user].current_hp += team_user[active_user].HP*team_user[active_user].moveset[attacks[attacker]].hp_user[1]
            if team_user[active_user].moveset[attacks[attacker]].hp_user[0] == 2:
                team_user[active_user].current_hp += team_foe[active_foe].HP*team_user[active_user].moveset[attacks[attacker]].hp_user[1]
            if team_user[active_user].moveset[attacks[attacker]].hp_user[0] == 3:
                team_user[active_user].current_hp += team_user[active_user].moveset[attacks[attacker]].hp_user[1]
        if team_user[active_user].moveset[attacks[attacker]].hp_foe != None:
            if team_user[active_user].moveset[attacks[attacker]].hp_foe[0] == 0:
                team_foe[active_foe].current_hp += damage_dealt*team_user[active_user].moveset[attacks[attacker]].hp_foe[1]
            if team_user[active_user].moveset[attacks[attacker]].hp_foe[0] == 1:
                team_foe[active_foe].current_hp += team_user[active_user].HP*team_user[active_user].moveset[attacks[attacker]].hp_foe[1]
            if team_user[active_user].moveset[attacks[attacker]].hp_foe[0] == 2:
                team_foe[active_foe].current_hp += team_foe[active_foe].HP*team_user[active_user].moveset[attacks[attacker]].hp_foe[1]
            if team_user[active_user].moveset[attacks[attacker]].hp_foe[0] == 3:
                team_foe[active_foe].current_hp += team_user[active_user].moveset[attacks[attacker]].hp_foe[1]
    if attacker == 1:
        if team_foe[active_foe].moveset[attacks[attacker]].hp_user != None:
            if team_foe[active_foe].moveset[attacks[attacker]].hp_user[0] == 0:
                team_foe[active_foe].current_hp += damage_dealt*team_foe[active_foe].moveset[attacks[attacker]].hp_user[1]
            if team_foe[active_foe].moveset[attacks[attacker]].hp_user[0] == 1:
                team_foe[active_foe].current_hp += team_foe[active_foe].HP*team_foe[active_foe].moveset[attacks[attacker]].hp_user[1]
            if team_foe[active_foe].moveset[attacks[attacker]].hp_user[0] == 2:
                team_foe[active_foe].current_hp += team_foe[active_foe].HP*team_foe[active_foe].moveset[attacks[attacker]].hp_user[1]
            if team_foe[active_foe].moveset[attacks[attacker]].hp_user[0] == 3:
                team_foe[active_foe].current_hp += team_foe[active_foe].moveset[attacks[attacker]].hp_user[1]
        if team_foe[active_foe].moveset[attacks[attacker]].hp_foe != None:
            if team_foe[active_foe].moveset[attacks[attacker]].hp_foe[0] == 0:
                team_user[active_user].current_hp += damage_dealt*team_foe[active_foe].moveset[attacks[attacker]].hp_foe[1]
            if team_foe[active_foe].moveset[attacks[attacker]].hp_foe[0] == 1:
                team_user[active_user].current_hp += team_foe[active_foe].HP*team_foe[active_foe].moveset[attacks[attacker]].hp_foe[1]
            if team_foe[active_foe].moveset[attacks[attacker]].hp_foe[0] == 2:
                team_user[active_user].current_hp += team_foe[active_foe].HP*team_foe[active_foe].moveset[attacks[attacker]].hp_foe[1]
            if team_foe[active_foe].moveset[attacks[attacker]].hp_foe[0] == 3:
                team_user[active_user].current_hp += team_foe[active_foe].moveset[attacks[attacker]].hp_foe[1]
    team_foe[active_foe].current_hp = int(round(team_foe[active_foe].current_hp))
    team_user[active_user].current_hp = int(round(team_user[active_user].current_hp))
    if team_foe[active_foe].current_hp > team_foe[active_foe].HP:
        team_foe[active_foe].current_hp = team_foe[active_foe].HP
    if team_foe[active_foe].current_hp < 0:
        team_foe[active_foe].current_hp = 0
    if team_user[active_user].current_hp > team_user[active_user].HP:
        team_user[active_user].current_hp = team_user[active_user].HP
    if team_user[active_user].current_hp < 0:
        team_user[active_user].current_hp = 0
    return [team_user, team_foe]

def status_effect(team, active):
    i: int = 0
    burnt: bool = False
    poisoned: bool = False
    apply_hazard: bool = False

    while i < len(team[active].status_turns):
        if team[active].status_turns[i] == 0: 
            team[active].status_turns.pop(i)
            team[active].status_list.pop(i)
        else: i += 1
    i = 0
    print(team[active].name, team[active].status_list, team[active]. status_turns)
    if team[active].status_list != None:
        while i < len(team[active].status_list):
            if team[active].status_list[i] == 1: 
                team[active].current_hp -= team[active].HP/8
                burnt = True
            elif team[active].status_list[i] == 4:
                team[active].current_hp -= team[active].HP/8
                poisoned = True
            elif team[active].status_list[i] == 5:
                team[active].current_hp -= team[active].HP/6
                poisoned = True
            elif team[active].status_list[i] == 37:
                apply_hazard = True
                
            if team[active].status_turns[i] != None:
                team[active].status_turns[i] -= 1

            i += 1
    return [team, burnt, poisoned, apply_hazard]

def attack(types_table, combat, attacker):
    attack_functions_output: list
    attack_power_output: None
    damage_dealt: int
    hazard = []

    if attacker == 0: 
        attack_functions_output = status_effect(combat['team_user_objs'], combat['active_user'])
        combat['team_user_objs'] = attack_functions_output[0]
        if attack_functions_output[3] == True: 
            hazard.append(0)
        attack_functions_output = status_effect(combat['team_foe_objs'], combat['active_foe'])
        combat['team_foe_objs'] = attack_functions_output[0]
        if attack_functions_output[3] == True: 
            hazard.append(1)
        if 10 not in combat['team_user_objs'][combat['active_user']].status_list:
            if 31 not in combat['team_foe_objs'][combat['active_foe']].status_list:
                if (9 in combat['team_user_objs'][combat['active_user']].status_list) and (random.random() < 0.33):
                    combat['team_user_objs'][combat['active_user']].current_hp -= (40 * 40 * combat['team_user_objs'][combat['active_user']].current_att/combat['team_user_objs'][combat['active_user']].current_def)/50 + 2
                else: 
                    if combat['team_user_objs'][combat['active_user']].moveset[combat['attacking']['attacks'][attacker]].accuracy != None:
                        if random.random() < (combat['team_user_objs'][combat['active_user']].moveset[combat['attacking']['attacks'][attacker]].accuracy*combat['team_user_objs'][combat['active_user']].accuracy*combat['team_foe_objs'][combat['active_foe']].accuracy):
                            failed = False
                            attack_functions_output = attack_power(types_table, combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                            combat['team_user_objs'] = attack_functions_output[0]
                            combat['team_foe_objs'] = attack_functions_output[1]
                            damage_dealt = attack_functions_output[2]
                            print('user', str(damage_dealt))
                            attack_functions_output = attack_status(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                            combat['team_user_objs'] = attack_functions_output[0]
                            combat['team_foe_objs'] = attack_functions_output[1]
                            attack_functions_output = attack_hp(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'], damage_dealt)
                            combat['team_user_objs'] = attack_functions_output[0]
                            combat['team_foe_objs'] = attack_functions_output[1]
                        else: 
                            failed = True
                            print('failed')
                    else:
                        attack_power_output = attack_power(types_table, combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                        combat['team_user_objs'] = attack_power_output[0]
                        combat['team_foe_objs'] = attack_power_output[1]
                        damage_dealt = attack_power_output[2]
                        print('user', str(damage_dealt))
                        attack_functions_output = attack_status(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                        combat['team_user_objs'] = attack_functions_output[0]
                        combat['team_foe_objs'] = attack_functions_output[1]
                        attack_functions_output = attack_hp(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'], damage_dealt)
                        combat['team_user_objs'] = attack_functions_output[0]
                        combat['team_foe_objs'] = attack_functions_output[1]
            else: print(combat['team_foe_objs'][combat['active_foe']].name + ' is protecting himself')
        else: print(combat['team_user_objs'][combat['active_user']].name + ' flinched!')
    else: 
        if 10 not in combat['team_foe_objs'][combat['active_foe']].status_list:
            if 31 not in combat['team_user_objs'][combat['active_user']].status_list:
                if (9 in combat['team_foe_objs'][combat['active_foe']].status_list) and (random.random() < 0.33):
                    combat['team_foe_objs'][combat['active_foe']].current_hp -= (40 * 40 * combat['team_foe_objs'][combat['active_foe']].current_att/combat['team_foe_objs'][combat['active_foe']].current_def)/50 + 2
                else:
                    if combat['team_foe_objs'][combat['active_foe']].moveset[combat['attacking']['attacks'][attacker]].accuracy != None:
                        if random.random() < (combat['team_foe_objs'][combat['active_foe']].moveset[combat['attacking']['attacks'][attacker]].accuracy*combat['team_foe_objs'][combat['active_foe']].accuracy*combat['team_user_objs'][combat['active_user']].accuracy):
                            failed = False
                            attack_functions_output = attack_power(types_table, combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                            combat['team_user_objs'] = attack_functions_output[0]
                            combat['team_foe_objs'] = attack_functions_output[1]
                            damage_dealt = attack_functions_output[2]
                            print('foe', str(damage_dealt))
                            attack_functions_output = attack_status(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                            combat['team_user_objs'] = attack_functions_output[0]
                            combat['team_foe_objs'] = attack_functions_output[1]
                            attack_functions_output = attack_hp(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'], damage_dealt)
                            combat['team_user_objs'] = attack_functions_output[0]
                            combat['team_foe_objs'] = attack_functions_output[1]
                        else: 
                            failed = True
                            print('failed')
                    else:
                        attack_power_output = attack_power(types_table, combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                        combat['team_user_objs'] = attack_power_output[0]
                        combat['team_foe_objs'] = attack_power_output[1]
                        damage_dealt = attack_power_output[2]
                        print('foe', str(damage_dealt))
                        attack_functions_output = attack_status(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'])
                        combat['team_user_objs'] = attack_functions_output[0]
                        combat['team_foe_objs'] = attack_functions_output[1]
                        attack_functions_output = attack_hp(combat['team_user_objs'], combat['active_user'], combat['team_foe_objs'], combat['active_foe'], attacker, combat['attacking']['attacks'], damage_dealt)
                        combat['team_user_objs'] = attack_functions_output[0]
                        combat['team_foe_objs'] = attack_functions_output[1]
            else: print(combat['team_user_objs'][combat['active_user']].name + ' is protecting himself')
        else: print(combat['team_foe_objs'][combat['active_foe']].name + ' flinched!')
        combat['team_foe_objs'][combat['active_foe']].moveset[combat['attacking']['attacks'][attacker]].spendPP()
    return combat

def shift_foe(combat):
    i = 0
    while i < len(combat['team_foe_objs']): 
        if combat['team_foe_objs'][i].ko == False: 
            combat['active_foe'] = i
            i += len(combat['team_foe_objs'])
        i += 1
    return combat

def check_life(combat): 
    user_ko = False

    if combat['team_foe_objs'][combat['active_foe']].current_hp <= 0: 
        combat['team_foe_objs'][combat['active_foe']].current_hp = 0
        combat['team_foe_objs'][combat['active_foe']].ko = True
    if combat['team_user_objs'][combat['active_user']].current_hp <= 0: 
        combat['team_user_objs'][combat['active_user']].current_hp = 0
        combat['team_user_objs'][combat['active_user']].ko = True
    return combat

def check_ko(combat): 
    user_ko = False

    combat = check_life(combat)

    if combat['team_foe_objs'][combat['active_foe']].ko == True: 
        combat = shift_foe(combat)
    if combat['team_user_objs'][combat['active_user']].ko == True: 
        user_ko = True
    return [user_ko, combat]

def battle(combat): 
    types_table: dict
    with open(os.path.join(os.path.dirname(__file__), 'data/types.json'), 'r') as f_types:
        types_table = json.load(f_types)
    if combat['attacking']['turn'] == 1:
        print('turn 1')
        if combat['attacking']['user_shift'] == True: 
            combat['active_user'] = combat['attacking']['shifts_to']
        else: 
            if combat['attacking']['user_first'] == True: 
                combat = attack(types_table, combat, 0)
                combat['attacking']['text_onscreen'] = True
                combat['attacking']['text_message'] = combat['team_user_objs'][combat['active_user']].name + ' used ' + combat['team_user_objs'][combat['active_user']].moveset[combat['attacking']['attacks'][0]].name
            else: 
                combat = attack(types_table, combat, 1)
                combat['attacking']['text_onscreen'] = True
                combat['attacking']['text_message'] = 'The foe ' + combat['team_foe_objs'][combat['active_foe']].name + ' used ' + combat['team_foe_objs'][combat['active_foe']].moveset[combat['attacking']['attacks'][1]].name
    elif combat['attacking']['turn'] == 2: 
        print('turn 2')
        if combat['attacking']['user_shift'] == True: 
            combat = attack(types_table, combat, 1)
            combat['attacking']['text_onscreen'] = True
            combat['attacking']['text_message'] = 'The foe ' + combat['team_foe_objs'][combat['active_foe']].name + ' used ' + combat['team_foe_objs'][combat['active_foe']].moveset[combat['attacking']['attacks'][1]].name
        elif combat['attacking']['user_first'] == True: 
            combat = attack(types_table, combat, 1)
            combat['attacking']['text_onscreen'] = True
            combat['attacking']['text_message'] = 'The foe ' + combat['team_foe_objs'][combat['active_foe']].name + ' used ' + combat['team_foe_objs'][combat['active_foe']].moveset[combat['attacking']['attacks'][1]].name
        else: 
            combat = attack(types_table, combat, 0)
            combat['attacking']['text_onscreen'] = True
            combat['attacking']['text_message'] = combat['team_user_objs'][combat['active_user']].name + ' used ' + combat['team_user_objs'][combat['active_user']].moveset[combat['attacking']['attacks'][0]].name
    combat['attacking']['turn'] += 1
    return combat

def load_images(to_build):
    images_list: list = []
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'images')):
        if filename.startswith(to_build + '_'):
            images_list.append(pygame.image.load(os.path.join(os.path.dirname(__file__)+'\\images', filename).replace('/', '\\')))
    return images_list

def load_poke_sprites_tiny():
    sprites_list: list = []
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/pokemon/tiny').replace('/', '\\')):
        sprites_list.append(pygame.image.load(os.path.join(os.path.dirname(__file__) + '/sprites/pokemon/tiny', filename).replace('/', '\\')))
    return sprites_list

def load_poke_sprites_big(view):
    sprites_list: list = []
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/pokemon/big/' + view).replace('/', '\\')):
        sprites_list.append(pygame.image.load(os.path.join(os.path.dirname(__file__) + '/sprites/pokemon/big/' + view, filename).replace('/', '\\')))
    return sprites_list

def load_type_sprites(size):
    sprites_list: list = []
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/types/' + size).replace('/', '\\')):
        sprites_list.append(pygame.image.load(os.path.join(os.path.dirname(__file__) + '/sprites/types/' + size, filename).replace('/', '\\')))
    return sprites_list

def load_attack_sprites():
    sprites_list: list = []
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/attacks').replace('/', '\\')):
        sprites_list.append(pygame.image.load(os.path.join(os.path.dirname(__file__) + '/sprites/attacks', filename).replace('/', '\\')))
    return sprites_list

def playlist_music(SONG_END):
    pygame.mixer.music.set_endevent(SONG_END)
    song_rel_path = os.path.join(os.path.dirname(__file__), 'music/song_' + str(random.randint(1,5)) + '.mp3')
    pygame.mixer.music.load(song_rel_path)
    for i in range(13):
        song_rel_path = os.path.join(os.path.dirname(__file__), 'music/song_' + str(random.randint(1,5)) + '.mp3')
        pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.set_volume(0.35)
    return pygame.mixer.music

def blit_menu(screen, resources): 
    counter = 0
    screen.fill((255, 255, 255))
    for image in resources['images_menu']: 
        if resources['images_menu'].index(image) != 0:
            screen.blit(image, [731, 117 + 131*counter])
            counter += 1
        else: screen.blit(image, [0, 0])
    screen.blit(resources['font_roboto_medium_20'].render("Héctor Álvarez Fernández, CDAV UDC, 2020", True, (128,128,128)), [970, 743])
    return screen

def blit_builder(screen, resources, team, active): 
    counter = 1
    counter_i = 0
    counter_j = 0
    dir_py = os.path.dirname(__file__)
    rel_path = 'data/pokedex.json'
    sprites_list = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/pokemon/tiny/'))
    types_list = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/types/tiny/'))
    screen.fill((255, 255, 255))
    for image in resources['images_builder']: 
        if resources['images_builder'].index(image) == 0:    # render background
            screen.blit(image, [0, 0])
        elif resources['images_builder'].index(image) == 1:  # render party title
            screen.blit(image, [18, 18])
        elif resources['images_builder'].index(image) == 2:  # render party buttons active
            while counter_i < 6: 
                if counter_i == active: 
                    screen.blit(image, [30, 95 + 110*counter_i])
                counter_i += 1
            counter_i = 0
        elif resources['images_builder'].index(image) == 5:  # render party buttons inactive
            while counter_i < 6: 
                if counter_i != active: 
                    screen.blit(image, [18, 95 + 110*counter_i])
                counter_i += 1
        elif resources['images_builder'].index(image) == 3:  # render box titles
            screen.blit(image, [780, 55])
        elif resources['images_builder'].index(image) == 6:  # render back arrow
            screen.blit(image, [1280, 680])
        elif resources['images_builder'].index(image) == 4:  # render box buttons
            while counter_j < 5: 
                while counter_i < 6: 
                    screen.blit(image, [672 + 110*counter_i, 160 + 110*counter_j])
                    if counter_j == 4 and counter_i == 3:
                        counter_i += 4
                    else: counter_i += 1
                counter_i = 0
                counter_j += 1
        counter_i = 0
        counter_j = 0
    with open(os.path.join(dir_py, rel_path), 'r') as f_pokedex:        # blits button content
        dic_pokedex = json.load(f_pokedex)
        for id in team:
            if id != 0:
                index_ = str(id) + '.png'
                if len(index_) < 7: 
                    index_ = '0' + index_
                if len(index_) < 7: 
                    index_ = '0' + index_
                screen.blit(resources['sprites_poke_tiny'][sprites_list.index(index_)], [35, 118 + 110*(team.index(id))])
                screen.blit(resources['font_roboto_medium_24'].render(dic_pokedex[str(id)]['name'], True, (90,90,90)), [120, 115 + 110*(team.index(id))])
                screen.blit(resources['sprites_types_tiny'][types_list.index(dic_pokedex[str(id)]['mainType'] + '.png')], [120, 150 + 110*(team.index(id))])
                if dic_pokedex[str(id)]['secType'] != None: 
                    screen.blit(resources['sprites_types_tiny'][types_list.index(dic_pokedex[str(id)]['secType'] + '.png')], [128 + resources['sprites_types_tiny'][types_list.index(dic_pokedex[str(id)]['mainType'] + '.png')].get_width(), 150 + 110*(team.index(id))])
    while counter_j < 5:                                    # render box sprites
        while counter_i < 6: 
            screen.blit(resources['sprites_poke_tiny'][counter], [675 + 110*counter_i, 168 + 110*counter_j])
            counter += 1
            if counter_j == 4 and counter_i == 3:
                counter_i += 4
            else: counter_i += 1
        counter_i = 0
        counter_j += 1
    return screen

def blit_guide(screen, resources):
    counter = 0
    screen.fill((255, 255, 255))
    for image in resources['images_guide']: 
        if counter != 2:
            screen.blit(image, [0, 0])
        else:
            screen.blit(image, [50, 680])
        counter += 1
    screen.blit(resources['font_roboto_medium_20'].render("Pokémon Exercitium is a fan-made battle simulator based on Nintendo's Pokémon.", True, (80,80,80)), [580, 240])
    screen.blit(resources['font_roboto_medium_20'].render("Mechanic's are a simplified version of those we can find in the Pokémon Core Series. ", True, (80,80,80)), [580, 290])
    screen.blit(resources['font_roboto_medium_20'].render("The Pokédex is reduced to 28 monsters, all from the first generation. ", True, (80,80,80)), [580, 315])
    screen.blit(resources['font_roboto_medium_20'].render("Levels and IVs are maxed-out and EVs equally balanced. ", True, (80,80,80)), [580, 340])
    screen.blit(resources['font_roboto_medium_20'].render("The moveset of each Pokémon is predefined. ", True, (80,80,80)), [580, 365])
    screen.blit(resources['font_roboto_medium_20'].render("There is a pre-made team, but it can be modified in the Team Builder menu. ", True, (80,80,80)), [580, 415])
    screen.blit(resources['font_roboto_medium_20'].render("Once ready, hit the Combat button and do your best!", True, (80,80,80)), [580, 465])
    return screen

def remove_duplicates(list):
    clean_list = [] 
    for i in list: 
        if i not in clean_list: 
            clean_list.append(i) 
    while len(clean_list) < 6:
        clean_list.append(0)
    return clean_list 

def blit_battle_common(screen, resources, dic_pokedex, sprites_list_front, sprites_list_back, combat):
    hp_bar_foe_posx = 1050
    hp_bar_foe_posy = 107
    hp_bar_foe = (hp_bar_foe_posx, hp_bar_foe_posy, 300, 20)
    hp_bar_user_posx = 10
    hp_bar_user_posy = 250
    hp_bar_user = (hp_bar_user_posx, hp_bar_user_posy, 300, 20)
    division: int
    screen.fill((255, 255, 255))
    screen.blit(resources['images_battle'][0], [0, 0])
    index_ = str(combat['team_user_objs'][combat['active_user']].p_id) + '.png'
    if len(index_) < 7: 
        index_ = '0' + index_
    if len(index_) < 7: 
        index_ = '0' + index_
    screen.blit(resources['sprites_poke_big_back'][sprites_list_back.index(index_)], [-50, 200])
    index_ = str(combat['team_foe_objs'][combat['active_foe']].p_id) + '.png'
    if len(index_) < 7: 
        index_ = '0' + index_
    if len(index_) < 7: 
        index_ = '0' + index_
    screen.blit(resources['sprites_poke_big_front'][sprites_list_front.index(index_)], [555, 33])
    for image in resources['images_battle']: 
        if resources['images_battle'].index(image) < 3 and resources['images_battle'].index(image) > 0:
            screen.blit(image, [0, 0])
    screen.blit(resources['font_roboto_medium_28'].render(combat['team_user_objs'][combat['active_user']].name, True, (70,70,70)), [10, 210])
    screen.blit(resources['font_roboto_medium_24'].render(str(combat['team_user_objs'][combat['active_user']].current_hp) + '/' + str(combat['team_user_objs'][combat['active_user']].HP), True, (100,100,100)), [210, 214])
    screen.blit(resources['font_roboto_medium_28'].render(combat['team_foe_objs'][combat['active_foe']].name, True, (70,70,70)), [1050, 70])
    screen.blit(resources['font_roboto_medium_24'].render(str(combat['team_foe_objs'][combat['active_foe']].current_hp) + '/' + str(combat['team_foe_objs'][combat['active_foe']].HP), True, (100,100,100)), [1260, 74])
    pygame.draw.rect(screen, (170, 170, 170), hp_bar_user)
    division = combat['team_user_objs'][combat['active_user']].current_hp/combat['team_user_objs'][combat['active_user']].HP
    if division > 0.5: 
        pygame.draw.rect(screen, (178, 217, 48), (hp_bar_user[0], hp_bar_user[1], int(hp_bar_user[2]*division), hp_bar_user[3]))
    elif division <= 0.5 and division > 0.2: 
        pygame.draw.rect(screen, (236, 179, 30), (hp_bar_user[0], hp_bar_user[1], int(hp_bar_user[2]*division), hp_bar_user[3]))
    if division <= 0.2: 
        pygame.draw.rect(screen, (214, 39, 39), (hp_bar_user[0], hp_bar_user[1], int(hp_bar_user[2]*division), hp_bar_user[3]))
    pygame.draw.rect(screen, (170, 170, 170), hp_bar_foe)
    division = combat['team_foe_objs'][combat['active_foe']].current_hp/combat['team_foe_objs'][combat['active_foe']].HP
    if division > 0.5: 
        pygame.draw.rect(screen, (178, 217, 48), (hp_bar_foe[0], hp_bar_foe[1], int(hp_bar_foe[2]*division), hp_bar_foe[3]))
    elif division <= 0.5 and division > 0.2: 
        pygame.draw.rect(screen, (236, 179, 30), (hp_bar_foe[0], hp_bar_foe[1], int(hp_bar_foe[2]*division), hp_bar_foe[3]))
    if division <= 0.2: 
        pygame.draw.rect(screen, (214, 39, 39), (hp_bar_foe[0], hp_bar_foe[1], int(hp_bar_foe[2]*division), hp_bar_foe[3]))
    return screen

def blit_battle_0(screen, resources):
    counter = 0
    for image in resources['images_battle']: 
        if resources['images_battle'].index(image) >= 3 and resources['images_battle'].index(image) <= 5:
            screen.blit(image, [968, 660 - 100*counter])
            counter += 1
    return screen

def blit_battle_text(screen, resources, text: str):
    screen.blit(resources['images_battle'][9], [0, 0])
    screen.blit(resources['font_roboto_medium_24'].render(text, True, (90, 90, 90)), [10, 573])
    return screen

def blit_battle_1(screen, resources, combat):
    counter = 1
    dic_pokedex: None
    sprites_list = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/pokemon/tiny/'))
    types_list = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/types/tiny/'))
    # alive = 0
    # for i in combat['team_user_objs']: 
    #     if i.ko == False:
    #         alive += 1
    for image in resources['images_battle']: 
        if resources['images_battle'].index(image) == 6:
            screen.blit(image, [968, 660])
        elif resources['images_battle'].index(image) == 7:
            for i in range(len(combat['team_user_objs']) - 1): 
                screen.blit(image, [968, 660 - 100*(i + 1)])
    with open(os.path.join(os.path.dirname(__file__), 'data/pokedex.json'), 'r') as f_pokedex:
        dic_pokedex = json.load(f_pokedex)
    for i in combat['team_user_ids']:
        if combat['team_user_ids'].index(i) != combat['active_user']:
            if i != 0:
                index_ = str(i) + '.png'
                if len(index_) < 7: 
                    index_ = '0' + index_
                if len(index_) < 7: 
                    index_ = '0' + index_
                screen.blit(resources['sprites_poke_tiny'][sprites_list.index(index_)], [975, 680 - 100*counter])
                screen.blit(resources['font_roboto_medium_24'].render(dic_pokedex[str(i)]['name'], True, (90,90,90)), [1050, 680 - 100*counter])
                screen.blit(resources['font_roboto_medium_28'].render(str(combat['team_user_objs'][combat['team_user_ids'].index(i)].current_hp) + '/' + str(combat['team_user_objs'][combat['team_user_ids'].index(i)].HP), True, (200,200,200)), [1215, 700 - 100*counter])
                screen.blit(resources['sprites_types_tiny'][types_list.index(dic_pokedex[str(i)]['mainType'] + '.png')], [1050, 710 - 100*counter])
                if dic_pokedex[str(i)]['secType'] != None: 
                    screen.blit(resources['sprites_types_tiny'][types_list.index(dic_pokedex[str(i)]['secType'] + '.png')], [1060 + resources['sprites_types_tiny'][types_list.index(dic_pokedex[str(i)]['mainType'] + '.png')].get_width(), 710 - 100*counter])
            counter += 1
    return screen

def blit_battle_2(screen, resources, combat):
    counter = 1
    sprites_list = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/attacks/'))
    types_list = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/types/tiny/'))
    for image in resources['images_battle']: 
        if resources['images_battle'].index(image) == 6:
            screen.blit(image, [968, 660])
        elif resources['images_battle'].index(image) == 8:
            for i in range(4): 
                screen.blit(image, [968, 660 - 100*(i + 1)])
    for i in combat['team_user_objs'][combat['active_user']].moveset:
        screen.blit(resources['font_roboto_medium_24'].render(combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].name, True, (90, 90, 90)), [1008, 683 - 100*counter])
        screen.blit(resources['sprites_types_tiny'][types_list.index(combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].type + '.png')], [1300, 678 - 100*counter])
        power = str(combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].power)
        if power == 'None': 
            power = ' -'
        screen.blit(resources['font_roboto_medium_24'].render(power, True, (90, 90, 90)), [1033, 717 - 100*counter])
        screen.blit(resources['sprites_attack'][sprites_list.index('01_power.png')], [1008, 720 - 100*counter])
        accuracy = combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].accuracy
        if accuracy == None:
            accuracy = ' -'
        else: 
            accuracy = str(int(accuracy*100))
        screen.blit(resources['font_roboto_medium_24'].render(accuracy, True, (90, 90, 90)), [1117, 717 - 100*counter])
        screen.blit(resources['sprites_attack'][sprites_list.index('00_accuracy.png')], [1090, 720 - 100*counter])
        if combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].category == 'Physical':
            screen.blit(resources['sprites_attack'][sprites_list.index('02_physical.png')], [1250, 678 - 100*counter])
        elif combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].category == 'Special':
            screen.blit(resources['sprites_attack'][sprites_list.index('03_special.png')], [1250, 678 - 100*counter])
        else:
            screen.blit(resources['sprites_attack'][sprites_list.index('04_status.png')], [1250, 678 - 100*counter])
        screen.blit(resources['font_roboto_medium_24'].render(str(combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].pps) + '/' + str(combat['team_user_objs'][combat['active_user']].moveset[combat['team_user_objs'][combat['active_user']].moveset.index(i)].max_pps), True, (240, 240, 240)), [1250, 720 - 100*counter])
        counter += 1
    return screen

def battle_gui(screen, resources, combat): 
    sprites_list_front = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/pokemon/big/front/'))
    sprites_list_back = os.listdir(os.path.join(os.path.dirname(__file__), 'sprites/pokemon/big/back/'))
    with open(os.path.join(os.path.dirname(__file__), 'data/pokedex.json'), 'r') as f_pokedex:
        dic_pokedex = json.load(f_pokedex)
    screen = blit_battle_common(screen, resources, dic_pokedex, sprites_list_front, sprites_list_back, combat)
    if combat['battle_status'] == 0: 
        screen = blit_battle_0(screen, resources)
    elif combat['battle_status'] == 1: 
        screen = blit_battle_1(screen, resources, combat)
    elif combat['battle_status'] == 2: 
        screen = blit_battle_2(screen, resources, combat)
    elif combat['battle_status'] == 3: 
        screen = blit_battle_text(screen, resources, combat['attacking']['text_message'])

    return screen

def check_buttons(game_status, screen, resources, mouse_pos, combat): 
    resources_ = []
    buttons_list: list = []
    sizes: list = [131, 110, 100]
    positions: list = [731, 117, 30, 95, 672, 160, 1280, 680, 968, 660, 50, 680]
    counter = 0
    counter_i = 0
    counter_j = 0
    returned_value = None
    if game_status == 0: 
        counter += 1
        while counter < len(resources['images_menu']):       # load list in local variable
            resources_.append(resources['images_menu'][counter])
            counter += 1
        counter = 0
        for img in resources_: 
            buttons_list.append(img.get_rect())
            buttons_list[counter][0] = positions[0]
            buttons_list[counter][1] = positions[1] + sizes[0]*(counter)
            counter += 1
        counter = 0
        while counter < len(buttons_list):
            if buttons_list[counter].collidepoint(mouse_pos):
                returned_value = counter + 1
            counter += 1
    elif game_status == 1:
        resources_.append(resources['images_builder'][2])
        resources_.append(resources['images_builder'][4])
        resources_.append(resources['images_builder'][6])
        counter = 0
        while counter < 6: 
            buttons_list.append(resources_[0].get_rect())
            buttons_list[counter][0] = positions[2]
            buttons_list[counter][1] = positions[3] + sizes[1]*(counter)
            counter += 1
        counter = 0
        while counter < 28: 
            buttons_list.append(resources_[1].get_rect())
            counter += 1
        counter = 0
        buttons_list.append(resources_[2].get_rect())
        buttons_list[-1][0] = positions[6]
        buttons_list[-1][1] = positions[7]
        while counter_j < 5: 
            while counter_i < 6: 
                buttons_list[6 + counter][0] = positions[4] + sizes[1]*counter_i
                buttons_list[6 + counter][1] = positions[5] + sizes[1]*counter_j
                if counter_j == 4 and counter_i == 3:
                    counter_i += 4
                    counter += 1
                else: 
                    counter_i += 1
                    counter += 1
            counter_i = 0
            counter_j += 1
        counter = 0
        while counter < len(buttons_list):
            if buttons_list[counter].collidepoint(mouse_pos):
                returned_value = counter
            counter += 1
    elif game_status == 2: 
        if combat['battle_status'] == 0: 
            counter = 0
            while counter < 3: 
                resources_.append(resources['images_battle'][3 + counter])
                counter += 1
            counter = 0
            for img in resources_: 
                buttons_list.append(img.get_rect())
                buttons_list[counter][0] = positions[8]
                buttons_list[counter][1] = positions[9] - sizes[2]*counter
                counter += 1
            counter = 0
            while counter < len(buttons_list):
                if buttons_list[counter].collidepoint(mouse_pos):
                    returned_value = counter + 1
                counter += 1
        elif combat['battle_status'] == 1: 
            counter = 0
            while counter < 2: 
                resources_.append(resources['images_battle'][6 + counter])
                counter += 1
            for img in resources_: 
                if resources_.index(img) == 0:
                    buttons_list.append(img.get_rect())
                    buttons_list[0][0] = positions[8]
                    buttons_list[0][1] = positions[9]
                else: 
                    for i in range(len(combat['team_user_objs']) - 1):
                        buttons_list.append(img.get_rect())
                        buttons_list[i + 1][0] = positions[8]
                        buttons_list[i + 1][1] = positions[9] - sizes[2]*(i + 1)
            counter = 0
            while counter < len(buttons_list):
                if buttons_list[counter].collidepoint(mouse_pos):
                    returned_value = counter
                counter += 1
        elif combat['battle_status'] == 2: 
            resources_.append(resources['images_battle'][6])
            resources_.append(resources['images_battle'][8])
            for img in resources_: 
                if resources_.index(img) == 0:
                    buttons_list.append(img.get_rect())
                    buttons_list[0][0] = positions[8]
                    buttons_list[0][1] = positions[9]
                else: 
                    for i in range(4):
                        buttons_list.append(img.get_rect())
                        buttons_list[i + 1][0] = positions[8]
                        buttons_list[i + 1][1] = positions[9] - sizes[2]*(i + 1)
            counter = 0
            while counter < len(buttons_list):
                if buttons_list[counter].collidepoint(mouse_pos):
                    returned_value = counter
                counter += 1
    elif game_status == 3:
        buttons_list.append(resources['images_guide'][2].get_rect())
        buttons_list[0][0] = positions[10]
        buttons_list[0][1] = positions[11]
        if buttons_list[0].collidepoint(mouse_pos):
            returned_value = 0
    return returned_value

def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.display.set_caption("Pokémon Exercitium")
    pygame.display.set_icon(pygame.image.load(os.path.dirname(__file__) + '/images/display_icon.png'))
    screen = pygame.display.set_mode((1366, 768))

    with open(os.path.join(os.path.dirname(__file__), 'data/pokedex.json'), 'r') as f_pokedex:
        dic_pokedex = json.load(f_pokedex)
    resources: dict = {
        'images_menu': load_images('menu'),
        'images_builder': load_images('builder'),
        'images_battle': load_images('battle'),
        'images_guide': load_images('guide'),
        'font_roboto_medium_20': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts/roboto_medium.ttf'), 20),
        'font_roboto_medium_24': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts/roboto_medium.ttf'), 24),
        'font_roboto_medium_28': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts/roboto_medium.ttf'), 28),
        'sprites_poke_tiny': load_poke_sprites_tiny(),
        'sprites_poke_big_front': load_poke_sprites_big('front'),
        'sprites_poke_big_back': load_poke_sprites_big('back'),
        'sprites_types_tiny': load_type_sprites('tiny'),
        'sprites_types_big': load_type_sprites('big'),
        'sprites_attack': load_attack_sprites()
    }
    
    # PyGame music
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music = playlist_music(SONG_END)
    pygame.mixer.Channel(0).set_volume(0.5)
    pygame.mixer.music.play()

    # Game logic variables
    i: int = 0
    game_status: int = 0
    functions_output: None
    ids_list = []
    combat = {
        'team_user_ids': [3, 26, 150, 115, 0, 0],
        'team_user_objs': [],
        'active_user': 0, 
        'team_foe_ids': [],
        'team_foe_objs': [],
        'active_foe': 0, 
        'new_battle': True,
        'battle_status': 0, 
        'attacking': {
            'attacks': [0, 0],
            'user_first': False, 
            'user_shift': False, 
            'shifts_to': 0,
            'turn': 0,
            'text_onscreen': False,
            'text_message': ''
            }
    }

    while True:
        functions_output = None

      # Drawing on screen
        if game_status == 0:
            screen = blit_menu(screen, resources)
        if game_status == 1: 
            screen = blit_builder(screen, resources, combat['team_user_ids'], combat['active_user'])
        if game_status == 2:
            if is_combat_possible(combat['team_user_objs'], combat['team_foe_objs']) == 0: 
                functions_output = check_ko(combat)
                if functions_output[0] == True: 
                    combat['battle_status'] = 1
                elif combat['attacking']['text_onscreen'] == False: 
                    combat = battle(combat)
                else: 
                    combat['battle_status'] = 3
                functions_output = battle_gui(screen, resources, combat)
                screen = functions_output
            elif is_combat_possible(combat['team_user_objs'], combat['team_foe_objs']) == 1: 
                combat['battle_status'] = 3
                combat['attacking']['text_onscreen'] = True
                combat['attacking']['text_message'] = 'You win the battle!'
                functions_output = battle_gui(screen, resources, combat)
                screen = functions_output
            elif is_combat_possible(combat['team_user_objs'], combat['team_foe_objs']) == 2: 
                combat['battle_status'] = 3
                combat['attacking']['text_onscreen'] = True
                combat['attacking']['text_message'] = 'The foe wins the battle'
                functions_output = battle_gui(screen, resources, combat)
                screen = functions_output
        if game_status == 3: 
            screen = blit_guide(screen, resources)
        if game_status == 4:
            pygame.quit()
            sys.exit(0)

      # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == SONG_END:
                pygame.mixer.music = playlist_music(SONG_END)
                pygame.mixer.music.play()
            if event.type == pygame.MOUSEBUTTONUP: 
                mouse_pos = pygame.mouse.get_pos()
                functions_output = check_buttons(game_status, screen, resources, mouse_pos, combat)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/effects/click.ogg'), maxtime=600)
                if (game_status == 0 or game_status == 3) and functions_output != None: 
                    game_status = functions_output
                    if game_status == 2: 
                        combat['team_user_objs'] = build_team_user(combat['team_user_ids'])
                        combat['team_foe_ids'] = build_team_foe(combat['team_user_ids'])[0]
                        combat['team_foe_objs'] = build_team_foe(combat['team_user_ids'])[1]
                elif game_status == 1 and functions_output != None:
                    if functions_output < 6:
                        combat['active_user'] = functions_output
                    elif functions_output == 34:
                        combat['active_user'] = 0
                        game_status = 0
                    elif functions_output > 5:
                        functions_output -= 5
                        for i in dic_pokedex:
                            ids_list.append(dic_pokedex[i]['pid'])
                        combat['team_user_ids'][combat['active_user']] = int(dic_pokedex[str(ids_list[functions_output])]['pid'])
                        for i in range(len(combat['team_user_ids'])): 
                            if combat['team_user_ids'][i] == 0: 
                                combat['team_user_ids'].append(combat['team_user_ids'][i])
                                del(combat['team_user_ids'][i])
                        combat['team_user_ids'] = remove_duplicates(combat['team_user_ids'])
                elif game_status == 2:
                    print('status', combat['battle_status'], 'out', functions_output)
                    if combat['battle_status'] == 0 and functions_output != None: 
                        if functions_output == 1: 
                            combat['team_user_objs'] = []
                            combat['team_foe_objs'] = []
                            game_status = 0
                        elif functions_output == 2 or functions_output == 3: 
                            combat['battle_status'] = functions_output - 1
                    elif combat['battle_status'] == 1 and functions_output != None:
                        if functions_output == 0: 
                            combat['battle_status'] = 0
                        else: 
                            if functions_output <= combat['active_user']: 
                                functions_output -= 1
                            if combat['team_user_objs'][functions_output].ko == False: 
                                combat['attacking'] = attacking_shift(combat, functions_output)
                                print('active', combat['active_user'])
                                combat = battle(combat)
                                print('active', combat['active_user'])
                                combat['battle_status'] = 0
                    elif combat['battle_status'] == 2 and functions_output != None:
                        if functions_output == 0: 
                            combat['battle_status'] = 0
                        else: 
                            functions_output -= 1
                            if combat['team_user_objs'][combat['active_user']].moveset[functions_output].pps > 0: 
                                combat['attacking'] = attacking_both(combat, functions_output)
                                combat = battle(combat)
                                combat['battle_status'] = 0
                    if combat['battle_status'] == 3: 
                        combat['attacking']['text_onscreen'] = False
                        combat['battle_status'] = 0
                        if is_combat_possible(combat['team_user_objs'], combat['team_foe_objs']) == 1 or is_combat_possible(combat['team_user_objs'], combat['team_foe_objs']) == 2: 
                            game_status = 0
                     
            if game_status == 4:
                pygame.quit()
                sys.exit(0)

      # refresh screen
        pygame.display.update()
    

if __name__ == '__main__':
   main()