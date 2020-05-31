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

def Attacking_order(team_user, active_user, team_foe, active_foe, attack_user):
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

def Attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks):
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

def Attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks):
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

def Attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt):
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

def Status_effect(team, active):
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

def Attack(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks):
    attack_functions_output: list
    damage_dealt: int = 0
    failed = None
    hazard: list = []

    if attacker == 0:
        attack_functions_output = Status_effect(team_user, active_user)
        team_user = attack_functions_output[0]
        if attack_functions_output[1] == True: 
            print('Burning damage u')
        if attack_functions_output[2] == True: 
            print('Poison damage u')
        if attack_functions_output[3] == True: 
            hazard.append(0)
        attack_functions_output = Status_effect(team_foe, active_foe)
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
                            attack_functions_output = Attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                            damage_dealt = attack_functions_output[2]
                            if 20 in team_user[active_user].status_list:
                                taunted = True
                                print('taunted')
                            else: 
                                attack_functions_output = Attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                                team_user = attack_functions_output[0]
                                team_foe = attack_functions_output[1]
                            attack_functions_output = Attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        else: failed = True
                    else:
                        attack_power_output = Attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                        team_user = attack_power_output[0]
                        team_foe = attack_power_output[1]
                        if 20 in team_user[active_user].status_list:
                            taunted = True
                            print('taunted')
                        else: 
                            attack_functions_output = Attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        attack_functions_output = Attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
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
                            attack_functions_output = Attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                            damage_dealt = attack_functions_output[2]
                            print('++++'+str(damage_dealt)+str(team_user[active_user].current_hp))
                            if 20 in team_foe[active_foe].status_list:
                                taunted = True
                                print('taunted')
                            else: 
                                attack_functions_output = Attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                                team_user = attack_functions_output[0]
                                team_foe = attack_functions_output[1]
                            attack_functions_output = Attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        else: 
                            failed = True
                            print('failed')
                    else:
                        attack_power_output = Attack_power(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                        team_user = attack_power_output[0]
                        team_foe = attack_power_output[1]
                        if 20 in team_foe[active_foe].status_list:
                            taunted = True
                            print('taunted')
                        else: 
                            attack_functions_output = Attack_status(team_user, active_user, team_foe, active_foe, attacker, attacks)
                            team_user = attack_functions_output[0]
                            team_foe = attack_functions_output[1]
                        attack_functions_output = Attack_hp(team_user, active_user, team_foe, active_foe, attacker, attacks, damage_dealt)
                        team_user = attack_functions_output[0]
                        team_foe = attack_functions_output[1]
            else: print(team_user[active_user].name + ' is protecting himself')
        else: print(team_foe[active_foe].name + ' flinched!')
        team_foe[active_foe].moveset[attacks[attacker]].spendPP()
    return [team_user, team_foe, failed, hazard]

def Battle(chosen_pokemon):
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
                    attacking_output = Attacking_order(team_user, active_user, team_foe, active_foe, menu_choice)
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
                        attack_output = Attack(types_table, team_user, active_user, team_foe, active_foe, attacker, attacks)
                        print('Foe used ' + str(team_foe[active_foe].moveset[attacks[1]].name))
                        team_user = attack_output[0]
                        team_foe = attack_output[1]
            elif battle_status == 2: 
                menu_choice = battle_menu_team(team_user, active_user)
                if menu_choice != -1:
                    active_user = menu_choice
                    attacking_output = Attacking_order(team_user, active_user, team_foe, active_foe, menu_choice)
                    attacking_order = [attacking_output[0], attacking_output[1]]
                    attack_output = Attack(types_table, team_user, active_user, team_foe, active_foe, 1, attacks)
                    team_user = attack_output[0]
                    team_foe = attack_output[1]
                battle_status = 0

        else: endCombat = True

def main():
    pygame.init()
    pygame.display.set_caption("Pokémon Exercitium")
    screen = pygame.display.set_mode((1366, 768))
    dir_py = os.path.dirname(__file__)

    # PyGame fonts
    roboto_medium_rel_path = os.path.join(dir_py, 'fonts/roboto_medium.ttf')
    author_text_font = pygame.font.Font(roboto_medium_rel_path, 20)

    # PyGame variables main menu
    menu_bg_rel_path = os.path.join(dir_py, 'images/menu_bg.png')
    menu_button_builder_rel_path = os.path.join(dir_py, 'images/menu_button_builder.png')
    menu_button_combat_rel_path = os.path.join(dir_py, 'images/menu_button_combat.png')
    menu_button_guide_rel_path = os.path.join(dir_py, 'images/menu_button_guide.png')
    menu_button_quit_rel_path = os.path.join(dir_py, 'images/menu_button_quit.png')
    menu_bg_path = pygame.image.load(str(menu_bg_rel_path))
    menu_button_builder_path = pygame.image.load(str(menu_button_builder_rel_path))
    menu_button_combat_path = pygame.image.load(str(menu_button_combat_rel_path))
    menu_button_guide_path = pygame.image.load(str(menu_button_guide_rel_path))
    menu_button_quit_path = pygame.image.load(str(menu_button_quit_rel_path))

    # PyGame variables builder menu
    builder_bg_rel_path = os.path.join(dir_py, 'images/builder_bg.png')
    builder_bg_path = pygame.image.load(str(builder_bg_rel_path))

    # PyGame music
    song_rel_path = os.path.join(dir_py, 'music/song_' + str(random.randint(1,5)) + '.mp3')
    pygame.mixer.music.load(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.queue(song_rel_path)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play()

    # Game logic variables
    game_state: int = 1

   # Bucle principal
    while True:

      # 1.- Debúxase a pantalla
        if game_state == 0:
            screen.fill((253, 253, 253))
            screen.blit(menu_bg_path, [0, 0])
            screen.blit(menu_button_builder_path, [731, 117])
            screen.blit(menu_button_combat_path, [731, 248])
            screen.blit(menu_button_guide_path, [731, 379])
            screen.blit(menu_button_quit_path, [731, 510])
            author_text = author_text_font.render("Héctor Álvarez Fernández, CDAV UDC, 2020", True, (128,128,128))
            screen.blit(author_text, [970, 743])

        if game_state == 1: 
            screen.fill((253, 253, 253))
            screen.blit(builder_bg_path, [0, 0])

      # 2.- Compróbanse os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

      # 3.- Actualízase a pantalla
        pygame.display.update()
    

if __name__ == '__main__':
   main()