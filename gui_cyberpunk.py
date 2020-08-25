import tkinter as tk
import os.path
import npcs
from app_classes import Character, Combat

difficulty_table1 = ((10, 5, 10, 10, 5, 15, None, 15),
                     (15, 10, 15, 10, 5, 15, 10, 15),
                     (20, 15, 25, 10, 10, 10, 10, 15),
                     (25, 20, 30, 15, 10, 10, 10, 20),
                     (30, 25, None, 20, 20, 15, 10, 20),
                     (None, 30, None, 25, 25, 20, 15, 25),
                     (None, None, None, 30, None, 20, 15, 30),
                     (None, None, None, 30, None, 25, 20, 35))

damage_table1 = ((0, 1, 1, 2, 3, 4, 5, 6, 4, 6, 7, 8, 9, 11, 14, 16),
                 (0, 1, 1, 3, 4, 5, 6, 7, 5, 7, 8, 9, 10, 12, 16, 18),
                 (1, 1, 2, 4, 5, 6, 7, 8, 6, 8, 9, 10, 11, 14, 18, 20),
                 (1, 2, 3, 5, 6, 7, 8, 9, 7, 9, 10, 11, 12, 16, 20, 24),
                 (1, 2, 4, 6, 7, 8, 9, 10, 8, 10, 11, 12, 13, 18, 24, 28),
                 (2, 3, 5, 7, 8, 9, 10, 11, 9, 11, 12, 13, 14, 20, 28, 32),
                 (3, 4, 6, 8, 9, 9, 10, 11, 9, 11, 12, 13, 14, 20, 28, 32),
                 (4, 5, 7, 9, 10, 9, 10, 11, 9, 11, 12, 13, 14, 20, 28, 32))

fight = Combat(False, False, None, False, 0, 0, False)


def main(dist, base_t_h_v, bonus_damage, chosen_weapon_damage, chosen_weapon):
    global fight
    enemy_stats = npcs.all_npcs[enemy_stats_index.get() - 1]
    enemy = Character(0, enemy_stats['BC'], enemy_stats['dodgebase'], enemy_stats['armorhead'],
                      enemy_stats['armortorso'], enemy_stats['armorlefthand'], enemy_stats['armorrighthand'],
                      enemy_stats['armorleftleg'], enemy_stats['armorrightleg'], enemy_stats['hard_armor'])
    armor_of_body_part = {'head': enemy.armorhead, 'torso': enemy.armortorso, 'left arm': enemy.armorlefthand,
                          'right arm': enemy.armorrighthand, 'left leg': enemy.armorleftleg,
                          'right leg': enemy.armorrightleg}
    char_state_c = ''
    char_state_l = ''
    sum_mods = int(sum([mod1.get(), mod2.get(), mod3.get(), mod4.get(), mod5.get(), mod6.get(), mod7.get(), mod8.get(),
                        mod9.get(), mod10.get(), mod11.get(), mod12.get(), mod13.get(), mod14.get(), mod15.get(),
                        mod16.get(), mod17.get(), mod18.get(), mod19.get()]))
    fight.shot_parameters(chosen_weapon, enemy.hns_difficulty(dist), difficulty_table1, enemy.dodgebase)
    fight.hit_calc(base_t_h_v + sum_mods)
    if fight.hit:
        if not fight.full_auto:
            damage = damage_table1[enemy.hns_damage(bonus_damage)][chosen_weapon_damage - 1]
        else:
            damage = enemy.full_auto_damage(fight.number_of_hits, (chosen_weapon_damage - 1), bonus_damage,
                                            damage_table1)
        if not fight.aiming_at_body_location:
            hit_location = enemy.hit_location()
        else:
            popup_ch_bod_loc()
            root.wait_window(choose_hit_location)
            hit_location = hit_location_temp.get()

        armor_prot = enemy.hns_armor_protection(armor_of_body_part[hit_location], fight.monoblade, enemy.hard_armor)
        if not fight.full_auto:
            damage_dealt = enemy.damage_dealt_no_full_auto(hit_location, damage, armor_prot, enemy.bc_to_mbc())
        else:
            damage_dealt = enemy.damage_dealt_full_auto(hit_location, damage, armor_prot, enemy.bc_to_mbc(),
                                                        fight.number_of_hits)
        if damage_dealt < 0:
            damage_dealt = 0
        enemy.hplost += damage_dealt
        if enemy.life_check():
            if not enemy.stun_check():
                char_state_c = 'Character is stunned. \n'
            if hit_location == 'head' and damage_dealt >= 13:
                char_state_c = ''
                char_state_l = 'Character died.'
        else:
            char_state_l = 'Character died.'

        output[
            'text'] = f'Hit landed at {hit_location} and dealt {damage_dealt} damage. \n' + char_state_c + char_state_l
    else:
        output['text'] = 'Missed.'

    fight = Combat(False, False, None, False, 0, 0, False)


def get_value(entryWidget):
    value = entryWidget.get()
    try:
        return int(value)
    except ValueError:
        return 0


def popup_ch_bod_loc():
    global hit_location_temp, choose_hit_location
    hit_location_temp = tk.StringVar(value='head')
    choose_hit_location = tk.Toplevel()
    choose_hit_location.title('Choose body location')
    canvas_top = tk.Canvas(choose_hit_location, height=0, width=280)
    canvas_top.pack()

    BL1 = tk.Radiobutton(choose_hit_location, text="Head", variable=hit_location_temp, value='head')
    BL2 = tk.Radiobutton(choose_hit_location, text="Torso", variable=hit_location_temp, value='torso')
    BL3 = tk.Radiobutton(choose_hit_location, text="Left arm", variable=hit_location_temp, value='left arm')
    BL4 = tk.Radiobutton(choose_hit_location, text="Right arm", variable=hit_location_temp, value='right arm')
    BL5 = tk.Radiobutton(choose_hit_location, text="Left leg", variable=hit_location_temp, value='left leg')
    BL6 = tk.Radiobutton(choose_hit_location, text="Right leg", variable=hit_location_temp, value='right leg')

    BL1.pack(anchor='w')
    BL2.pack(anchor='w')
    BL3.pack(anchor='w')
    BL4.pack(anchor='w')
    BL5.pack(anchor='w')
    BL6.pack(anchor='w')


root = tk.Tk()

root.title('Cyberpunk 2020 High Noon Shootout App')
canvas = tk.Canvas(root, height=720, width=1280)
canvas.pack()

if os.path.isfile('./cyberpunk_background.png'):
    background_image = tk.PhotoImage(file='cyberpunk_background.png')
    background_label = tk.Label(root, image=background_image)
else:
    background_label = tk.Label(root, bg='#130012')

background_label.place(relwidth=1, relheight=1)

weapons_menu = tk.Frame(root, bg='#b50000')
weapons_menu.place(relx=0.025, rely=0.025, relwidth=0.322, relheight=0.415)
weapon_m_label = tk.Label(weapons_menu, text='1) Choose your weapon:', bg='#b50000')
weapon_m_label.pack(anchor='w')

mods_menu = tk.Frame(root, bg='#00a0d1')
mods_menu.place(relx=0.025, rely=0.475, relwidth=0.322, relheight=0.415)
mods_m_label = tk.Label(mods_menu, text='2) Choose your modifiers:', bg='#00a0d1')
mods_m_label.grid(column=0, row=0, sticky='w')

inputs_menu = tk.Frame(root, bg='#FF7700')
inputs_menu.place(relx=0.397, rely=0.475, relwidth=0.322, relheight=0.415)

w_dam_entry = tk.Frame(root, bg='#52b94c')
w_dam_entry.place(relx=0.397, rely=0.025, relwidth=0.25, relheight=0.415)
w_dam_label = tk.Label(w_dam_entry, text='3) Choose damage dealt by weapon:', bg='#52b94c')
w_dam_label.grid(sticky='w', column=0, row=0)

characters_menu = tk.Frame(root, bg='#F3ED73')
characters_menu.place(relx=0.697, rely=0.025, relwidth=0.278, relheight=0.415)
char_label = tk.Label(characters_menu, text='4) Choose character to fight:', bg='#F3ED73')
char_label.grid(sticky='w', column=0, row=0)

distance_label = tk.Label(inputs_menu, bg='#FF7700', text='Distance to target [m]')
distance_label.place(relx=0.04325, rely=0.025, relwidth=0.338, relheight=0.07)
bonus_damage_label = tk.Label(inputs_menu, bg='#FF7700', text='Bonus to weapon damage')
bonus_damage_label.place(relx=0.04325, rely=0.13, relwidth=0.338, relheight=0.07)
bthv_label = tk.Label(inputs_menu, bg='#FF7700', text='Base to hit value \n [REF + Att. skill + mods]')
bthv_label.place(relx=0.04325, rely=0.235, relwidth=0.338, relheight=0.1)

start_button = tk.Button(inputs_menu, text='Fight!', font=40, command=lambda: main(get_value(entry_distance),
                                                                                   get_value(base_t_h_v_entry),
                                                                                   get_value(bonus_damage_entry),
                                                                                   damage_choice.get(),
                                                                                   weapon_choice.get()))
start_button.place(relheight=0.2825, relwidth=0.28175, relx=0.675, rely=0.025)

output = tk.Label(inputs_menu, font=60)
output.place(relx=0.04325, rely=0.5, relwidth=0.9135, relheight=0.475)

entry_distance = tk.Entry(inputs_menu)
entry_distance.place(rely=0.025, relx=0.4, relheight=0.07, relwidth=0.23)

bonus_damage_entry = tk.Entry(inputs_menu)
bonus_damage_entry.place(rely=0.13, relx=0.4, relheight=0.07, relwidth=0.23)

base_t_h_v_entry = tk.Entry(inputs_menu)
base_t_h_v_entry.place(rely=0.235, relx=0.4, relheight=0.07, relwidth=0.23)

weapon_choice = tk.IntVar(value=1)
text_for_w_radiobutton = ("Handgun (also paintball guns, dart guns and tasers)", "SMG, Bow", "Shotgun", "Rifle, MG",
                          "Laser (also microwavers)", "Cannon (also grenade launchers and hand thrown grenades)",
                          "Missile (also mini-missiles)", "Rockets", "Brawling", "Melee weapon", "Monoblade")
for row_w in range(11):
    R = tk.Radiobutton(weapons_menu, text=text_for_w_radiobutton[row_w], variable=weapon_choice, value=row_w + 1,
                       bg='#b50000')
    R.pack(anchor='w')

enemy_stats_index = tk.IntVar(value=1)
for row_c in range(1, len(npcs.all_npcs) + 1):
    A = tk.Radiobutton(characters_menu, text=npcs.all_npcs[row_c - 1]['name'], variable=enemy_stats_index, value=row_c,
                       bg='#F3ED73')
    A.grid(sticky='w', column=0, row=row_c)

damage_choice = tk.IntVar(value=1)
text_for_d_radiobutton = ("1k6/3", "1k6/2", "1k6", "2k6", "3k6", "4k6", "5k6", "6k6", "3k10", "4k10", "5k10", "6k10",
                          "7k10", "8k10", "9k10", "More")
for row_d1 in range(8):
    D = tk.Radiobutton(w_dam_entry, text=text_for_d_radiobutton[row_d1], variable=damage_choice, value=row_d1 + 1,
                       bg='#52b94c')
    D.grid(sticky='w', column=0)

for row_d2 in range(8):
    D = tk.Radiobutton(w_dam_entry, text=text_for_d_radiobutton[row_d2 + 8], variable=damage_choice, value=row_d2 + 9,
                       bg='#52b94c')
    D.grid(sticky='w', column=1, row=row_d2 + 1)

mod1 = tk.IntVar()
mod2 = tk.IntVar()
mod3 = tk.IntVar()
mod4 = tk.IntVar()
mod5 = tk.DoubleVar()
mod6 = tk.IntVar()
mod7 = tk.IntVar()
mod8 = tk.IntVar()
mod9 = tk.IntVar()
mod10 = tk.IntVar()
mod11 = tk.DoubleVar()
mod12 = tk.DoubleVar()
mod13 = tk.DoubleVar()
mod14 = tk.DoubleVar()
mod15 = tk.DoubleVar()
mod16 = tk.DoubleVar()
mod17 = tk.DoubleVar()
mod18 = tk.IntVar()
mod19 = tk.IntVar()
C1 = tk.Checkbutton(mods_menu, text="Target Immobile (+2) ", variable=mod1, onvalue=2, bg='#00a0d1')
C2 = tk.Checkbutton(mods_menu, text="Target Dodging (-2)", variable=mod2, onvalue=-2, bg='#00a0d1')
C3 = tk.Checkbutton(mods_menu, text="Target Dodging, REF 10+ (-4)", variable=mod3, onvalue=-4, bg='#00a0d1')
C4 = tk.Checkbutton(mods_menu, text="Ambush (+2)", variable=mod4, onvalue=2, bg='#00a0d1')
C5 = tk.Checkbutton(mods_menu, text="Aiming at body location (-3)", variable=mod5, onvalue=-3.5, bg='#00a0d1',
                    command=lambda: fight.modifiers(mod5.get()))
C6 = tk.Checkbutton(mods_menu, text="Firing while running (-2) ", variable=mod6, onvalue=-2, bg='#00a0d1')
C7 = tk.Checkbutton(mods_menu, text="Firing while dodging (-4) ", variable=mod7, onvalue=-4, bg='#00a0d1')
C8 = tk.Checkbutton(mods_menu, text="Large target (+2)", variable=mod8, onvalue=2, bg='#00a0d1')
C9 = tk.Checkbutton(mods_menu, text="Small target (-2)", variable=mod9, onvalue=-2, bg='#00a0d1')
C10 = tk.Checkbutton(mods_menu, text="Tiny target (-4)", variable=mod10, onvalue=-4, bg='#00a0d1')
C11 = tk.Checkbutton(mods_menu, text="3-round burst (+1)", variable=mod11, onvalue=1.11, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod11.get()))
C12 = tk.Checkbutton(mods_menu, text="5-round burst (+2)", variable=mod12, onvalue=2.12, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod12.get()))
C13 = tk.Checkbutton(mods_menu, text="10-round burst (+3)", variable=mod13, onvalue=3.13, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod13.get()))
C14 = tk.Checkbutton(mods_menu, text="20-round burst (+4)", variable=mod14, onvalue=4.14, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod14.get()))
C15 = tk.Checkbutton(mods_menu, text="25-round burst (+5)", variable=mod15, onvalue=5.15, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod15.get()))
C16 = tk.Checkbutton(mods_menu, text="30-round burst (+6)", variable=mod16, onvalue=6.16, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod16.get()))
C17 = tk.Checkbutton(mods_menu, text="100-round burst (+15)", variable=mod17, onvalue=15.17, bg='#00a0d1',
                     command=lambda: fight.modifiers(mod17.get()))
C18 = tk.Checkbutton(mods_menu, text="Fast draw (-2)", variable=mod18, onvalue=-2, bg='#00a0d1')
C19 = tk.Checkbutton(mods_menu, text="Blinded/in the dark (-2)", variable=mod19, onvalue=-2, bg='#00a0d1')
C1.grid(column=0, row=1, sticky='w')
C2.grid(column=0, row=2, sticky='w')
C3.grid(column=0, row=3, sticky='w')
C4.grid(column=0, row=4, sticky='w')
C5.grid(column=0, row=5, sticky='w')
C6.grid(column=0, row=6, sticky='w')
C7.grid(column=0, row=7, sticky='w')
C8.grid(column=0, row=8, sticky='w')
C9.grid(column=0, row=9, sticky='w')
C10.grid(column=0, row=10, sticky='w')
C11.grid(column=1, row=1, sticky='w')
C12.grid(column=1, row=2, sticky='w')
C13.grid(column=1, row=3, sticky='w')
C14.grid(column=1, row=4, sticky='w')
C15.grid(column=1, row=5, sticky='w')
C16.grid(column=1, row=6, sticky='w')
C17.grid(column=1, row=7, sticky='w')
C18.grid(column=1, row=8, sticky='w')
C19.grid(column=1, row=9, sticky='w')

root.mainloop()
