import pygame
import json
import random


class Move():
    def __init__(self, move_id): 
        with open("data/movedex.json") as f_movedex:
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
        with open("data/pokedex.json") as f_pokedex:
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

def kill_team_user(team_user):                                # debugging purposes
    for i in range(len(team_user)):
        team_user[i].ko = True
    return team_user

def kill_team_foe(team_foe):                                # debugging purposes
    for i in range(len(team_foe)):           # debugging purposes
        team_foe[i].ko = True                # debugging purposes
    return team_foe

def battle_display(team_user, active_user, team_foe, active_foe):
    print('\nUser:')
    print(team_user[active_user].name)
    print(team_user[active_user].current_hp)
    print('\nFoe')
    print(team_foe[active_foe].name)
    print(team_foe[active_foe].current_hp)

def battle_menu_main(menu_choice):
    print("""
[1] Moves
[2] Team
[3] Exit
""")
    menu_choice = int(input())
    return menu_choice

def battle_menu_moves(team_user, active_user, team_foe, active_foe):
    print("""
[0] Back
[1] {}
[2] {}
[3] {}
[4] {}
""".format(team_user[active_user].moveset[0].name, team_user[active_user].moveset[1].name, team_user[active_user].moveset[2].name, team_user[active_user].moveset[3].name))
    menu_choice = int(input())-1
    return menu_choice

def battle_menu_team(team_user, active_user):
    list_pid = []
    print('\n[0] Back')
    for i in range(len(team_user)):
        if i != active_user:
            print('[' + str(i) + ']', team_user[i].name, team_user[i].p_id)
            list_pid.append(team_user[i].p_id)
    menu_choice = int(input())
    if menu_choice != 0:
        pokemon_choice = list_pid[menu_choice-1]
        return pokemon_choice
    else: return menu_choice

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
        return (1, 0)
    elif team_user[active_user].moveset[attack_user].priority > team_foe[active_foe].moveset[attack_foe].priority: 
        return (0, 1)
    elif team_user[active_user].moveset[attack_user].priority = team_foe[active_foe].moveset[attack_foe].priority: 
        if team_user[active_user].current_speed > team_foe[active_foe].current_speed: 
            return (0, 1)
        elif team_user[active_user].current_speed < team_foe[active_foe].current_speed: 
            return (1, 0)
        elif team_user[active_user].current_speed = team_foe[active_foe].current_speed: 
            random_number = random.randint(1, 6000)
            if random_number < 3001:
                return (1, 0)
            else: return (0, 1)

def Battle(chosen_pokemon):
    i = 0
    endCombat = False
    team_user = []
    team_foe = []
    active_user: int = 0
    active_foe: int = 0
    battle_status: int = 0  #0 menu, 1  moves, 2  team, 3  exit
    menu_choice: int = 0

    team_user = build_team_user(team_user, chosen_pokemon)
    team_foe = build_team_foe(team_foe, chosen_pokemon)

    while endCombat != True:
        if is_combat_possible(team_user, team_foe) == False:
            battle_status = 3
        if battle_status != 3: 
            battle_display(team_user, active_user, team_foe, active_foe)
            if battle_status == 0:
                menu_choice = battle_menu_main(menu_choice)
                battle_status = menu_choice
            elif battle_status == 1: 
                menu_choice = battle_menu_moves(team_user, active_user, team_foe, active_foe)
                battle_status = 0
                if menu_choice != -1:
                    Attacking_order(team_user, active_user, team_foe, active_foe, menu_choice)
            elif battle_status == 2: 
                menu_choice = battle_menu_team(team_user, active_user)
                battle_status = 0
                if menu_choice != 0:
                    i = 0
                    while i < len(team_user): 
                        if team_user[i].p_id == menu_choice: 
                            active_user = i
                            i = len(team_user)
                        else: 
                            i += 1
        else: endCombat = True
        
        # team_user = kill_team_user(team_user)
        # team_foe = kill_team_foe(team_foe)
            
Battle([3,6,9,150])