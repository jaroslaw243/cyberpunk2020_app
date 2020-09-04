import random


class Character:
    def __init__(self, hplost, BC, dodgebase, armorhead, armortorso, armorlefthand, armorrighthand, armorleftleg,
                 armorrightleg, hard_armor):
        self.hplost = hplost
        self.BC = BC
        self.dodgebase = dodgebase
        self.armorhead = armorhead
        self.armortorso = armortorso
        self.armorlefthand = armorlefthand
        self.armorrighthand = armorrighthand
        self.armorleftleg = armorleftleg
        self.armorrightleg = armorrightleg
        self.hard_armor = hard_armor
        self.armor_protection = None
        self.hit_location = None
        self.damage = None

    def stun_check(self):
        stun_safe_value = self.BC - (int((self.hplost / 4) - 0.001))
        if stun_safe_value >= random.randint(1, 10):
            return True
        else:
            return False

    def life_check(self):
        life_safe_value = self.BC - (int((self.hplost / 4) - 3.001))
        if life_safe_value >= random.randint(1, 10):
            return True
        else:
            return False

    def bc_to_mbc(self):
        mbc = (0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 5)
        if 0 < self.BC <= 11:
            return -mbc[self.BC - 1]
        else:
            return -5

    def full_auto_damage(self, number_of_hits_func, weapon_damage_func, weapon_damage_bonus_func, damage_table_func):
        damage_func = 0

        for i in range(0, number_of_hits_func):
            damage_func += damage_table_func[self.hns_damage(weapon_damage_bonus_func)][weapon_damage_func - 1]

        self.damage = damage_func

    def damage_dealt_full_auto(self, number_of_hits_func):
        if self.hit_location == 'head':
            damage_dealt_full_auto = ((self.damage - (self.armor_protection * number_of_hits_func)) * 4) + (
                                       self.bc_to_mbc() * number_of_hits_func)
        else:
            damage_dealt_full_auto = ((self.damage - (self.armor_protection * number_of_hits_func)) * 2) + (
                                       self.bc_to_mbc() * number_of_hits_func)

        if damage_dealt_full_auto < 0:
            damage_dealt_full_auto = 0

        self.hplost += damage_dealt_full_auto

    def damage_dealt_no_full_auto(self):
        if self.hit_location == 'head':
            damage_dealt = ((self.damage - self.armor_protection) * 4) + self.bc_to_mbc()
        else:
            damage_dealt = ((self.damage - self.armor_protection) * 2) + self.bc_to_mbc()

        if damage_dealt < 0:
            damage_dealt = 0

        self.hplost += damage_dealt

    def hns_armor_protection(self, armor_piercing):
        armor_to_armor_protection = (0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7,
                                     7, 7,
                                     7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 12, 12, 12,
                                     12, 12,
                                     12, 12, 12, 12, 12, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 16, 16, 16, 16, 16, 16,
                                     16, 16,
                                     16, 16, 18)
        armor_of_body_part = {'head': self.armorhead, 'torso': self.armortorso, 'left arm': self.armorlefthand,
                              'right arm': self.armorrighthand, 'left leg': self.armorleftleg,
                              'right leg': self.armorrightleg}
        armor = armor_of_body_part[self.hit_location]
        if armor > 80:
            armor = 80

        if not armor_piercing:
            self.armor_protection = armor_to_armor_protection[armor]
        else:
            if self.hard_armor:
                self.armor_protection = round(armor_to_armor_protection[armor] / 2)
            else:
                self.armor_protection = round(armor_to_armor_protection[armor] / 3)

    def random_hit_location(self):
        body_locations = ('head', 'torso', 'torso', 'torso', 'right arm', 'left arm', 'right leg', 'right leg',
                          'left leg', 'left leg')
        self.hit_location = body_locations[random.randint(0, 9)]

    @staticmethod
    def hns_damage(bonus_to_roll):
        damage_rolls = (0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7)
        total_roll = damage_rolls[random.randint(0, 14)] + bonus_to_roll
        if total_roll <= 7:
            return total_roll
        else:
            return 7


class Combat:
    def __init__(self, full_auto, monoblade, difficulty, hit, number_of_hits, rate_of_fire, aiming_at_body_location,
                 fumble, critical_hit):
        self.full_auto = full_auto
        self.monoblade = monoblade
        self.difficulty = difficulty
        self.hit = hit
        self.number_of_hits = number_of_hits
        self.rate_of_fire = rate_of_fire
        self.aiming_at_body_location = aiming_at_body_location
        self.fumble = fumble
        self.critical_hit = critical_hit

    @staticmethod
    def hns_difficulty(distance_to_target):
        try:
            if 0 <= distance_to_target <= 12:
                return 0
            elif 13 <= distance_to_target <= 25:
                return 1
            elif 26 <= distance_to_target <= 50:
                return 2
            elif 51 <= distance_to_target <= 100:
                return 3
            elif 101 <= distance_to_target <= 150:
                return 4
            elif 151 <= distance_to_target <= 400:
                return 5
            elif 401 <= distance_to_target <= 800:
                return 6
            elif 800 < distance_to_target:
                return 7
        except TypeError:
            return None

    def shot_parameters(self, weapon, distance, difficulty_table, dodgebase):

        if 1 <= weapon <= 11:

            if 1 <= weapon <= 8:
                try:
                    self.difficulty = difficulty_table[self.hns_difficulty(distance)][weapon - 1]
                except TypeError:
                    pass
            else:
                self.full_auto = False
                self.difficulty = dodgebase + random.randint(1, 10)

                if weapon == 11:
                    self.monoblade = True

    def hit_calc(self, base_to_hit_value):
        dice_hit = random.randint(1, 10)

        if dice_hit == 1:
            self.fumble = True
        elif dice_hit == 10:
            self.critical_hit = True

        if self.difficulty is None:
            self.hit = False

        elif self.difficulty <= (dice_hit + base_to_hit_value) and not self.full_auto:
            self.hit = True

        elif self.difficulty < (dice_hit + base_to_hit_value) and self.full_auto:
            self.hit = True
            self.number_of_hits = ((dice_hit + base_to_hit_value) - self.difficulty - 1)
            if self.rate_of_fire < self.number_of_hits:
                self.number_of_hits = self.rate_of_fire

        else:
            self.hit = False

    def modifiers(self, mod):
        rates_of_fire_list = (3, 5, 10, 20, 25, 30, 100)
        mod = round((mod % 1) * 100)
        if mod == 50:
            self.aiming_at_body_location = True
        if 11 <= mod <= 17:
            self.full_auto = True
            self.rate_of_fire = rates_of_fire_list[mod - 11]
