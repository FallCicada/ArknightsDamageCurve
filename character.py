import copy
import random
from math import ceil

cp = copy.deepcopy
random.seed(114514)

# Charge on defense: average charge speed (how much sp charged in 1 sec)
# Change this to set how much SP a charge-on-defense character could get per second
Charge_on_defense_equivalent_charge_speed = 0.75

# Hellague approximately has +36 attack speed at 75% HP
# Change this to set Hellague's HP ratio, thus change the attack speed of Hellague
Hellagur_talent_hp_ratio = 0.75

# Provence has 50% attack scale up when target is at 60% HP
# Change this to set Enemy's HP ratio for Provence(Wolf's Eye), thus change the damage of Provence
Provence_Wolfeye_target_hp_ratio = 0.6

# Enemy dict
# You can pick any enemy here. You can also add your own choice
enemy_dict = {
    "伐木老手": {
        "HP": 25000,
        "def": 100,
        "MR": 30,
        "img": "伐木老手.png",
        "rank": "Elite.png",
        "tag": ["3级血.png"]
    },
    "高阶术师组长": {
        "HP": 33750,
        "def": 160,
        "MR": 50,
        "img": "高阶术师组长.png",
        "rank": "Elite.png",
        "tag": ["3级血.png"]
    },
    "碎岩者组长": {
        "HP": 32500,
        "def": 100,
        "MR": 90,
        "img": "碎岩者组长.png",
        "rank": "Elite.png",
        "tag": ["3级血.png", "3级斧.png"]
    },
    "浮士德": {
        "HP": 50000,
        "def": 350,
        "MR": 35,
        "img": "浮士德.png",
        "rank": "Boss.png",
        "tag": []
    },
    "庞贝": {
        "HP": 50000,
        "def": 270,
        "MR": 70,
        "img": "庞贝.png",
        "rank": "Boss.png",
        "tag": []
    },
    "末路狂徒": {
        "HP": 32500,
        "def": 600,
        "MR": 0,
        "img": "末路狂徒.png",
        "rank": "Elite.png",
        "tag": ["3级血.png"]
    },
    "雪怪小队破冰者": {
        "HP": 40000,
        "def": 600,
        "MR": 20,
        "img": "雪怪小队破冰者.png",
        "rank": "Elite.png",
        "tag": ["2级血.png"]
    },
    "梅菲斯特": {
        "HP": 126000,
        "def": 500,
        "MR": 60,
        "img": "梅菲斯特.png",
        "rank": "Boss.png",
        "tag": []
    },
    "磐蟹": {
        "HP": 3000,
        "def": 500,
        "MR": 85,
        "img": "磐蟹.png",
        "rank": "",
        "tag": []
    },
    "倾轧者": {
        "HP": 25000,
        "def": 1000,
        "MR": 30,
        "img": "倾轧者.png",
        "rank": "Elite.png",
        "tag": []
    },
    "复仇者": {
        "HP": 39600,
        "def": 1035,
        "MR": 50,
        "img": "复仇者.png",
        "rank": "Elite.png",
        "tag": ["3级刀.png", "加防.png"]
    },
    "武装人员": {
        "HP": 30000,
        "def": 1050,
        "MR": 75,
        "img": "武装人员.png",
        "rank": "Elite.png",
        "tag": ["3级血.png", "加防.png"]
    },
    "重装五十夫长": {
        "HP": 37500,
        "def": 1200,
        "MR": 0,
        "img": "重装五十夫长.png",
        "rank": "Elite.png",
        "tag": ["3级血.png"]
    },
    "重装防御组长": {
        "HP": 25000,
        "def": 1500,
        "MR": 0,
        "img": "重装防御组长.png",
        "rank": "Elite.png",
        "tag": ["3级血.png", "加防.png"]
    },
    "粉碎攻坚组长": {
        "HP": 36000,
        "def": 2000,
        "MR": 0,
        "img": "粉碎攻坚组长.png",
        "rank": "Elite.png",
        "tag": ["2级血.png"]
    },
}

# Multi target -- Target num dict
target_num_dict = {
    "超小半径圆溅射": 1.2,  # 麦哲伦3
    "小半径圆溅射": 1.9,  # 白雪2
    "中半径圆溅射": 2.7,  # 普通群狙, 普通群法
    "大半径圆溅射": 3.2,  # 空爆1, 天火2
    "超大半径圆溅射": 3.6,  # 陨星1

    "0格打2": 1.3,  # 火神2, 格拉尼2
    "0格打3": 1.87,  # 坚雷2

    "1格打2": 1.4,  # 普通精一群卫, 星极2
    "1格打3": 2,  # 普通精二群卫
    "1格群攻": 2.7,  # 星熊3, 煌3-切割

    "2格打2": 1.5,  # 精一煌2
    "2格打3": 2.12,  # 精二煌2, 1~7级赫拉格3
    "2格打4": 2.52,  # 雷蛇2

    "3格打2": 1.55,  # 精一布洛卡2
    "3格打3": 2.21,  # 精二布洛卡2, 1~3级暴行2, 8~10级赫拉格3
    "3格打4": 2.51,  # 4~7级暴行2
    "3格打5": 2.82,  # 8~10级暴行2

    "4格打2": 1.6,  # 暗索2

    "5格群攻": 3.4,  # 精一伊芙利特

    "3格远卫打2": 1.65,  # 拉普兰德2、
    "3格远卫打4": 2.83,  # 1~3级陈2
    "3格远卫打5": 3.07,  # 4~6级陈2
    "3格远卫打6": 3.25,  # 7~9级陈2
    "3格远卫打7": 3.35,  # 10级陈2

    "3格扇形打3": 2.5,  # 1~3级银灰3
    "3格扇形打4": 2.95,  # 4~6级银灰3
    "3格扇形打5": 3.25,  # 7~9级银灰3
    "3格扇形打6": 3.52,  # 10级银灰3

    "1格菱形群攻": 3.1,  # 推进之王2

    "2格菱形群攻": 3.55,  # 德克萨斯2

    "3格菱形打3": 2.55,  # 1~3级艾雅法拉3
    "3格菱形打4": 3.05,  # 4~6级艾雅法拉3
    "3格菱形打5": 3.4,  # 7~9级艾雅法拉3
    "3格菱形打6": 3.75,  # 10级艾雅法拉3
    "3格菱形群攻": 4.15,  # 格劳克斯2

    "精一群法群攻": 3.52,  # 莫斯提马2, 煌3-爆裂

    "精零快狙打2": 3.52,  # 精零蓝毒1

    "精一快狙打2": 1.7,  # 蓝毒1, 红云2
    "精一快狙打3": 2.44,  # 蓝毒2
    "精一快狙打5": 3.2,  # 流星2
    "精一快狙群攻": 3.62,  # 远山2

    "精零群奶群攻": 3.45,  # 狮蝎, 伊桑

    "精一群奶打2": 1.68,  # 精零初雪1, 格劳克斯1

    "精一初雪打2": 1.85,  # 精二初雪

    "反重力打4": 3.05,  # 1~6级安洁莉娜3
    "反重力打5": 3.36,  # 7~10级安洁莉娜3

    "药物配置打2": 1.78,  # 4~10级真理2
    "药物配置打3": 2.55,  # 4~10级真理2

    "序时之匙群攻": 3.9,  # 莫斯提马3 (莫斯提马3额外减少0.2，因为容易把敌人推出去),

    "战术电台2发": 4.2,  # 1~7级守林人2
    "战术电台3发": 5.5,  # 8~10级守林人2

    "4格霰弹群攻": 3.22,  # 精零送葬人
    "6格霰弹群攻": 3.37,  # 精一送葬人
    "9格霰弹打3": 2.38,  # 崖心2
}


class StateData:
    def __init__(self, info_dict, dmg_type, is_skill_state=False):
        self.is_skill_state = is_skill_state

        # ---------- Required Info ----------
        self.dmg_type = dmg_type  # physical / magic / mix
        self.atk = info_dict.get("base_atk")
        self.atk_time = info_dict.get("atk_time")
        self.atk_up = info_dict.get("atk", 0)
        self.atk_scale = info_dict.get("atk_scale", 1.00)
        self.dmg_scale = info_dict.get("damage_scale", 1.00)
        self.atk_speed_up = info_dict.get("attack_speed", 0)

        self.atk_times = info_dict.get("atk_times", 1)
        self.equivalent_target_num = info_dict.get("atk_times", 1.0)

        self.enemy_defense_decrease_value = info_dict.get("def_value", 0)
        self.enemy_defense_decrease_ratio = info_dict.get("def_ratio", 0.0)
        self.enemy_magic_resistance_decrease_value = info_dict.get("mr_value", 0)
        self.enemy_magic_resistance_decrease_ratio = info_dict.get("mr_ratio", 0.0)

        # ---------- Special Info ----------
        self.atk_time_add_modifier = info_dict.get("base_attack_time_add", 0.00)
        self.atk_time_mul_modifier = info_dict.get("base_attack_time_mul", 0.00)
        self.penetration_ratio = info_dict.get("pene_ratio", 0.00)
        self.mix_physical_scale = info_dict.get("phy_scale", 0.00)
        self.mix_magic_scale = info_dict.get("mag_scale", 0.00)
        self.stun = info_dict.get("stun", 0.00)
        self.dot_damage_raw = info_dict.get("dot_dmg", 0)
        self.dot_time = info_dict.get("dot_time", 0)

        # ---------- Optional Info ----------
        self.def_up = 0
        self.maxHP_up = 0
        self.HP_recover_ratio = 0
        self.HP_recover_constant = 0

        # ---------- Temp ----------
        self.damage = -1
        self.frame = -1
        self.dot_damage = -1
        self.dot_frame = -1

    def real_dmg(self, defense, magic_resistance):
        real_atk = self.atk * (1 + self.atk_up) * self.atk_scale
        if self.dmg_type == "physical":
            enemy_def = (defense + self.enemy_defense_decrease_value) * (1 + self.enemy_defense_decrease_ratio)
            if enemy_def < 0:
                enemy_def = 0
            if real_atk - enemy_def * (1 - self.penetration_ratio) >= 0.05 * real_atk:
                return (real_atk - enemy_def * (1 - self.penetration_ratio)) * self.dmg_scale
            else:
                return real_atk * 0.05 * self.dmg_scale
        elif self.dmg_type == "magic":
            enemy_mr = (magic_resistance + self.enemy_magic_resistance_decrease_value) * (
                    1 + self.enemy_magic_resistance_decrease_ratio)
            if enemy_mr > 95:
                enemy_mr = 95
            return real_atk * (100 - enemy_mr) / 100 * self.dmg_scale
        elif self.dmg_type == "mix":
            enemy_def = (defense + self.enemy_defense_decrease_value) * (1 + self.enemy_defense_decrease_ratio)
            if real_atk - enemy_def * (1 - self.penetration_ratio) >= 0.05 * real_atk:
                physical_part = (real_atk - enemy_def * (1 - self.penetration_ratio)) * self.dmg_scale
            else:
                physical_part = real_atk * 0.05 * self.dmg_scale
            enemy_mr = (magic_resistance + self.enemy_magic_resistance_decrease_value) * (
                    1 + self.enemy_magic_resistance_decrease_ratio)
            if enemy_mr > 95:
                enemy_mr = 95
            magic_part = real_atk * (100 - enemy_mr) / 100 * self.dmg_scale
            return physical_part + magic_part

    def real_atk_frame(self):
        if self.atk_speed_up < -90:
            self.atk_speed_up = -90
        elif self.atk_speed_up > 500:
            self.atk_speed_up = 500
        real_atk_interval = (self.atk_time + self.atk_time_add_modifier) * (1 + self.atk_time_mul_modifier)
        real_atk_time = real_atk_interval * 100 / (100 + self.atk_speed_up)
        return ceil(real_atk_time * 30)

    def save_temp(self, defense, magic_resistance):
        if self.damage <= 0:
            self.damage = self.real_dmg(defense, magic_resistance)
        if self.frame <= 0:
            self.frame = self.real_atk_frame()
        if magic_resistance <= 95:
            self.dot_damage = self.dot_damage_raw * self.atk_scale * (100 - magic_resistance) / 100 * self.dmg_scale
        else:
            self.dot_damage = self.dot_damage_raw * self.atk_scale * 0.05 * self.dmg_scale
        self.dot_frame = ceil(self.dot_time * 30)
        # print("\tAttack: %-4d, Attack buff: %-3.0f%%, Attack Scale: %-3.0f%%, Damage buff: %-3.0f%% ;"
        #       % (self.atk, self.atk_up * 100, self.atk_scale * 100, self.dmg_scale * 100))
        # print("\tDamage per attack: %-7.1f" % self.damage, end="; ")
        # print("Attack interval in frame: %-3d" % self.frame, end="; ")
        # print("DPS: %-7.1f" % (self.damage / self.frame * 30), end="; ")
        # print()


class CharacterData:
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        self.name = name
        self.skill_order = skill_order
        self.rarity = basic_info_dict.get("rarity")
        self.normal_damage_type = basic_info_dict.get("normal_damage_type", "physical")
        self.skill_damage_type = basic_info_dict.get("skill_damage_type", "physical")
        self.skill_type = basic_info_dict.get("skill_type", "lasting")  # lasting / instant / passive / onDeploy
        self.sp_type = basic_info_dict.get("sp_type", "auto")  # auto / attack / defense
        self.sp_cost = basic_info_dict.get("sp_cost")
        self.init_sp = basic_info_dict.get("init_sp", 0)
        self.sp_recovery = basic_info_dict.get("sp_recovery", 0.0) + 1.0
        self.skill_duration = basic_info_dict.get("duration")
        self.sp_recovery_block_time = basic_info_dict.get("block", self.skill_duration)
        self.skill_reset_cooldown_flag = basic_info_dict.get("reset", True)

        self.NormalData = StateData(info_dict=normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.SkillData = StateData(info_dict=skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.multi_target_desc = "单体攻击"

    def replace_basic_attack(self):
        # This method is for skill replacing normal attack, like 强力击, 飞羽(灰喉1技能), and 药物配置(塞雷娅2技能), etc.
        self.skill_reset_cooldown_flag = False
        self.skill_duration = self.NormalData.atk_time + 1 / 30
        self.sp_recovery_block_time = self.NormalData.atk_time + 1 / 30

    def release_on_deploy(self, duration):
        # This method is for skill only effective in several seconds after deployment, like 跃浪击 and 处决模式, etc.
        self.skill_duration = duration
        self.sp_cost = 9999
        self.init_sp = 9999

    def infinite_skill_duration(self):
        # This method is for skill which once released, it will last forever, like 天马视域 and 链锯延伸模块, etc.
        self.skill_duration = 9999
        self.sp_recovery_block_time = 9999

    def passive_skill(self):
        # This method is for passive skills, like 蝎毒, etc.
        self.init_sp = 9999
        self.sp_cost = 9999
        self.skill_duration = 9999
        self.sp_recovery_block_time = 9999

    def replace_charge_on_defense(self, sp):
        # This method is for skill charging on defense, like 反击电弧 and 舍身突击(艾斯黛尔2技能), etc.
        self.sp_type = "auto"
        self.sp_recovery = sp

    def magic_damage(self):
        # This method is for character with magic damage.
        self.normal_damage_type = "magic"
        self.skill_damage_type = "magic"
        self.NormalData.dmg_type = "magic"
        self.SkillData.dmg_type = "magic"

    def generate_multi_target_desc(self):
        # This method is to generate text description for character with multiple attack target.
        NETN = self.NormalData.equivalent_target_num
        SETN = self.SkillData.equivalent_target_num
        if NETN != 1 and SETN != 1:
            if NETN == SETN:
                self.multi_target_desc = "打%s" % NETN
            else:
                self.multi_target_desc = "普攻打%s,技能打%s" % (NETN, SETN)
        elif NETN != 1:
            self.multi_target_desc = "普攻打%s" % NETN
        elif SETN != 1:
            self.multi_target_desc = "技能打%s" % SETN

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class ArmorBreaker(CharacterData):
    """
    For characters with armor-breaking effect, i.e. decrease enemy target's defense in a period.

        -`normal_break_flag`: Only normal attack decrease enemy def
        -`skill_break_flag`: Only skill attack decrease enemy def
        -`both_break_flag`: Both normal and skill attack decrease enemy def
    """

    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.BrokenNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.BrokenSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.enemy_def_decrease_ratio = 0
        self.enemy_def_decrease_value = 0
        self.enemy_def_decrease_duration = 0
        self.normal_break_flag = False
        self.skill_break_flag = False
        self.both_break_flag = False

    def simulate(self, defense, magic_resistance):
        self.BrokenNormalData.enemy_defense_decrease_ratio = self.enemy_def_decrease_ratio
        self.BrokenNormalData.enemy_defense_decrease_value = self.enemy_def_decrease_value
        self.BrokenSkillData.enemy_magic_resistance_decrease_ratio = self.enemy_def_decrease_ratio
        self.BrokenSkillData.enemy_magic_resistance_decrease_value = self.enemy_def_decrease_value
        damage_node = list()
        N = self.NormalData
        BN = self.BrokenNormalData
        S = self.SkillData
        BS = self.BrokenSkillData
        N.save_temp(defense, magic_resistance)
        BN.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        BS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        def_decrease_remain = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            def_decrease_remain -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    if self.skill_break_flag or self.both_break_flag:
                        def_decrease_remain = self.enemy_def_decrease_duration
                    if def_decrease_remain <= 0:
                        damage += S.damage * S.atk_times * S.equivalent_target_num
                        atk_cooldown = S.frame
                        if S.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = S.dot_frame
                            else:
                                dot_dmg = S.dot_damage
                                dot_remain = S.dot_frame
                    else:
                        damage += BS.damage * BS.atk_times * BS.equivalent_target_num
                        atk_cooldown = BS.frame
                        if BS.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = BS.dot_frame
                            else:
                                dot_dmg = BS.dot_damage
                                dot_remain = BS.dot_frame
                else:
                    if self.normal_break_flag or self.both_break_flag:
                        def_decrease_remain = self.enemy_def_decrease_duration
                    if def_decrease_remain <= 0:
                        damage += N.damage * N.atk_times * N.equivalent_target_num
                        atk_cooldown = N.frame
                        if N.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = N.dot_frame
                            else:
                                dot_dmg = N.dot_damage
                                dot_remain = N.dot_frame
                    else:
                        damage += BN.damage * BN.atk_times * BN.equivalent_target_num
                        atk_cooldown = BN.frame
                        if BN.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = BN.dot_frame
                            else:
                                dot_dmg = BN.dot_damage
                                dot_remain = BN.dot_frame

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class TalentAtkBuff(CharacterData):
    """
    For characters with probably triggered effect when attacking.

        -`normal_trig_prob`: Probability of triggering talent effect in normal state
        -`skill_trig_prob`: Probability of triggering talent effect in skill state
    """

    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.TalentNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.normal_trig_prob = 0
        self.skill_trig_prob = 0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N, TN = self.NormalData, self.TalentNormalData
        S, TS = self.SkillData, self.TalentSkillData
        N.save_temp(defense, magic_resistance)
        TN.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        TS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num * (1 - self.skill_trig_prob) + \
                              TS.damage * TS.atk_times * TS.equivalent_target_num * self.skill_trig_prob
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num * (1 - self.skill_trig_prob) + \
                              TN.damage * TN.atk_times * TN.equivalent_target_num * self.skill_trig_prob
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30
                damage_node.append((frame / 30, damage))

        return damage_node


class Astesia(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.atk_speed_up_per_stage = 0
        self.atk_speed_up_interval = 0
        self.maximum_stage = 0

    def simulate(self, defense, magic_resistance):
        atk_spd_interval = self.atk_speed_up_interval * 30
        atk_spd_cnt = 0

        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            atk_spd_interval -= 1
            if atk_spd_interval <= 0 and atk_spd_cnt < self.maximum_stage:
                atk_spd_interval = self.atk_speed_up_interval * 30
                atk_spd_cnt += 1
                N.atk_speed_up += self.atk_speed_up_per_stage
                N.frame = N.real_atk_frame()
                S.atk_speed_up += self.atk_speed_up_per_stage
                S.frame = S.real_atk_frame()

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Blaze(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.skill_gradual_atk = 0
        self.skill_final_atk_scale = 0
        self.skill_gradual_target_num = 1.0
        self.skill_final_target_num = 1.0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                S.atk_scale = self.skill_final_atk_scale
                S.damage = S.real_dmg(defense, magic_resistance)
                damage += S.damage * S.atk_times * self.skill_final_target_num
                skill = False
                S.atk_scale = 1.0
                S.atk_up = 0.0
                S.damage = S.real_dmg(defense, magic_resistance)
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    if self.skill_order == "3":
                        S.atk_up += self.skill_gradual_atk / 9
                        S.damage = S.real_dmg(defense, magic_resistance)
                        damage += S.damage * S.atk_times * self.skill_gradual_target_num
                        atk_cooldown = S.frame
                        if S.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = S.dot_frame
                            else:
                                dot_dmg = S.dot_damage
                                dot_remain = S.dot_frame
                    else:
                        damage += S.damage * S.atk_times * S.equivalent_target_num
                        atk_cooldown = S.frame
                        if S.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = S.dot_frame
                            else:
                                dot_dmg = S.dot_damage
                                dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_dmg == 0:
                            dot_dmg = N.dot_damage
                            dot_interval = 0
                        dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Chen(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.sp_recovery_per_round = 0
        self.sp_recovery_interval = 0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        charge_interval = self.sp_recovery_interval * 30

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if charge_interval <= 0:
                if sp_recovery_block <= 0:
                    charge_interval = self.sp_recovery_interval * 30
                    curr_sp += self.sp_recovery_per_round * 30

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Haze(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.TalentNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.mr_reduction_ratio = 0
        self.mr_reduction_duration = 0

    def simulate(self, defense, magic_resistance):
        self.TalentNormalData.enemy_magic_resistance_decrease_ratio = self.mr_reduction_ratio
        self.TalentSkillData.enemy_magic_resistance_decrease_ratio = self.mr_reduction_ratio
        damage_node = list()
        N = self.NormalData
        TN = self.TalentNormalData
        S = self.SkillData
        TS = self.TalentSkillData
        N.save_temp(defense, magic_resistance)
        TN.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        TS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        mr_reduction = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            mr_reduction -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                mr_reduction = self.mr_reduction_duration
                if skill:
                    if mr_reduction <= 0:
                        damage += S.damage * S.atk_times * S.equivalent_target_num
                        atk_cooldown = S.frame
                        if S.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = S.dot_frame
                            else:
                                dot_dmg = S.dot_damage
                                dot_remain = S.dot_frame
                    else:
                        damage += TS.damage * TS.atk_times * TS.equivalent_target_num
                        atk_cooldown = TS.frame
                        if TS.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = TS.dot_frame
                            else:
                                dot_dmg = TS.dot_damage
                                dot_remain = TS.dot_frame
                else:
                    if mr_reduction <= 0:
                        damage += N.damage * N.atk_times * N.equivalent_target_num
                        atk_cooldown = N.frame
                        if N.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = N.dot_frame
                            else:
                                dot_dmg = N.dot_damage
                                dot_remain = N.dot_frame
                    else:
                        damage += TN.damage * TN.atk_times * TN.equivalent_target_num
                        atk_cooldown = TN.frame
                        if TN.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = TN.dot_frame
                            else:
                                dot_dmg = TN.dot_damage
                                dot_remain = TN.dot_frame

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Amiya(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.sp_recovery_by_atk = 0
        self.sp_recovery_by_kill = 0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if sp_recovery_block <= 0:
                    curr_sp += self.sp_recovery_by_atk * 30
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Eyjafjalla(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.TalentNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.SecondSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.mr_reduction_ratio = 0
        self.mr_reduction_duration = 0
        self.init_sp_gain = 0
        self.skill_release_cnt = 0
        self.multi_target_num = 1.0

    def simulate(self, defense, magic_resistance):
        self.TalentNormalData.enemy_magic_resistance_decrease_ratio = self.mr_reduction_ratio
        self.TalentSkillData.enemy_magic_resistance_decrease_ratio = self.mr_reduction_ratio
        damage_node = list()
        N = self.NormalData
        TN = self.TalentNormalData
        S = self.SkillData
        TS = self.TalentSkillData
        SS = self.SecondSkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        if self.skill_order == "1":
            SS.save_temp(defense, magic_resistance)
        elif self.skill_order == "2":
            TN.save_temp(defense, magic_resistance)
            TS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        curr_sp += self.init_sp_gain * 30
        sp_cost = self.sp_cost * 30
        self.skill_release_cnt = 0

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        mr_reduction = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            mr_reduction -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                self.skill_release_cnt += 1
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    if self.skill_order == "2":
                        mr_reduction = self.mr_reduction_duration
                    if self.skill_order == "1" and self.skill_release_cnt >= 2:
                        damage += SS.damage * SS.atk_times * SS.equivalent_target_num
                        atk_cooldown = SS.frame
                        if SS.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = SS.dot_frame
                            else:
                                dot_dmg = SS.dot_damage
                                dot_remain = SS.dot_frame
                    else:
                        if mr_reduction <= 0:
                            damage += S.damage * S.atk_times * S.equivalent_target_num
                            atk_cooldown = S.frame
                            if S.dot_damage > 0:
                                if dot_remain > 0:
                                    dot_remain = S.dot_frame
                                else:
                                    dot_dmg = S.dot_damage
                                    dot_remain = S.dot_frame
                        else:
                            damage += TS.damage * TS.atk_times * TS.equivalent_target_num + \
                                      S.damage * S.atk_times * (self.multi_target_num - 1)
                            atk_cooldown = TS.frame
                            if TS.dot_damage > 0:
                                if dot_remain > 0:
                                    dot_remain = TS.dot_frame
                                else:
                                    dot_dmg = TS.dot_damage
                                    dot_remain = TS.dot_frame
                else:
                    if mr_reduction <= 0:
                        damage += N.damage * N.atk_times * N.equivalent_target_num
                        atk_cooldown = N.frame
                        if N.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = N.dot_frame
                            else:
                                dot_dmg = N.dot_damage
                                dot_remain = N.dot_frame
                    else:
                        damage += TN.damage * TN.atk_times * TN.equivalent_target_num
                        atk_cooldown = TN.frame
                        if TN.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = TN.dot_frame
                            else:
                                dot_dmg = TN.dot_damage
                                dot_remain = TN.dot_frame

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Ifrit(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.mr_reduction_ratio = 0
        self.sp_recovery_per_round = 0
        self.sp_recovery_interval = 0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        charge_interval = self.sp_recovery_interval * 30

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if charge_interval <= 0:
                if sp_recovery_block <= 0:
                    charge_interval = self.sp_recovery_interval * 30
                    curr_sp += self.sp_recovery_per_round * 30

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class BluePoison(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.other_target_dot_raw = 0
        self.other_target_dot_atk_scale = 1.0
        self.other_target_dot_damage_scale = 1.0
        self.other_target_num = 0
        self.other_target_dot_duration = 0
        self.other_target_dot_damage = 0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        self.other_target_dot_damage = self.other_target_dot_raw * self.other_target_dot_atk_scale * \
                                       (100 - magic_resistance) / 100 * self.other_target_dot_damage_scale

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        oth_dot_remain = 0
        oth_dot_interval = 0
        oth_dot_dmg = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if oth_dot_dmg > 0 and oth_dot_remain > 0:
                oth_dot_remain -= 1
                oth_dot_interval -= 1
                if oth_dot_interval <= 0:
                    damage += oth_dot_dmg * self.other_target_num
                    damage_node.append((frame / 30, damage))
                    oth_dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                    if self.other_target_dot_damage > 0:
                        if oth_dot_remain > 0:
                            oth_dot_remain = ceil(self.other_target_dot_duration * 30)
                        else:
                            oth_dot_dmg = self.other_target_dot_damage
                            oth_dot_remain = ceil(self.other_target_dot_duration * 30)
                else:
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Platinum(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.min_atk_scale = 1.0
        self.max_atk_scale = 1.0
        self.min_atk_interval = 0
        self.max_atk_interval = 0

    def calc_atk_scale_modifier(self, atk_interval_frame, minAI, maxAI, minAS, maxAS):
        minAF = ceil(minAI * 30)
        maxAF = ceil(maxAI * 30)
        if atk_interval_frame <= minAF:
            return minAS
        elif atk_interval_frame >= maxAF:
            return maxAS
        else:
            return ((atk_interval_frame - minAF) * maxAS + (maxAF - atk_interval_frame) * minAS) / (maxAF - minAF)

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N = self.NormalData
        S = self.SkillData
        N.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        atk_interval_frame = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            atk_interval_frame += 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                atk_scale_modifier = self.calc_atk_scale_modifier(atk_interval_frame, self.min_atk_interval,
                                                                  self.max_atk_interval, self.min_atk_scale,
                                                                  self.max_atk_scale)
                if skill:
                    S.atk_scale = atk_scale_modifier
                    S.damage = S.real_dmg(defense, magic_resistance)
                    damage += S.damage * S.atk_times * S.equivalent_target_num
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    N.atk_scale = atk_scale_modifier
                    N.damage = N.real_dmg(defense, magic_resistance)
                    damage += N.damage * N.atk_times * N.equivalent_target_num
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame
                atk_interval_frame = 0

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Meteorite(ArmorBreaker):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        ArmorBreaker.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.atk_up_prob = 0
        self.atk_up_ratio = 0.0

    def simulate(self, defense, magic_resistance):
        self.BrokenNormalData.enemy_defense_decrease_ratio = self.enemy_def_decrease_ratio
        self.BrokenNormalData.enemy_defense_decrease_value = self.enemy_def_decrease_value
        self.BrokenSkillData.enemy_magic_resistance_decrease_ratio = self.enemy_def_decrease_ratio
        self.BrokenSkillData.enemy_magic_resistance_decrease_value = self.enemy_def_decrease_value
        damage_node = list()
        N = self.NormalData
        BN = self.BrokenNormalData
        S = self.SkillData
        BS = self.BrokenSkillData
        N.save_temp(defense, magic_resistance)
        BN.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        BS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        def_decrease_remain = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            def_decrease_remain -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    if self.skill_break_flag or self.both_break_flag:
                        def_decrease_remain = self.enemy_def_decrease_duration
                    if def_decrease_remain <= 0:
                        damage_no_atkup = S.real_dmg(defense, magic_resistance)
                        S.atk_up += self.atk_up_ratio
                        damage_atkup = S.real_dmg(defense, magic_resistance)
                        S.atk_up -= self.atk_up_ratio
                        S.damage = damage_no_atkup * (1 - self.atk_up_prob) + damage_atkup * self.atk_up_prob
                        damage += S.damage * S.atk_times * S.equivalent_target_num
                        atk_cooldown = S.frame
                        if S.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = S.dot_frame
                            else:
                                dot_dmg = S.dot_damage
                                dot_remain = S.dot_frame
                    else:
                        damage_no_atkup = BS.real_dmg(defense, magic_resistance)
                        BS.atk_up += self.atk_up_ratio
                        damage_atkup = BS.real_dmg(defense, magic_resistance)
                        BS.atk_up -= self.atk_up_ratio
                        BS.damage = damage_no_atkup * (1 - self.atk_up_prob) + damage_atkup * self.atk_up_prob
                        damage += BS.damage * BS.atk_times * BS.equivalent_target_num
                        atk_cooldown = BS.frame
                        if BS.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = BS.dot_frame
                            else:
                                dot_dmg = BS.dot_damage
                                dot_remain = BS.dot_frame
                else:
                    if self.normal_break_flag or self.both_break_flag:
                        def_decrease_remain = self.enemy_def_decrease_duration
                    if def_decrease_remain <= 0:
                        damage_no_atkup = N.real_dmg(defense, magic_resistance)
                        N.atk_up += self.atk_up_ratio
                        damage_atkup = N.real_dmg(defense, magic_resistance)
                        N.atk_up -= self.atk_up_ratio
                        N.damage = damage_no_atkup * (1 - self.atk_up_prob) + damage_atkup * self.atk_up_prob
                        damage += N.damage * N.atk_times * N.equivalent_target_num
                        atk_cooldown = N.frame
                        if N.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = N.dot_frame
                            else:
                                dot_dmg = N.dot_damage
                                dot_remain = N.dot_frame
                    else:
                        damage_no_atkup = BN.real_dmg(defense, magic_resistance)
                        BN.atk_up += self.atk_up_ratio
                        damage_atkup = BN.real_dmg(defense, magic_resistance)
                        BN.atk_up -= self.atk_up_ratio
                        BN.damage = damage_no_atkup * (1 - self.atk_up_prob) + damage_atkup * self.atk_up_prob
                        damage += BN.damage * BN.atk_times * BN.equivalent_target_num
                        atk_cooldown = BN.frame
                        if BN.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = BN.dot_frame
                            else:
                                dot_dmg = BN.dot_damage
                                dot_remain = BN.dot_frame

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Provence(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.TalentNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.talent_atk_scale = 0
        self.talent_prob = 0

    def simulate(self, defense, magic_resistance):
        self.TalentNormalData.atk_scale *= self.talent_atk_scale
        self.TalentSkillData.atk_scale *= self.talent_atk_scale
        damage_node = list()
        N = self.NormalData
        TN = self.TalentNormalData
        S = self.SkillData
        TS = self.TalentSkillData
        N.save_temp(defense, magic_resistance)
        TN.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        TS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        mr_reduction = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            mr_reduction -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    damage += (S.damage * S.atk_times * S.equivalent_target_num * (1 - self.talent_prob) +
                               TS.damage * TS.atk_times * TS.equivalent_target_num * self.talent_prob)
                    atk_cooldown = S.frame
                    if S.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = S.dot_frame
                        else:
                            dot_dmg = S.dot_damage
                            dot_remain = S.dot_frame
                else:
                    damage += (N.damage * N.atk_times * N.equivalent_target_num * (1 - self.talent_prob) +
                               TN.damage * TN.atk_times * TN.equivalent_target_num * self.talent_prob)
                    atk_cooldown = N.frame
                    if N.dot_damage > 0:
                        if dot_remain > 0:
                            dot_remain = N.dot_frame
                        else:
                            dot_dmg = N.dot_damage
                            dot_remain = N.dot_frame

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Schwarz(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.TalentNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.BreakNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.BreakSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.TalentBreakNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentBreakSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.talent_atk_scale = 1.0
        self.enemy_def_decrease_ratio = 0
        self.enemy_def_decrease_duration = 0
        self.talent_prob = 0
        self.skill_talent_prob = 0
        self.atk_type_dict = dict()

    def get_state_propotion_by_simulation(self, simulation_times=1000):
        state_list = [self.NormalData, self.TalentNormalData, self.BreakNormalData, self.TalentNormalData,
                      self.SkillData, self.TalentSkillData, self.BreakSkillData, self.TalentSkillData]
        frame_list = map(lambda x: x.real_atk_frame(), state_list)
        N, TN, BN, TBN, S, TS, BS, TBS = frame_list
        type_dict = {
            "normal_no_break_no_talent": 0,
            "skill_no_break_no_talent": 0,
            "normal_break_no_talent": 0,
            "skill_break_no_talent": 0,
            "normal_break_talent": 0,
            "skill_break_talent": 0,
        }
        skill_atk_cnt = 0
        normal_atk_cnt = 0
        for i in range(simulation_times):
            curr_sp = self.init_sp * 30
            sp_cost = self.sp_cost * 30
            atk_cooldown = 0
            skill_remain = 0
            sp_recovery_block = 0
            frame = 0
            skill = False
            def_decrease_remain = 0

            while frame < 300 * 30:
                frame += 1
                atk_cooldown -= 1
                skill_remain -= 1
                sp_recovery_block -= 1
                def_decrease_remain -= 1

                if sp_recovery_block <= 0 and self.sp_type == "auto":
                    curr_sp += self.sp_recovery
                if skill_remain < 0 and skill:
                    skill = False
                    if self.skill_reset_cooldown_flag:
                        atk_cooldown = 5
                if curr_sp >= sp_cost:
                    skill_remain = self.skill_duration * 30
                    skill = True
                    sp_recovery_block = self.sp_recovery_block_time * 30
                    curr_sp = 0.0
                    if self.skill_reset_cooldown_flag:
                        atk_cooldown = 5

                if atk_cooldown <= 0:
                    roll = random.random()
                    if skill:
                        skill_atk_cnt += 1
                        atk_cooldown = S
                        if roll < self.skill_talent_prob:
                            type_dict["skill_break_talent"] += 1
                            def_decrease_remain = self.enemy_def_decrease_duration
                        else:
                            if def_decrease_remain > 0:
                                type_dict["skill_break_no_talent"] += 1
                            else:
                                type_dict["skill_no_break_no_talent"] += 1
                    else:
                        normal_atk_cnt += 1
                        atk_cooldown = N
                        if roll < self.talent_prob:
                            type_dict["normal_break_talent"] += 1
                            def_decrease_remain = self.enemy_def_decrease_duration
                        else:
                            if def_decrease_remain > 0:
                                type_dict["normal_break_no_talent"] += 1
                            else:
                                type_dict["normal_no_break_no_talent"] += 1
                    if sp_recovery_block <= 0 and self.sp_type == "attack":
                        curr_sp += 30

        # print(self.talent_prob, self.skill_talent_prob, simulation_times)
        type_dict["normal_no_break_no_talent"] /= normal_atk_cnt
        type_dict["normal_break_no_talent"] /= normal_atk_cnt
        type_dict["normal_break_talent"] /= normal_atk_cnt
        type_dict["skill_no_break_no_talent"] /= skill_atk_cnt
        type_dict["skill_break_no_talent"] /= skill_atk_cnt
        type_dict["skill_break_talent"] /= skill_atk_cnt

        for k, v in type_dict.items():
            print("%s: %.2f%%;" % (k, type_dict[k] * 100), end=" ")
        print()
        self.atk_type_dict = cp(type_dict)
        return type_dict

    def simulate(self, defense, magic_resistance, simulation_times=1000):
        if len(self.atk_type_dict.keys()) == 0:
            self.get_state_propotion_by_simulation(simulation_times)

        state_list = [self.NormalData, self.TalentNormalData, self.BreakNormalData, self.TalentNormalData,
                      self.SkillData, self.TalentSkillData, self.BreakSkillData, self.TalentSkillData]
        N, TN, BN, TBN, S, TS, BS, TBS = state_list
        N.atk_scale /= self.talent_atk_scale
        BN.atk_scale /= self.talent_atk_scale
        S.atk_scale /= self.talent_atk_scale
        BS.atk_scale /= self.talent_atk_scale
        BN.enemy_defense_decrease_ratio = self.enemy_def_decrease_ratio
        TBN.enemy_defense_decrease_ratio = self.enemy_def_decrease_ratio
        BS.enemy_defense_decrease_ratio = self.enemy_def_decrease_ratio
        TBS.enemy_defense_decrease_ratio = self.enemy_def_decrease_ratio
        for stage in state_list:
            stage.save_temp(defense, magic_resistance)

        damage_node = list()

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        def_decrease_remain = 0

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            def_decrease_remain -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    atk_cooldown = S.frame
                    damage += S.damage * self.atk_type_dict["skill_no_break_no_talent"] + \
                              BS.damage * self.atk_type_dict["skill_break_no_talent"] + \
                              TBS.damage * self.atk_type_dict["skill_break_talent"]
                else:
                    atk_cooldown = N.frame
                    damage += N.damage * self.atk_type_dict["skill_no_break_no_talent"] + \
                              BN.damage * self.atk_type_dict["skill_break_no_talent"] + \
                              TBN.damage * self.atk_type_dict["skill_break_talent"]

                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30

                damage_node.append((frame / 30, damage))

        return damage_node


class Manticore(CharacterData):
    def __init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict):
        CharacterData.__init__(self, name, skill_order, basic_info_dict, normal_info_dict, skill_info_dict)
        self.TalentNormalData = StateData(normal_info_dict, dmg_type=self.normal_damage_type, is_skill_state=False)
        self.TalentSkillData = StateData(skill_info_dict, dmg_type=self.skill_damage_type, is_skill_state=True)
        self.atk_buff_interval = 0
        self.atk_buff_value = 0

    def simulate(self, defense, magic_resistance):
        damage_node = list()
        N, TN = self.NormalData, self.TalentNormalData
        S, TS = self.SkillData, self.TalentSkillData
        TN.atk_up += self.atk_buff_value
        TS.atk_up += self.atk_buff_value
        N.save_temp(defense, magic_resistance)
        TN.save_temp(defense, magic_resistance)
        S.save_temp(defense, magic_resistance)
        TS.save_temp(defense, magic_resistance)

        curr_sp = self.init_sp * 30
        sp_cost = self.sp_cost * 30

        atk_cooldown = 0
        skill_remain = 0
        sp_recovery_block = 0

        frame = 0
        damage = 0
        stun = 0
        skill = False

        dot_remain = 0
        dot_interval = 0
        dot_dmg = 0

        talent_frame = self.atk_buff_interval * 30

        while frame < 300 * 30:
            frame += 1
            atk_cooldown -= 1
            skill_remain -= 1
            sp_recovery_block -= 1
            talent_frame -= 1

            if dot_dmg > 0 and dot_remain > 0:
                dot_remain -= 1
                dot_interval -= 1
                if dot_interval <= 0:
                    damage += dot_dmg
                    damage_node.append((frame / 30, damage))
                    dot_interval = 30

            if sp_recovery_block <= 0 and self.sp_type == "auto":
                curr_sp += self.sp_recovery

            if stun > 0:
                stun -= 1
                continue

            if skill_remain < 0 and skill:
                skill = False
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5
                stun = S.stun * 30

            if curr_sp >= sp_cost:
                skill_remain = self.skill_duration * 30
                skill = True
                sp_recovery_block = self.sp_recovery_block_time * 30
                curr_sp = 0.0
                if self.skill_reset_cooldown_flag:
                    atk_cooldown = 5

            if atk_cooldown <= 0:
                if skill:
                    if talent_frame > 0:
                        damage += S.damage * S.atk_times * S.equivalent_target_num
                        atk_cooldown = S.frame
                        if S.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = S.dot_frame
                            else:
                                dot_dmg = S.dot_damage
                                dot_remain = S.dot_frame
                    else:
                        damage += TS.damage * TS.atk_times * TS.equivalent_target_num
                        atk_cooldown = TS.frame
                        if TS.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = TS.dot_frame
                            else:
                                dot_dmg = TS.dot_damage
                                dot_remain = TS.dot_frame
                else:
                    if talent_frame > 0:
                        damage += N.damage * N.atk_times * N.equivalent_target_num
                        atk_cooldown = N.frame
                        if N.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = N.dot_frame
                            else:
                                dot_dmg = N.dot_damage
                                dot_remain = N.dot_frame
                    else:
                        damage += TN.damage * TN.atk_times * TN.equivalent_target_num
                        atk_cooldown = TN.frame
                        if TN.dot_damage > 0:
                            if dot_remain > 0:
                                dot_remain = TN.dot_frame
                            else:
                                dot_dmg = TN.dot_damage
                                dot_remain = TN.dot_frame
                talent_frame = self.atk_buff_interval * 30
                if sp_recovery_block <= 0 and self.sp_type == "attack":
                    curr_sp += 30
                damage_node.append((frame / 30, damage))

        return damage_node


def load_data(row):
    trait = eval(row["Trait Dict"])  # A dict. Not used. Info will be manually added.
    talent = eval(row["Talent Dict"])  # A dict. Used.
    skill = eval(row["Skill Dict"])  # A dict. Used.
    skill_type_dict = {"Auto": "auto", "Attack": "attack", "Defense": "defense", "Passive": "auto", }
    basic_info_dict = {
        "rarity": int(row["Rarity"]),
        "stage": row["Stage"],
        "prof": row["Profession"],
        "name": row["Char Name"],
        "skill": int(row["Skill Order"]),
        # "normal_damage_type": "physical",  # Manually modified
        # "skill_damage_type": "physical",  # Manually modified
        # "skill_type": "lasting",  # Manually modified
        "sp_type": skill_type_dict[row["SP Type"]],
        "sp_cost": float(row["SP Cost"]),
        "init_sp": float(row["Init SP"]),
        "sp_recovery": float(talent.get("sp_recovery_per_sec", 0.0)),
        "duration": float(row["Skill Duration"]),
        "block": float(row["Skill Duration"]),
        "reset": True
    }

    normal_info_dict = {
        "base_atk": int(row["Attack"]),
        "atk_time": float(row["Attack Interval"]),
        "attack_speed": float(row["Attack Speed Modifier"]) +
                        float(talent.get("attack_speed", 0)) * int(talent.get("max_stack_cnt", 1)),
        "atk": float(talent.get("atk", 0)) * int(talent.get("max_stack_cnt", 1)),
        "atk_scale": float(talent.get("atk_scale", 1.0)),
        "damage_scale": float(talent.get("damage_scale", 1.0)),
        "pene_ratio": float(talent.get("def_penetrate", 0)),
        "def_value": float(talent.get("def_penetrate_fixed", 0)),
        "base_attack_time_add": float(talent.get("base_attack_time", 0)),
    }

    skill_info_dict = cp(normal_info_dict)

    skill_info_dict["atk"] += float(skill.get("atk", 0.0))
    skill_info_dict["attack_speed"] += float(skill.get("attack_speed", 0))
    skill_info_dict["atk_scale"] *= float(skill.get("atk_scale", 1.0))
    skill_info_dict["base_attack_time_add"] += float(skill.get("base_attack_time", 0))

    return basic_info_dict, normal_info_dict, skill_info_dict


def modify_data(f, stage, multi_target=False):
    """
    Manually modify character data.
    Aim to deal with some special cases when calculating damage.

    :param f:                   file object
    :param stage:               <str> character stage
    :param defense:             <int> enemy defense
    :param magic_resistance:    <int> enemy magic resistance
    :param multi_target:        <bool> whether multi-target mode is on
    :return:    char_dict:      <dict> a dict containing characters
                                Format:
                                    <char key>: <CharacterData object>
                                    where <char key> is in format of "<Stage> - <CharName> - <SkillOrder> 技能"
                                Example:
                                    "29010-缠丸-1技能": <CharacterData object> corresponding to 缠丸
    """

    char_dict = dict()
    for row in f:
        if row["Stage"] != stage:
            continue
        name = row["Char Name"]
        skill_order = row["Skill Order"]
        key = "%s-%s-%s技能" % (stage, name, skill_order)

        # TODO: 近卫
        if name == "缠丸" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 1.2
            tmp.sp_recovery_block_time = 1.2
            tmp.skill_reset_cooldown_flag = False
            char_dict[key] = tmp
        elif name == "缠丸" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "芙兰卡" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0) * eval(row["Skill Dict"]).get("talent_scale", 1.0)
            tmp.TalentNormalData.penetration_ratio = 1.0
            tmp.TalentSkillData.penetration_ratio = 1.0
            char_dict[key] = tmp
        elif name == "芙兰卡" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0) * eval(row["Skill Dict"]).get("talent_scale", 1.0)
            tmp.TalentNormalData.penetration_ratio = 1.0
            tmp.TalentSkillData.penetration_ratio = 1.0
            char_dict[key] = tmp

        elif name == "炎客" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            char_dict[key] = tmp
        elif name == "炎客" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.infinite_skill_duration()
            char_dict[key] = tmp

        elif name == "斯卡蒂" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "斯卡蒂" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.release_on_deploy(eval(row["Skill Dict"]).get("duration", 0.0))
            char_dict[key] = tmp
        elif name == "斯卡蒂" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "杜宾" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            char_dict[key] = tmp
        elif name == "杜宾" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            char_dict[key] = tmp

        elif name == "诗怀雅" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Skill Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            char_dict[key] = tmp
        elif name == "诗怀雅" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            char_dict[key] = tmp

        elif name == "慕斯" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.replace_basic_attack()
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob")
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob")
            tmp.TalentNormalData.dmg_type = "magic"
            tmp.TalentSkillData.dmg_type = "magic"
            tmp.TalentNormalData.atk_times = 2
            tmp.TalentSkillData.atk_times = 2
            char_dict[key] = tmp
        elif name == "慕斯" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.replace_basic_attack()
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob")
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob")
            tmp.TalentNormalData.dmg_type = "magic"
            tmp.TalentSkillData.dmg_type = "magic"
            tmp.TalentNormalData.atk_times = 2
            tmp.TalentSkillData.atk_times = 2
            char_dict[key] = tmp

        elif name == "星极" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Astesia(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk_speed_up -= eval(row["Talent Dict"]).get("attack_speed", 0.0)
            tmp.SkillData.atk_speed_up -= eval(row["Talent Dict"]).get("attack_speed", 0.0)
            tmp.atk_speed_up_per_stage = eval(row["Talent Dict"]).get("attack_speed", 0.0)
            tmp.atk_speed_up_interval = eval(row["Talent Dict"]).get("interval", 0.0)
            tmp.maximum_stage = eval(row["Talent Dict"]).get("max_stack_cnt", 0.0)
            char_dict[key] = tmp
        elif name == "星极" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Astesia(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk_speed_up -= eval(row["Talent Dict"]).get("attack_speed", 0.0)
            tmp.SkillData.atk_speed_up -= eval(row["Talent Dict"]).get("attack_speed", 0.0)
            tmp.atk_speed_up_per_stage = eval(row["Talent Dict"]).get("attack_speed", 0.0)
            tmp.atk_speed_up_interval = eval(row["Talent Dict"]).get("interval", 0.0)
            tmp.maximum_stage = eval(row["Talent Dict"]).get("max_stack_cnt", 0.0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "霜叶" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.sp_recovery_block_time = 1.15
            char_dict[key] = tmp
        elif name == "霜叶" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "拉普兰德" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.infinite_skill_duration()
            char_dict[key] = tmp
        elif name == "拉普兰德" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_damage_type = tmp.SkillData.dmg_type = "magic"
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["3格远卫打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "银灰" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            char_dict[key] = tmp
        elif name == "银灰" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.infinite_skill_duration()
            char_dict[key] = tmp
        elif name == "银灰" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                target_num_key = "3格扇形打%.0f" % eval(row["Skill Dict"]).get("attack@max_target", 3.0)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "艾斯黛尔" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "艾斯黛尔" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_charge_on_defense(Charge_on_defense_equivalent_charge_speed)
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "暴行" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "暴行" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 8 / 30
            tmp.sp_recovery_block_time = 8 / 30
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                target_num_key = "3格打%.0f" % eval(row["Skill Dict"]).get("max_target", 3)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "幽灵鲨" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "幽灵鲨" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.stun = eval(row["Skill Dict"]).get("stun", 0.0)
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "布洛卡" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "布洛卡" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["3格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["3格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "煌" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "煌" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.infinite_skill_duration()
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["2格打3"]
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["2格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "煌" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = Blaze(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_reset_cooldown_flag = True
            tmp.SkillData.atk_up = 0.0
            tmp.SkillData.atk_scale = 1.0
            tmp.skill_gradual_atk = eval(row["Skill Dict"]).get('atk', 0)
            tmp.skill_final_atk_scale = eval(row["Skill Dict"]).get('damage_by_atk_scale', 1.0)
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打3"]
                    tmp.skill_gradual_target_num = target_num_dict["1格群攻"]
                    tmp.skill_final_target_num = target_num_dict["精一群法群攻"]
                    tmp.multi_target_desc = "普攻打%.0f,技能打%.0f/%.0f" % (target_num_dict["1格打3"],
                                                                      target_num_dict["1格群攻"],
                                                                      target_num_dict["精一群法群攻"])
                else:
                    tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                    tmp.skill_gradual_target_num = target_num_dict["1格群攻"]
                    tmp.skill_final_target_num = target_num_dict["精一群法群攻"]
                    tmp.multi_target_desc = "普攻打%.0f,技能打%.0f/%.0f" % (target_num_dict["1格打3"],
                                                                      target_num_dict["1格群攻"],
                                                                      target_num_dict["精一群法群攻"])
            char_dict[key] = tmp

        elif name == "赫拉格" and skill_order == "1":
            # Assume the talent always gives attack speed buff as set in `Hellagur_atk_speed`
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.SkillData.atk_times = 2
            MinAS = eval(row["Talent Dict"]).get('min_attack_speed', 0.0)
            MaxAS = eval(row["Talent Dict"]).get('max_attack_speed', 0.0)
            MinHP = eval(row["Talent Dict"]).get('min_hp_ratio', 0.0)
            MaxHP = eval(row["Talent Dict"]).get('max_hp_ratio', 1.0)
            if Hellagur_talent_hp_ratio <= MinHP:
                Hellagur_atk_speed = MinAS
            elif Hellagur_talent_hp_ratio >= MaxHP:
                Hellagur_atk_speed = MaxAS
            else:
                Hellagur_atk_speed = (MaxAS * (Hellagur_talent_hp_ratio - MinHP)
                                      + MinAS * (MaxHP - Hellagur_talent_hp_ratio)) / (MaxHP - MinHP)
            tmp.NormalData.atk_speed_up = Hellagur_atk_speed
            tmp.SkillData.atk_speed_up = Hellagur_atk_speed
            char_dict[key] = tmp
        elif name == "赫拉格" and skill_order == "2":
            # Assume the talent always gives attack speed buff as set in `Hellagur_atk_speed`
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_times = 2
            MinAS = eval(row["Talent Dict"]).get('min_attack_speed', 0.0)
            MaxAS = eval(row["Talent Dict"]).get('max_attack_speed', 0.0)
            MinHP = eval(row["Talent Dict"]).get('min_hp_ratio', 0.0)
            MaxHP = eval(row["Talent Dict"]).get('max_hp_ratio', 1.0)
            if Hellagur_talent_hp_ratio <= MinHP:
                Hellagur_atk_speed = MinAS
            elif Hellagur_talent_hp_ratio >= MaxHP:
                Hellagur_atk_speed = MaxAS
            else:
                Hellagur_atk_speed = (MaxAS * (Hellagur_talent_hp_ratio - MinHP)
                                      + MinAS * (MaxHP - Hellagur_talent_hp_ratio)) / (MaxHP - MinHP)
            tmp.NormalData.atk_speed_up = Hellagur_atk_speed
            tmp.SkillData.atk_speed_up = Hellagur_atk_speed
            char_dict[key] = tmp
        elif name == "赫拉格" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            MinAS = eval(row["Talent Dict"]).get('min_attack_speed', 0.0)
            MaxAS = eval(row["Talent Dict"]).get('max_attack_speed', 0.0)
            MinHP = eval(row["Talent Dict"]).get('min_hp_ratio', 0.0)
            MaxHP = eval(row["Talent Dict"]).get('max_hp_ratio', 1.0)
            if Hellagur_talent_hp_ratio <= MinHP:
                Hellagur_atk_speed = MinAS
            elif Hellagur_talent_hp_ratio >= MaxHP:
                Hellagur_atk_speed = MaxAS
            else:
                Hellagur_atk_speed = (MaxAS * (Hellagur_talent_hp_ratio - MinHP)
                                      + MinAS * (MaxHP - Hellagur_talent_hp_ratio)) / (MaxHP - MinHP)
            tmp.NormalData.atk_speed_up = Hellagur_atk_speed
            tmp.SkillData.atk_speed_up = Hellagur_atk_speed
            if multi_target:
                target_num_key = "%.0f格打%.0f" % (eval(row["Skill Dict"]).get("ability_range_forward_extend", 1.0) + 1,
                                                 eval(row["Skill Dict"]).get("attack@max_target", 3.0))
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "陈" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Chen(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_times = 2
            tmp.SkillData.atk_times = 1
            tmp.replace_basic_attack()
            char_dict[key] = tmp
        elif name == "陈" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Chen(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_times = 2
            tmp.SkillData.dmg_type = "mix"
            tmp.SkillData.mix_physical_scale = 5.0
            tmp.SkillData.mix_magic_scale = 5.0
            tmp.skill_duration = 8 / 30
            tmp.sp_recovery_block_time = 8 / 30
            if multi_target:
                target_num_key = "3格远卫打%.0f" % eval(row["Skill Dict"]).get("max_target", 4.0)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "陈" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = Chen(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_times = 2
            tmp.skill_duration = 4
            tmp.SkillData.frame = 12
            char_dict[key] = tmp

        elif name == "猎蜂" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.passive_skill()
            char_dict[key] = tmp
        elif name == "猎蜂" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_time_add_modifier -= eval(row["Skill Dict"]).get("base_attack_time", 0.0)
            tmp.SkillData.atk_time_mul_modifier += eval(row["Skill Dict"]).get("base_attack_time", 0.0)
            char_dict[key] = tmp

        elif name == "因陀罗" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            char_dict[key] = tmp
        elif name == "因陀罗" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            char_dict[key] = tmp

        # TODO: 术师
        elif name == "夜烟" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Haze(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.TalentNormalData.dmg_type = "magic"
            tmp.TalentSkillData.dmg_type = "magic"
            tmp.mr_reduction_duration = eval(row["Talent Dict"]).get("duration", 0)
            tmp.mr_reduction_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0)
            char_dict[key] = tmp
        elif name == "夜烟" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Haze(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.TalentNormalData.dmg_type = "magic"
            tmp.TalentSkillData.dmg_type = "magic"
            tmp.mr_reduction_duration = eval(row["Talent Dict"]).get("duration", 0)
            tmp.mr_reduction_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0)
            char_dict[key] = tmp

        elif name == "夜魔" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            char_dict[key] = tmp
        elif name == "夜魔" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.sp_cost = 9999  # Disable Nightmare's 2nd skill as unable to calculate damage of it.
            if multi_target:
                tmp.multi_target_desc = "不计2技能伤害"
            char_dict[key] = tmp

        elif name == "阿米娅" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Amiya(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.sp_recovery_by_atk = eval(row["Talent Dict"]).get("amiya_t_1[atk].sp", 0)
            char_dict[key] = tmp
        elif name == "阿米娅" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.sp_recovery_by_atk = eval(row["Talent Dict"]).get("amiya_t_1[atk].sp", 0)
            tmp.SkillData.atk_scale = eval(row["Skill Dict"]).get("attack@atk_scale", 1.0)
            tmp.SkillData.atk_times = eval(row["Skill Dict"]).get("attack@times", 1.0)
            tmp.SkillData.stun = eval(row["Skill Dict"]).get("stun", 0)
            char_dict[key] = tmp
        elif name == "阿米娅" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.sp_recovery_by_atk = eval(row["Talent Dict"]).get("amiya_t_1[atk].sp", 0)
            tmp.SkillData.dmg_type = "physical"  # Real damage, i.e., ignoring any armor and mr.
            tmp.SkillData.penetration_ratio = 1.00
            tmp.SkillData.stun = 70  # Retreat after skill, taking 70 sec to redeploy
            char_dict[key] = tmp

        elif name == "艾雅法拉" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Eyjafjalla(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.SecondSkillData.dmg_type = "magic"
            tmp.init_sp_gain = (eval(row["Talent Dict"]).get("sp_min", 0) + eval(row["Talent Dict"]).get("sp_max", 0)) / 2
            tmp.SkillData.atk_speed_up += eval(row["Skill Dict"]).get("amgoat_s_1[a].attack_speed", 0)
            tmp.SecondSkillData.atk_speed_up += eval(row["Skill Dict"]).get("amgoat_s_1[b].attack_speed", 0)
            tmp.SecondSkillData.atk_up += eval(row["Skill Dict"]).get("amgoat_s_1[b].atk", 0)
            char_dict[key] = tmp
        elif name == "艾雅法拉" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Eyjafjalla(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.TalentNormalData.dmg_type = "magic"
            tmp.TalentSkillData.dmg_type = "magic"
            tmp.replace_basic_attack()
            tmp.sp_recovery_block_time = 1.2
            tmp.init_sp_gain = (eval(row["Talent Dict"]).get("sp_min", 0) + eval(row["Talent Dict"]).get("sp_max", 0)) / 2
            tmp.mr_reduction_ratio = eval(row["Skill Dict"]).get("magic_resistance", 0)
            tmp.mr_reduction_duration = eval(row["Skill Dict"]).get("duration", 0)
            tmp.SkillData.equivalent_target_num = 2.0
            tmp.TalentSkillData.equivalent_target_num = 2.0
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"] + 1.0
                tmp.TalentSkillData.equivalent_target_num = target_num_dict["中半径圆溅射"] + 1.0
                tmp.multi_target_desc = "技能打%s" % target_num_dict["中半径圆溅射"]
            char_dict[key] = tmp
        elif name == "艾雅法拉" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.init_sp_gain = (eval(row["Talent Dict"]).get("sp_min", 0) + eval(row["Talent Dict"]).get("sp_max", 0)) / 2
            if multi_target:
                target_num_key = "3格菱形打%.0f" % eval(row["Skill Dict"]).get("attack@max_target", 3.0)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "格雷伊" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "格雷伊" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "远山" and skill_order == "1":
            # Assume 远山's talent buffs in attack speed
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "远山" and skill_order == "2":
            # Assume 远山's talent buffs in attack speed
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0)
            tmp.SkillData.stun = eval(row["Skill Dict"]).get("time", 0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["精一快狙群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "天火" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "天火" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.SkillData.atk_scale = eval(row["Skill Dict"]).get("attack@atk_scale", 0.0)
            tmp.SkillData.atk_time_add_modifier = 0
            tmp.SkillData.atk_time_mul_modifier = eval(row["Skill Dict"]).get("base_attack_time", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["大半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "莫斯提马" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "莫斯提马" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.SkillData.frame = 30
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["精一群法群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "莫斯提马" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["序时之匙群攻"] - 0.2
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "伊芙利特" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Ifrit(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.enemy_magic_resistance_decrease_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0.0)
            tmp.SkillData.enemy_magic_resistance_decrease_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0.0)
            tmp.sp_recovery_per_round = eval(row["Talent Dict"]).get("sp", 0.0)
            tmp.sp_recovery_interval = eval(row["Talent Dict"]).get("interval", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["5格群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["5格群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "伊芙利特" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Ifrit(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.replace_basic_attack()
            tmp.sp_recovery_block_time = 1.3
            tmp.NormalData.enemy_magic_resistance_decrease_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0.0)
            tmp.SkillData.enemy_magic_resistance_decrease_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0.0)
            tmp.sp_recovery_per_round = eval(row["Talent Dict"]).get("sp", 0.0)
            tmp.sp_recovery_interval = eval(row["Talent Dict"]).get("interval", 0.0)
            tmp.SkillData.dot_damage_raw = tmp.SkillData.atk * eval(row["Skill Dict"]).get("burn.atk_scale", 0.0)
            tmp.SkillData.dot_time = eval(row["Skill Dict"]).get("duration", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["5格群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["5格群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "伊芙利特" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = Ifrit(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.enemy_magic_resistance_decrease_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0.0)
            tmp.SkillData.enemy_magic_resistance_decrease_ratio = eval(row["Talent Dict"]).get("magic_resistance", 0.0)
            tmp.sp_recovery_per_round = eval(row["Talent Dict"]).get("sp", 0.0)
            tmp.sp_recovery_interval = eval(row["Talent Dict"]).get("interval", 0.0)
            tmp.SkillData.enemy_magic_resistance_decrease_value = eval(row["Skill Dict"]).get("magic_resistance", 0.0)
            tmp.SkillData.atk_time = 1.0
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["5格群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["5格群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        # TODO: 狙击
        elif name == "杰西卡" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            char_dict[key] = tmp
        elif name == "杰西卡" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "流星" and skill_order == "1":
            # Not attacking planes
            B, N, S = load_data(row)
            tmp = ArmorBreaker(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.skill_break_flag = True
            tmp.enemy_def_decrease_ratio = eval(row["Skill Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Skill Dict"]).get("duration", 0.0)
            char_dict[key] = tmp
            # Attacking planes
            key = "%s-%s-%s技能" % (stage, "流星(对空)", skill_order)
            B, N, S = load_data(row)
            tmp = ArmorBreaker("流星(对空)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.skill_break_flag = True
            tmp.enemy_def_decrease_ratio = eval(row["Skill Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Skill Dict"]).get("duration", 0.0)
            char_dict[key] = tmp
        elif name == "流星" and skill_order == "2":
            # Not attacking planes
            B, N, S = load_data(row)
            tmp = ArmorBreaker(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 1.0
            tmp.sp_recovery_block_time = 1.0
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.skill_break_flag = True
            tmp.enemy_def_decrease_ratio = eval(row["Skill Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Skill Dict"]).get("duration", 0.0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["精一快狙打5"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
            # Attacking planes
            key = "%s-%s-%s技能" % (stage, "流星(对空)", skill_order)
            B, N, S = load_data(row)
            tmp = ArmorBreaker("流星(对空)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 1.0
            tmp.sp_recovery_block_time = 1.0
            tmp.skill_break_flag = True
            tmp.enemy_def_decrease_ratio = eval(row["Skill Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Skill Dict"]).get("duration", 0.0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["精一快狙打5"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "红云" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "红云" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["精一快狙打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "蓝毒" and skill_order == "1":
            # Not considering the poison damage caused to multiple targets
            B, N, S = load_data(row)
            tmp = BluePoison(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.NormalData.dot_damage_raw = eval(row["Talent Dict"]).get("poison_damage", 0)
            tmp.NormalData.dot_time = eval(row["Talent Dict"]).get("duration", 0)
            tmp.SkillData.dot_damage_raw = eval(row["Talent Dict"]).get("poison_damage", 0)
            tmp.SkillData.dot_time = eval(row["Talent Dict"]).get("duration", 0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["精一快狙打2"]
                tmp.other_target_dot_raw = eval(row["Talent Dict"]).get("poison_damage", 0)
                tmp.other_target_dot_duration = eval(row["Talent Dict"]).get("duration", 0)
                tmp.other_target_dot_atk_scale = eval(row["Skill Dict"]).get("atk_scale", 1.0)
                tmp.other_target_num = target_num_dict["精一快狙打2"] - 1
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "蓝毒" and skill_order == "2":
            # Not considering the poison damage caused to multiple targets
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.dot_damage_raw = eval(row["Talent Dict"]).get("poison_damage", 0)
            tmp.NormalData.dot_time = eval(row["Talent Dict"]).get("duration", 0)
            tmp.SkillData.dot_damage_raw = eval(row["Talent Dict"]).get("poison_damage", 0)
            tmp.SkillData.dot_time = eval(row["Talent Dict"]).get("duration", 0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["精一快狙打3"] + 1.0
                tmp.other_target_dot_raw = eval(row["Talent Dict"]).get("poison_damage", 0)
                tmp.other_target_dot_duration = eval(row["Talent Dict"]).get("duration", 0)
                tmp.other_target_dot_atk_scale = eval(row["Skill Dict"]).get("atk_scale", 1.0)
                tmp.other_target_num = target_num_dict["精一快狙打3"] - 1
                tmp.multi_target_desc = "技能打%s" % target_num_dict["精一快狙打3"]
            char_dict[key] = tmp

        elif name == "白金" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Platinum(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.min_atk_interval = eval(row["Talent Dict"]).get("attack@min_delta", 1.0)
            tmp.min_atk_scale = eval(row["Talent Dict"]).get("attack@min_atk_scale", 1.0)
            tmp.max_atk_interval = eval(row["Talent Dict"]).get("attack@max_delta", 1.0)
            tmp.max_atk_scale = eval(row["Talent Dict"]).get("attack@max_atk_scale", 1.0)
            char_dict[key] = tmp
        elif name == "白金" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Platinum(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.infinite_skill_duration()
            tmp.min_atk_interval = eval(row["Talent Dict"]).get("attack@min_delta", 1.0)
            tmp.min_atk_scale = eval(row["Talent Dict"]).get("attack@min_atk_scale", 1.0)
            tmp.max_atk_interval = eval(row["Talent Dict"]).get("attack@max_delta", 1.0)
            tmp.max_atk_scale = eval(row["Talent Dict"]).get("attack@max_atk_scale", 1.0)
            char_dict[key] = tmp

        elif name == "灰喉" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_times = 2
            tmp.TalentSkillData.atk_times = 2
            char_dict[key] = tmp
        elif name == "灰喉" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_times = eval(row["Skill Dict"]).get("times", 1)
            tmp.TalentSkillData.atk_times = eval(row["Skill Dict"]).get("times", 1)
            char_dict[key] = tmp

        elif name == "能天使" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.SkillData.atk_times = eval(row["Skill Dict"]).get("times", 1)
            char_dict[key] = tmp
        elif name == "能天使" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_scale = eval(row["Skill Dict"]).get("attack@atk_scale", 1)
            tmp.SkillData.atk_times = eval(row["Skill Dict"]).get("attack@times", 1)
            char_dict[key] = tmp
        elif name == "能天使" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_scale = eval(row["Skill Dict"]).get("attack@atk_scale", 1)
            tmp.SkillData.atk_times = eval(row["Skill Dict"]).get("attack@times", 1)
            tmp.SkillData.atk_time_add_modifier += eval(row["Skill Dict"]).get("base_attack_time", 0)
            char_dict[key] = tmp

        elif name == "白雪" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "白雪" and skill_order == "2":
            # Assume the dart always hits 3 times
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dot_damage_raw = tmp.SkillData.atk * eval(row["Skill Dict"]).get("attack@atk_scale", 0) * \
                                           (tmp.SkillData.atk_up + 1.0) * target_num_dict["小半径圆溅射"]
            tmp.SkillData.dot_time = eval(row["Skill Dict"]).get("attack@duration", 1) * 2.1
            tmp.SkillData.atk = 0
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["小半径圆溅射"]
                tmp.SkillData.dot_damage_raw *= target_num_dict["小半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "陨星" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Meteorite(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.atk_up_ratio = eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.atk_up_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["超大半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "陨星" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Meteorite(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 0.5
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.atk_up_ratio = eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.atk_up_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_break_flag = True
            tmp.enemy_def_decrease_value = eval(row["Skill Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Skill Dict"]).get("duration", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "普罗旺斯" and skill_order == "1":
            # Not attacking enemy in the right frontal grid
            B, N, S = load_data(row)
            tmp = Provence(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.passive_skill()
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentNormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentSkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get('prob', 0.0)
            Provence_Wolfeye_atk_scale = (1 - Provence_Wolfeye_target_hp_ratio) / eval(row["Skill Dict"]).get(
                'hp_ratio_drop', 1.0) * eval(row["Skill Dict"]).get('atk_scale_up', 0.0) + 1.0
            tmp.SkillData.atk_scale *= Provence_Wolfeye_atk_scale
            tmp.TalentSkillData.atk_scale *= Provence_Wolfeye_atk_scale
            char_dict[key] = tmp
            # Attacking enemy in the right frontal grid
            key = "%s-%s-%s技能" % (stage, "普罗旺斯(正前方一格)", skill_order)
            B, N, S = load_data(row)
            tmp = Provence("普罗旺斯(正前方一格)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.passive_skill()
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentNormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentSkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get('prob2', 0.0)
            Provence_Wolfeye_atk_scale = (1 - Provence_Wolfeye_target_hp_ratio) / eval(row["Skill Dict"]).get(
                'hp_ratio_drop', 1.0) * eval(row["Skill Dict"]).get('atk_scale_up', 0.0) + 1.0
            tmp.SkillData.atk_scale *= Provence_Wolfeye_atk_scale
            tmp.TalentSkillData.atk_scale *= Provence_Wolfeye_atk_scale
            char_dict[key] = tmp
        elif name == "普罗旺斯" and skill_order == "2":
            # Not attacking enemy in the right frontal grid
            B, N, S = load_data(row)
            tmp = Provence(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentNormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentSkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get('prob', 0.0)
            char_dict[key] = tmp
            # Attacking enemy in the right frontal grid
            key = "%s-%s-%s技能" % (stage, "普罗旺斯(正前方一格)", skill_order)
            B, N, S = load_data(row)
            tmp = Provence("普罗旺斯(正前方一格)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentNormalData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.TalentSkillData.atk_scale /= eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get('atk_scale', 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get('prob2', 0.0)
            char_dict[key] = tmp

        elif name == "黑" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Schwarz(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_talent_prob = eval(row["Skill Dict"]).get("talent@prob", 0.0)
            tmp.enemy_def_decrease_ratio = eval(row["Talent Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Talent Dict"]).get("defdown_duration", 0.0)
            char_dict[key] = tmp
        elif name == "黑" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Schwarz(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_talent_prob = eval(row["Skill Dict"]).get("talent@prob", 0.0)
            tmp.enemy_def_decrease_ratio = eval(row["Talent Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Talent Dict"]).get("defdown_duration", 0.0)
            char_dict[key] = tmp
        elif name == "黑" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = Schwarz(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.talent_atk_scale = eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.talent_prob = eval(row["Talent Dict"]).get("prob", 0.0)
            tmp.skill_talent_prob = eval(row["Skill Dict"]).get("talent@prob", 0.0)
            tmp.enemy_def_decrease_ratio = eval(row["Talent Dict"]).get("def", 0.0)
            tmp.enemy_def_decrease_duration = eval(row["Talent Dict"]).get("defdown_duration", 0.0)
            char_dict[key] = tmp

        elif name == "安比尔" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "安比尔" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "守林人" and skill_order == "1":
            # Not attacking ranged enemy
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            char_dict[key] = tmp
            # Attacking ranged enemy
            key = "%s-%s-%s技能" % (stage, "守林人(远程敌人)", skill_order)
            B, N, S = load_data(row)
            tmp = CharacterData("守林人(远程敌人)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "守林人" and skill_order == "2":
            # Not attacking ranged enemy
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 2.0
            tmp.SkillData.atk_time = 2.0
            tmp.sp_recovery_block_time = 2.0
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            if multi_target:
                target_num_key = "战术电台%.0f发" % eval(row["Skill Dict"]).get("max_cnt", 2.0)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
            # Attacking ranged enemy
            key = "%s-%s-%s技能" % (stage, "守林人(远程敌人)", skill_order)
            B, N, S = load_data(row)
            tmp = CharacterData("守林人(远程敌人)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 2.0
            tmp.SkillData.atk_time = 2.0
            tmp.sp_recovery_block_time = 2.0
            if multi_target:
                target_num_key = "战术电台%.0f发" % eval(row["Skill Dict"]).get("max_cnt", 2.0)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "送葬人" and skill_order == "1":
            # Not attacking enemy in the right frontal row
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.SkillData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
            # Attacking enemy in the right frontal row
            key = "%s-%s-%s技能" % (stage, "送葬人(前方一排)", skill_order)
            B, N, S = load_data(row)
            tmp = CharacterData("送葬人(前方一排)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.SkillData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.NormalData.atk_scale *= eval(row["Trait Dict"]).get("atk_scale", 1.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "送葬人" and skill_order == "2":
            # Not attacking enemy in the right frontal row
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.SkillData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.SkillData.atk_times = 2
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
            # Attacking enemy in the right frontal row
            key = "%s-%s-%s技能" % (stage, "送葬人(前方一排)", skill_order)
            B, N, S = load_data(row)
            tmp = CharacterData("送葬人(前方一排)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.SkillData.enemy_defense_decrease_value = eval(row["Talent Dict"]).get("def_penetrate_fixed", 0)
            tmp.SkillData.atk_times = 2
            tmp.NormalData.atk_scale *= eval(row["Trait Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale *= eval(row["Trait Dict"]).get("atk_scale", 1.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["6格霰弹群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        # TODO: 先锋
        elif name == "清道夫" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_reset_cooldown_flag = False
            char_dict[key] = tmp
        elif name == "清道夫" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "德克萨斯" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_reset_cooldown_flag = False
            char_dict[key] = tmp
        elif name == "德克萨斯" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 2.2
            tmp.sp_recovery_block_time = 2.2
            tmp.SkillData.atk_time = 1.0
            tmp.SkillData.atk_up -= eval(row["Skill Dict"]).get("atk", 0.0)
            tmp.SkillData.dmg_type = "magic"
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["2格菱形群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "推进之王" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_reset_cooldown_flag = False
            char_dict[key] = tmp
        elif name == "推进之王" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.skill_duration = 1.65
            tmp.sp_recovery_block_time = 1.65
            tmp.SkillData.atk_time = 1.65
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["1格菱形群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "推进之王" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_scale = eval(row["Skill Dict"]).get("attack@atk_scale", 1.0)
            char_dict[key] = tmp

        elif name == "讯使" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_reset_cooldown_flag = False
            char_dict[key] = tmp
        elif name == "讯使" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "凛冬" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_reset_cooldown_flag = False
            char_dict[key] = tmp
        elif name == "凛冬" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp

        elif name == "桃金娘" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk = 0
            char_dict[key] = tmp
        elif name == "桃金娘" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk = 0
            char_dict[key] = tmp

        elif name == "红豆" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob1", 0.0)
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob2", 0.0)
            char_dict[key] = tmp
        elif name == "红豆" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.normal_trig_prob = eval(row["Talent Dict"]).get("prob1", 0.0)
            tmp.skill_trig_prob = eval(row["Talent Dict"]).get("prob2", 0.0)
            char_dict[key] = tmp

        elif name == "格拉尼" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "格拉尼" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["0格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "苇草" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "苇草" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "mix"
            tmp.SkillData.mix_physical_scale = 1.0
            tmp.SkillData.mix_magic_scale = eval(row["Skill Dict"]).get("attack@skill.atk_scale", 0.0)
            char_dict[key] = tmp

        # TODO: 辅助
        elif name == "地灵" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            char_dict[key] = tmp
        elif name == "地灵" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.SkillData.atk = 0
            char_dict[key] = tmp

        elif name == "真理" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            char_dict[key] = tmp
        elif name == "真理" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                target_num_key = "药物配置打%.0f" % eval(row["Skill Dict"]).get("max_target", 2)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "格劳克斯" and skill_order == "1":
            # Not attacking planes
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            if multi_target:
                target_num_key = "精一群奶打%.0f" % eval(row["Skill Dict"]).get("max_target", 2)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
            # Attacking planes
            key = "%s-%s-%s技能" % (stage, "格劳克斯(对空)", skill_order)
            B, N, S = load_data(row)
            tmp = CharacterData("格劳克斯(对空)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            if multi_target:
                target_num_key = "精一群奶打%.0f" % eval(row["Skill Dict"]).get("max_target", 2)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "格劳克斯" and skill_order == "2":
            # Not attacking planes
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.skill_duration = 1.5  # Wait for test
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale[normal]", 1.0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["3格菱形群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
            # Attacking planes
            key = "%s-%s-%s技能" % (stage, "格劳克斯(对空)", skill_order)
            B, N, S = load_data(row)
            tmp = CharacterData("格劳克斯(对空)", skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.skill_duration = 1.5  # Wait for test
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale[drone]", 1.0)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["3格菱形群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "安洁莉娜" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            char_dict[key] = tmp
        elif name == "安洁莉娜" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.SkillData.atk_time_add_modifier -= eval(row["Skill Dict"]).get("base_attack_time", 0.0)
            tmp.SkillData.atk_time_mul_modifier = eval(row["Skill Dict"]).get("base_attack_time", 0.0) - 1
            tmp.NormalData.atk = 0
            char_dict[key] = tmp
        elif name == "安洁莉娜" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.atk = 0
            if multi_target:
                target_num_key = "反重力打%.0f" % eval(row["Skill Dict"]).get("attack@max_target", 4)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "初雪" and skill_order == "1":
            # Take the expectation of talent effect, i.e. if talent increase 30% damage when enemy HP is below 40%, then
            # the damage increase expectation is 12%.
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.dmg_scale = (eval(row["Talent Dict"]).get("damage_scale", 0.0) - 1) * \
                                       eval(row["Talent Dict"]).get("hp_ratio", 0.0) + 1
            tmp.SkillData.dmg_scale = (eval(row["Talent Dict"]).get("damage_scale", 0.0) - 1) * \
                                      eval(row["Talent Dict"]).get("hp_ratio", 0.0) + 1
            if multi_target:
                if stage[0] == "1":
                    tmp.SkillData.equivalent_target_num = target_num_dict["精一初雪打2"]
                    tmp.generate_multi_target_desc()
                elif stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["精一初雪打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["精一初雪打2"]
                    tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "初雪" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.magic_damage()
            tmp.NormalData.dmg_scale = (eval(row["Talent Dict"]).get("damage_scale", 0.0) - 1) * \
                                       eval(row["Talent Dict"]).get("hp_ratio", 0.0) + 1
            tmp.SkillData.dmg_scale = (eval(row["Talent Dict"]).get("damage_scale", 0.0) - 1) * \
                                      eval(row["Talent Dict"]).get("hp_ratio", 0.0) + 1
            tmp.SkillData.enemy_magic_resistance_decrease_ratio = eval(row["Skill Dict"]).get("magic_resistance", 0.0)
            if multi_target:
                if stage[0] == "2":
                    tmp.NormalData.equivalent_target_num = target_num_dict["精一初雪打2"]
                    tmp.SkillData.equivalent_target_num = target_num_dict["精一初雪打2"]
                    tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        # TODO: 重装
        elif name == "雷蛇" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            tmp.sp_type = "auto"
            tmp.sp_recovery = (eval(row["Talent Dict"]).get("sp", 0.0) + 1.0) * Charge_on_defense_equivalent_charge_speed
            tmp.SkillData.stun = eval(row["Skill Dict"]).get("sp", 0.0)
            if multi_target:
                target_num_key = "2格打%.0f" % eval(row["Skill Dict"]).get("attack@max_target", 3)
                tmp.SkillData.equivalent_target_num = target_num_dict[target_num_key]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "星熊" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "星熊" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_time = 1.0
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["1格群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "坚雷" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            char_dict[key] = tmp
        elif name == "坚雷" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            tmp.sp_type = "auto"
            tmp.sp_recovery = Charge_on_defense_equivalent_charge_speed
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["0格打3"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "火神" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            char_dict[key] = tmp
        elif name == "火神" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["0格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "年" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            char_dict[key] = tmp
        elif name == "年" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.atk_up += eval(row["Skill Dict"]).get("nian_s_3[self].atk", 0.0)
            char_dict[key] = tmp

        # TODO: 特种
        elif name == "阿消" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.sp_recovery_block_time = 1.15
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "阿消" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 1.0
            tmp.sp_recovery_block_time = 1.0  # Wait for test
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "食铁兽" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.sp_recovery_block_time = 1.2
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.SkillData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "食铁兽" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 1.0
            tmp.sp_recovery_block_time = 0.8
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["1格打2"]
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "暗索" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.skill_duration = 2.1
            tmp.SkillData.atk_time = 2.1
            tmp.sp_recovery_block_time = 2.1
            char_dict[key] = tmp
        elif name == "暗索" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 2.1
            tmp.SkillData.atk_time = 2.1
            tmp.sp_recovery_block_time = 2.1
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["4格打2"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "崖心" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            tmp.replace_basic_attack()
            tmp.skill_duration = 2.1
            tmp.SkillData.atk_time = 2.1
            tmp.sp_recovery_block_time = 2.1
            char_dict[key] = tmp
        elif name == "崖心" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.skill_duration = 2.1
            tmp.SkillData.atk_time = 2.1
            tmp.sp_recovery_block_time = 2.1
            tmp.SkillData.penetration_ratio = 1.0
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["9格霰弹打3"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "雪雉" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.replace_basic_attack()
            tmp.skill_duration = 2.1
            tmp.SkillData.atk_time = 2.1
            tmp.sp_recovery_block_time = 2.1
            char_dict[key] = tmp
        elif name == "雪雉" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.SkillData.dmg_type = "magic"
            tmp.skill_duration = 2.1
            tmp.SkillData.atk_time = 2.1
            tmp.sp_recovery_block_time = 2.1
            if multi_target:
                tmp.SkillData.equivalent_target_num = target_num_dict["中半径圆溅射"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "伊桑" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.passive_skill()
            tmp.SkillData.dot_damage_raw = eval(row["Skill Dict"]).get("attack@poison_damage", 0.0)
            tmp.SkillData.dot_time = eval(row["Skill Dict"]).get("attack@duration", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.SkillData.dot_damage_raw *= target_num_dict["精零群奶群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "伊桑" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = CharacterData(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "狮蝎" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = Manticore(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.passive_skill()
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.TalentNormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.TalentSkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.atk_buff_interval = eval(row["Talent Dict"]).get("delay", 0.0)
            tmp.atk_buff_value = eval(row["Talent Dict"]).get("atk", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.TalentNormalData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.TalentSkillData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp
        elif name == "狮蝎" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = Manticore(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.NormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.SkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.TalentNormalData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.TalentSkillData.atk_up -= eval(row["Talent Dict"]).get("atk", 0.0)
            tmp.atk_buff_interval = eval(row["Talent Dict"]).get("delay", 0.0)
            tmp.atk_buff_value = eval(row["Talent Dict"]).get("atk", 0.0)
            if multi_target:
                tmp.NormalData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.TalentNormalData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.SkillData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.TalentSkillData.equivalent_target_num = target_num_dict["精零群奶群攻"]
                tmp.generate_multi_target_desc()
            char_dict[key] = tmp

        elif name == "阿" and skill_order == "1":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.normal_trig_prob = 0.25
            tmp.skill_trig_prob = 0.25
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.TalentNormalData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.TalentSkillData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            char_dict[key] = tmp
        elif name == "阿" and skill_order == "2":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.normal_trig_prob = 0.25
            tmp.skill_trig_prob = 0.25
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.TalentNormalData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.TalentSkillData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            char_dict[key] = tmp
        elif name == "阿" and skill_order == "3":
            B, N, S = load_data(row)
            tmp = TalentAtkBuff(name, skill_order, basic_info_dict=B, normal_info_dict=N, skill_info_dict=S)
            tmp.normal_trig_prob = 0.25
            tmp.skill_trig_prob = 0.25
            tmp.NormalData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.SkillData.atk_scale /= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.TalentNormalData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            tmp.TalentSkillData.atk_scale *= eval(row["Talent Dict"]).get("atk_scale", 1.0)
            char_dict[key] = tmp
    return char_dict


# Plot Color Config
color_dict = {
    "缠丸": "turquoise",
    "芙兰卡": "darkgoldenrod",
    "炎客": "darkorange",
    "斯卡蒂": "lightsteelblue",
    "杜宾": "navy",
    "诗怀雅": "wheat",
    "慕斯": "tan",
    "星极": "gold",
    "霜叶": "darkred",
    "拉普兰德": "silver",
    "银灰": "skyblue",
    "艾斯黛尔": "olivedrab",
    "暴行": "sandybrown",
    "幽灵鲨": "slateblue",
    "布洛卡": "y",
    "煌": "crimson",
    "赫拉格": "darkkhaki",
    "陈": "mediumvioletred",
    "猎蜂": "indianred",
    "因陀罗": "dimgray",

    "夜烟": "firebrick",
    "夜魔": "darkkhaki",
    "阿米娅": "#400010",
    "艾雅法拉": "tomato",
    "格雷伊": "yellow",
    "远山": "lightpink",
    "天火": "coral",
    "莫斯提马": "slateblue",
    "伊芙利特": "sandybrown",

    "杰西卡": "deeppink",
    "流星": "palegreen",
    "流星(对空)": "forestgreen",
    "红云": "darksalmon",
    "蓝毒": "skyblue",
    "白金": "darkgray",
    "灰喉": "indigo",
    "能天使": "antiquewhite",
    "白雪": "slategray",
    "陨星": "sandybrown",
    "普罗旺斯": "mediumslateblue",
    "普罗旺斯(正前方一格)": "slateblue",
    "黑": "palevioletred",
    "安比尔": "mediumturquoise",
    "守林人": "darkseagreen",
    "守林人(远程敌人)": "seagreen",
    "送葬人": "lightslategray",
    "送葬人(前方一排)": "slategray",

    "清道夫": "chocolate",
    "德克萨斯": "powderblue",
    "推进之王": "#8B7F4C",
    "讯使": "#CDC5BF",
    "凛冬": "brown",
    "桃金娘": "thistle",
    "红豆": "lightcoral",
    "格拉尼": "lightblue",
    "苇草": "peachpuff",

    "地灵": "purple",
    "真理": "rosybrown",
    "格劳克斯": "steelblue",
    "安洁莉娜": "dodgerblue",
    "初雪": "c",

    "雷蛇": "deepskyblue",
    "星熊": "mediumseagreen",
    "坚雷": "darkviolet",
    "火神": "dimgray",
    "年": "paleturquoise",

    "阿消": "orange",
    "食铁兽": "black",
    "暗索": "cornflowerblue",
    "崖心": "yellowgreen",
    "雪雉": "gainsboro",
    "伊桑": "cyan",
    "狮蝎": "violet",
    "阿": "darkorange",

    "": "",
}

# Linestyle config
# Rarity determines Linestyle and Marker
# Skill order determines Linewidth and Marker Size
ls_dict = {
    3: "-",
    4: (0, (10, 5)),
    5: (0, (11, 1, 3, 1, 3, 1)),
    6: "-"
}
ls_assist_dict = {
    3: "-",
    4: (0, (5, 2)),
    5: (0, (6, 1, 2, 1, 2, 1)),
    6: "-"
}
mk_dict = {
    3: "|",
    4: "",
    5: "",
    6: ""
}
lw_dict = {
    "1": 1,
    "2": 2,
    "3": 3
}
ms_dict = {
    "1": 5,
    "2": 7.5,
    "3": 10
}

# Just for transforming parameters into description text
multitarget2str = {
    False: "单体伤害",
    True: "群体伤害"
}
