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
 
def build_team_user(team_user, chosen_pokemon):
    num_pokemons = len(chosen_pokemon)
    for i in range(num_pokemons):
        team_user.append(Pokemon(str(chosen_pokemon[i])))
    return team_user

def build_team_foe(team_foe, chosen_pokemon):
    list_pokemons = [3, 6, 9, 26, 62, 65, 68, 76, 78, 91, 94, 97, 112, 113, 115, 127, 130, 131, 134, 135, 136, 143, 144, 145, 146, 149, 150, 151]
    num_pokemons = len(chosen_pokemon)
    list_foe = random.sample(list_pokemons, num_pokemons)
    for i in range(num_pokemons): 
        team_foe.append(Pokemon(str(list_foe[i])))
    return team_foe

def is_combat_possible(team_user, team_foe):
    count = 0
    for i in team_user:
        if i.ko == False:
            count += 1
    if count > 0:
        count = 0
        for i in team_foe:
            if i.ko == False:
                count += 1
    if count == 0:
        return False
    else: return True

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

def attacking_order(team_user, active_user, team_foe, active_foe, attack_user):
    random_number: int
    attack_foe = random.randint(1, 16000)   #random with small ranges doesn't feel really random
    if attack_foe < 4001: 
        attack_foe = 0
    elif attack_foe < 8001:
        attack_foe = 1
    elif attack_foe < 12001:
        attack_foe = 2
    else: attack_foe = 3
    if team_user[active_user].moveset[attack_user].priority < team_foe[active_foe].moveset[attack_foe].priority: 
        return (1, 0, attack_user, attack_foe)
    elif team_user[active_user].moveset[attack_user].priority > team_foe[active_foe].moveset[attack_foe].priority: 
        return (0, 1, attack_user, attack_foe)
    elif team_user[active_user].moveset[attack_user].priority == team_foe[active_foe].moveset[attack_foe].priority: 
        if 3 in team_user[active_user].status_list:
            team_user[active_user].current_speed = team_user[active_user].current_speed*0.5
        if 3 in team_foe[active_foe].status_list:
            team_foe[active_foe].current_speed = team_foe[active_foe].current_speed*0.5
        if team_user[active_user].current_speed > team_foe[active_foe].current_speed: 
            return (0, 1, attack_user, attack_foe)
        elif team_user[active_user].current_speed < team_foe[active_foe].current_speed: 
            return (1, 0, attack_user, attack_foe)
        elif team_user[active_user].current_speed == team_foe[active_foe].current_speed: 
            random_number = random.randint(1, 6000)
            if random_number < 3001:
                return (1, 0, attack_user, attack_foe)
            else: return (0, 1, attack_user, attack_foe)

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
                        if team_user[active_user].moveset[attacks[attacker]].status_user['turns'] != None:
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
            team[active].status_turns[i].pop(i)
            team[active].status_list[i].pop(i)
        else: i += 1
        i = 0

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
                
            team[active].status_turns[i] -= 1
    return [team, burnt, poisoned, apply_hazard]

def attack(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks):
    attack_functions_output: list
    damage_dealt: int = 0
    failed = None
    hazard: list = []

    if attacker == 0:
        attack_functions_output = status_effect(team_user, active_user)
        team_user = attack_functions_output[0]
        if attack_functions_output[1] == True: 
            print('Burning damage u')
        if attack_functions_output[2] == True: 
            print('Poison damage u')
        if attack_functions_output[3] == True: 
            hazard.append(0)
        attack_functions_output = status_effect(team_foe, active_foe)
        team_foe = attack_functions_output[0]
        if attack_functions_output[1] == True: 
            print('Burning damage f')
        if attack_functions_output[2] == True: 
            print('Poison damage f')
        if attack_functions_output[3] == True: 
            hazard.append(1)
        if 10 not in team_user[active_user].status_list:
            if 31 not in team_foe[active_foe].status_list:
                if (9 in team_user[active_user].status_list) and (random.random() < 0.33):
                    team_user[active_user].current_hp -= (40 * 40 * team_user[active_user].current_att/team_user[active_user].current_def)/50 + 2
                else:
                    if team_user[active_user].moveset[attacks[attacker]].accuracy != None:
                        if random.random() < (team_user[active_user].moveset[attacks[attacker]].accuracy*team_user[active_user].accuracy*team_foe[active_foe].accuracy):
                            failed = False
                            attack_functions_output = attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                            damage_dealt = attack_functions_output[2]
                            if 20 in team_user[active_user].status_list:
                                taunted = True
                                print('taunted')
                            else: 
                                attack_functions_output = attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                                team_user = attack_functions_output[0]
                                team_foe = attack_functions_output[1]
                            attack_functions_output = attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        else: failed = True
                    else:
                        attack_power_output = attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                        team_user = attack_power_output[0]
                        team_foe = attack_power_output[1]
                        if 20 in team_user[active_user].status_list:
                            taunted = True
                            print('taunted')
                        else: 
                            attack_functions_output = attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        attack_functions_output = attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                        team_user = attack_functions_output[0]
                        team_foe = attack_functions_output[1]
            else: print(team_foe[active_foe].name + ' is protecting himself')
        else: print(team_user[active_user].name + ' flinched!')
        team_user[active_user].moveset[attacks[attacker]].spendPP()
    if attacker == 1:
        print('+++')
        if 10 not in team_foe[active_foe].status_list:
            if 31 not in team_user[active_user].status_list:
                if (9 in team_foe[active_foe].status_list) and (random.random() < 0.33):
                    team_foe[active_foe].current_hp -= (40 * 40 * team_foe[active_foe].current_att/team_foe[active_foe].current_def)/50 + 2
                else:
                    if team_foe[active_foe].moveset[attacks[attacker]].accuracy != None:
                        if random.random() < (team_foe[active_foe].moveset[attacks[attacker]].accuracy*team_foe[active_foe].accuracy*team_user[active_user].accuracy):
                            failed = False
                            print('++++'+str(team_user[active_user].current_hp))
                            attack_functions_output = attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                            damage_dealt = attack_functions_output[2]
                            print('++++'+str(damage_dealt)+str(team_user[active_user].current_hp))
                            if 20 in team_foe[active_foe].status_list:
                                taunted = True
                                print('taunted')
                            else: 
                                attack_functions_output = attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                                team_user = attack_functions_output[0]
                                team_foe = attack_functions_output[1]
                            attack_functions_output = attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        else: 
                            failed = True
                            print('failed')
                    else:
                        attack_power_output = attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                        team_user = attack_power_output[0]
                        team_foe = attack_power_output[1]
                        if 20 in team_foe[active_foe].status_list:
                            taunted = True
                            print('taunted')
                        else: 
                            attack_functions_output = attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        attack_functions_output = attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                        team_user = attack_functions_output[0]
                        team_foe = attack_functions_output[1]
            else: print(team_user[active_user].name + ' is protecting himself')
        else: print(team_foe[active_foe].name + ' flinched!')
        team_foe[active_foe].moveset[attacks[attacker]].spendPP()
    return [team_user, team_foe, failed, hazard]

def battle(chosen_pokemon):
    i: int = 0
    endCombat: bool = False
    team_user: list = []
    team_foe: list = []
    active_user: int = 0
    active_foe: int = 0
    battle_status: int = 0  #0 menu, 1  moves, 2  team, 3  exit
    menu_choice: int = 0
    attacking_order: list
    attacking_output: tuple
    attacks: list
    attack_output: list
    types_table: dict
    hazards: list = []
    dir_py = os.path.dirname(__file__)
    rel_path = 'data/types.json'
    with open(os.path.join(dir_py, rel_path), 'r') as f_types:
        types_table = json.load(f_types)

    team_user = build_team_user(team_user, chosen_pokemon)
    team_foe = build_team_foe(team_foe, chosen_pokemon)

    while endCombat != True:
        if is_combat_possible(team_user, team_foe) == False:
            battle_status = 3
        if battle_status != 3: 
            if battle_status == 0:
                menu_choice = battle_menu_main(menu_choice)
                battle_status = menu_choice
            elif battle_status == 1: 
                menu_choice = battle_menu_moves(team_user, active_user, team_foe, active_foe)
                battle_status = 0
                if menu_choice != -1:
                    attacking_output = attacking_order(team_user, active_user, team_foe, active_foe, menu_choice)
                    attacking_order = [attacking_output[0], attacking_output[1]]
                    attacks = [attacking_output[2], attacking_output[3]]
                    for attacker in attacking_order:
                        if attacker == 0 and team_user[active_user].current_hp == 0:
                            team_user.pop(active_user)
                            menu_choice = battle_menu_team(team_user, active_user)
                            active_user = menu_choice
                            battle_status = 0
                        if attacker == 1 and team_foe[active_foe].current_hp == 0:
                            team_foe.pop(active_foe)
                            if team_foe: active_foe = random.randint(0, len(team_foe))
                            else: battle_status = 0
                        attack_output = attack(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                        print('Foe used ' + str(team_foe[active_foe].moveset[attacks[1]].name))
                        team_user = attack_output[0]
                        team_foe = attack_output[1]
            elif battle_status == 2: 
                menu_choice = battle_menu_team(team_user, active_user)
                if menu_choice != -1:
                    active_user = menu_choice
                    attacking_output = attacking_order(team_user, active_user, team_foe, active_foe, menu_choice)
                    attacking_order = [attacking_output[0], attacking_output[1]]
                    attack_output = attack(types_table, team_user, active_user, team_foe, active_foe, 1, attacks)
                    team_user = attack_output[0]
                    team_foe = attack_output[1]
                battle_status = 0

        else: endCombat = True

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

def check_buttons(game_state, screen, resources, mouse_pos): 
    resources_ = []
    buttons_list: list = []
    sizes: list = [131,110]
    positions: list = [731, 117, 30, 95, 672, 160, 1280, 680]
    counter = 0
    counter_i = 0
    counter_j = 0
    returned_value: int = 0
    if game_state == 0: 
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
    elif game_state == 1:
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
    elif game_state == 3:
        buttons_list.append(resources['images_guide'][2].get_rect())
        if buttons_list[0].collidepoint(mouse_pos):
            returned_value = 0
    return returned_value


def main():
    pygame.init()
    pygame.display.set_caption("Pokémon Exercitium")
    pygame.display.set_icon(pygame.image.load(os.path.dirname(__file__) + '/images/display_icon.png'))
    screen = pygame.display.set_mode((1366, 768))
    with open(os.path.join(os.path.dirname(__file__), 'data/pokedex.json'), 'r') as f_pokedex:
        dic_pokedex = json.load(f_pokedex)
    resources: dict = {
        'images_menu': load_images('menu'),
        'images_builder': load_images('builder'),
        'images_battle': [],
        'images_guide': load_images('guide'),
        'font_roboto_medium_20': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts/roboto_medium.ttf'), 20),
        'font_roboto_medium_24': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts/roboto_medium.ttf'), 24),
        'font_roboto_medium_28': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts/roboto_medium.ttf'), 28),
        'sprites_poke_tiny': load_poke_sprites_tiny(),
        'sprites_poke_big_front': load_poke_sprites_big('front'),
        'sprites_poke_big_back': load_poke_sprites_big('back'),
        'sprites_types_tiny': load_type_sprites('tiny'),
        'sprites_types_big': load_type_sprites('big')
    }

    # PyGame music
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music = playlist_music(SONG_END)
    pygame.mixer.music.play()

    # Game logic variables
    i: int = 0
    game_state: int = 0
    ids_list = []
    team: list = [91, 9, 94, 131, 0, 0]
    active: int = 0

    while True:
      # Drawing on screen
        if game_state == 0:
            screen = blit_menu(screen, resources)
            active = 4
        if game_state == 1: 
            screen = blit_builder(screen, resources, team, active)
        if game_state == 3: 
            screen = blit_guide(screen, resources)
        if game_state == 4:
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
                button_pressed = check_buttons(game_state, screen, resources, mouse_pos)
                if game_state == 0 or game_state == 3: 
                    game_state = button_pressed
                elif game_state == 1:
                    if button_pressed < 6:
                        active = button_pressed
                    elif button_pressed == 34:
                        game_state = 0
                    elif button_pressed > 5:
                        button_pressed -= 5
                        for i in dic_pokedex:
                            ids_list.append(dic_pokedex[i]['pid'])
                        team[active] = int(dic_pokedex[str(ids_list[button_pressed])]['pid'])
                        for i in range(len(team)): 
                            if team[i] == 0: 
                                team.append(team[i])
                                del(team[i])
                        team = remove_duplicates(team)
            if game_state == 4:
                pygame.quit()
                sys.exit(0)


      # refresh screen
        pygame.display.update()
    

if __name__ == '__main__':
   main()