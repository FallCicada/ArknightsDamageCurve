import json
import re
import csv
import os

skill_raw_data = open("raw/skill_table.json", 'r').read()
skill_dict = json.loads(skill_raw_data)
char_raw_data = open("raw/character_table.json", 'r').read()
char_dict = json.loads(char_raw_data)
potential_key = {0: "maxHP", 1: "atk", 2: "def", 3: "magicResistance",
                 4: "cost", 7: "attackSpeed", 21: "respawnTime"}
sp_type_key = {1: "Auto", 2: "Attack", 4: "Defense", 8: "Passive"}
skill_type_key = {0: "Passive", 1: "Manual", 2: "Auto"}

char_tree = {
    "Guard": {
        "Single Guard 1": ["玫兰莎"],
        "Single Guard 2": ["缠丸", "芙兰卡", "炎客"],
        "Single Guard 3": ["斯卡蒂"],
        "Support Guard 1": [],
        "Support Guard 2": ["杜宾", "诗怀雅"],
        "Support Guard 3": [],
        "Magic Guard 1": [],
        "Magic Guard 2": ["慕斯", "星极"],
        "Magic Guard 3": [],
        "Ranged Guard 1": ["月见夜"],
        "Ranged Guard 2": ["霜叶", "拉普兰德"],
        "Ranged Guard 3": ["银灰"],
        "Multiple Guard 1": ["泡普卡"],
        "Multiple Guard 2": ["艾丝黛尔", "暴行", "幽灵鲨", "布洛卡"],
        "Multiple Guard 3": ["煌"],
        "Berserk Guard 1": [],
        "Berserk Guard 2": [],
        "Berserk Guard 3": ["赫拉格"],
        "Double Guard 1": [],
        "Double Guard 2": [],
        "Double Guard 3": ["陈"],
        "Box Guard 1": [],
        "Box Guard 2": ["猎蜂", "因陀罗"],
        "Box Guard 3": [],
    },
    "Caster": {
        "Single Caster 1": ["史都华德"],
        "Single Caster 2": ["夜烟", "夜魔"],
        "Single Caster 3": ["阿米娅", "艾雅法拉"],
        "Splash Caster 1": ["炎熔"],
        "Splash Caster 2": ["格雷伊", "远山", "天火"],
        "Splash Caster 3": ["莫斯提马"],
        "AOE Caster 1": [],
        "AOE Caster 2": [],
        "AOE Caster 3": ["伊芙利特"],
        "Link Caster 1": [],
        "Link Caster 2": [],  # "惊蛰", Leizi
        "Link Caster 3": [],
    },
    "Sniper": {
        "Single Sniper 1": ["克洛丝", "安德切尔"],
        "Single Sniper 2": ["杰西卡", "流星", "红云", "蓝毒", "白金", "灰喉"],
        "Single Sniper 3": ["能天使"],
        "Splash Sniper 1": ["空爆"],
        "Splash Sniper 2": ["白雪", "陨星"],
        "Splash Sniper 3": [],
        "Close Sniper 1": [],
        "Close Sniper 2": ["普罗旺斯"],
        "Close Sniper 3": ["黑"],
        "Far Sniper 1": [],
        "Far Sniper 2": ["安比尔", "守林人"],
        "Far Sniper 3": [],
        "Shotgun Sniper 1": [],
        "Shotgun Sniper 2": ["送葬人"],
        "Shotgun Sniper 3": [],
    },
    "Vanguard": {
        "Offensive Vanguard 1": ["香草"],
        "Offensive Vanguard 2": ["清道夫", "德克萨斯"],
        "Offensive Vanguard 3": ["推进之王"],
        "Defensive Vanguard 1": ["芬"],
        "Defensive Vanguard 2": ["讯使", "凛冬"],
        "Defensive Vanguard 3": [],
        "Supportive Vanguard 1": [],
        "Supportive Vanguard 2": ["桃金娘"],
        "Supportive Vanguard 3": [],
        "Evacuable Vanguard 1": ["翎羽"],
        "Evacuable Vanguard 2": ["红豆", "格拉尼", "苇草"],
        "Evacuable Vanguard 3": [],
    },
    "Support": {
        "Decelerating Support 1": ["梓兰"],
        "Decelerating Support 2": ["地灵", "真理", "格劳克斯"],
        "Decelerating Support 3": ["安洁莉娜"],
        "Summon Support 1": [],
        "Summon Support 2": ["深海色", "梅尔"],
        "Summon Support 3": ["麦哲伦"],
        "Debuff Support 1": [],
        "Debuff Support 2": ["初雪"],
        "Debuff Support 3": [],
        "Buff Support 1": [],
        "Buff Support 2": ["空"],
        "Buff Support 3": [],
    },
    "Tank": {
        "HP Tank 1": ["卡缇"],
        "HP Tank 2": [],
        "HP Tank 3": [],
        "Defensive Tank 1": ["米格鲁"],
        "Defensive Tank 2": ["蛇屠箱", "可颂", "雷蛇", "拜松"],
        "Defensive Tank 3": ["星熊"],
        "Healing Tank 1": ["斑点"],
        "Healing Tank 2": ["古米", "临光", "吽"],
        "Healing Tank 3": ["塞雷娅"],
        "Magic Tank 1": [],
        "Magic Tank 2": ["角峰"],
        "Magic Tank 3": [],
        "Offensive Tank 1": [],
        "Offensive Tank 2": ["坚雷", "火神"],
        "Offensive Tank 3": [],
        "Supportive Tank 1": [],
        "Supportive Tank 2": [],
        "Supportive Tank 3": ["年"],
    },
    "Special": {
        "Pushing Special 1": [],
        "Pushing Special 2": ["阿消", "食铁兽"],
        "Pushing Special 3": [],
        "Pulling Special 1": [],
        "Pulling Special 2": ["暗索", "崖心", "雪雉"],
        "Pulling Special 3": [],
        "AOE Special 1": [],
        "AOE Special 2": ["伊桑", "狮蝎"],
        "AOE Special 3": [],
        "Redeployable Special 1": [],
        "Redeployable Special 2": ["砾", "红", "槐琥"],
        "Redeployable Special 3": [],
        "Supportive Special 1": [],
        "Supportive Special 2": [],
        "Supportive Special 3": ["阿"],
    },
    "Medic": {
        "Single Medic 1": ["安赛尔", "芙蓉"],
        "Single Medic 2": ["末药", "嘉维尔", "苏苏洛", "赫默", "华法琳"],
        "Single Medic 3": ["闪灵"],
        "Wide Medic 1": [],
        "Wide Medic 2": ["锡兰"],
        "Wide Medic 3": [],
        "Multiple Medic 1": [],
        "Multiple Medic 2": ["调香师", "白面鸮", "微风"],
        "Multiple Medic 3": ["夜莺"],
    },
}

trait_key_set = set()
talent_key_set = set()
skill_key_set = set()


def find_character_key(char_dict_, name_):
    for key, info_dict in char_dict_.items():
        if name_ == info_dict["name"]:
            return key
    return None


def find_trait(candidates_, level_, phase_, potential_):
    trait = dict()
    trait_description = None
    for i in range(len(candidates_)):
        condition = ((phase_ > candidates_[i]["unlockCondition"]["phase"] and
                      potential_ >= candidates_[i]["requiredPotentialRank"]) or
                     (phase_ == candidates_[i]["unlockCondition"]["phase"] and
                      level_ >= candidates_[i]["unlockCondition"]["level"] and
                      potential_ >= candidates_[i]["requiredPotentialRank"]))
        if condition:
            trait_description = candidates_[i]["overrideDescripton"]
            for item in candidates_[i]["blackboard"]:
                trait[item["key"]] = item["value"]
                trait_key_set.add(item["key"])

    return trait, trait_description


def find_talent(candidates_, level_, phase_, potential_):
    talent = dict()
    talent_description = None
    for i in range(len(candidates_)):
        condition = ((phase_ > candidates_[i]["unlockCondition"]["phase"] and
                      potential_ >= candidates_[i]["requiredPotentialRank"]) or
                     (phase_ == candidates_[i]["unlockCondition"]["phase"] and
                      level_ >= candidates_[i]["unlockCondition"]["level"] and
                      potential_ >= candidates_[i]["requiredPotentialRank"]))
        if condition:
            talent_description = candidates_[i]["description"]
            for item in candidates_[i]["blackboard"]:
                talent[item["key"]] = item["value"]
                talent_key_set.add(item["key"])
    return talent, talent_description


def find_potential(candidates_):
    potential_description = list()
    potential_data = dict()
    for buff in candidates_:
        potential_description.append(buff["description"])
        if buff["type"] == 0:
            key_list = buff["buff"]["attributes"]["attributeModifiers"]
            for elem in key_list:
                key = potential_key[elem["attributeType"]]
                if key in potential_data.keys():
                    potential_data[key] += elem["value"]
                else:
                    potential_data[key] = elem["value"]
    return potential_data, potential_description


def get_skill_description(raw_description_, blackboard_):
    description = raw_description_
    match_obj = re.compile(r'<@(.+?)>'  # 1 : style
                           r'([^{<]*)'  # 2 : pre_content
                           r'{?'
                           r'(-?)'  # 3 : symbol of keyword
                           r'([^:}<]*)'  # 4 : keyword
                           r':?'
                           r'([^}<]*)'  # 5 : format
                           r'}?'
                           r'([^<]*)'  # 6 : post_content
                           r'</>')

    def format_keyword(matched):
        pre_content = matched.group(2)
        symbol = matched.group(3)
        keyword = matched.group(4)
        format = matched.group(5)
        post_content = matched.group(6)
        if keyword:
            value = blackboard_[keyword.lower()]
            if symbol == '-':
                value = -value
            if format == "0%":
                return "%s%d%%%s" % (pre_content, value * 100, post_content)
            elif format == "0.0":
                return "%s%.1f%s" % (pre_content, value, post_content)
            elif format == "0":
                return "%s%d%s" % (pre_content, value, post_content)
            else:
                return "%s%d%s" % (pre_content, value, post_content)
        else:
            return pre_content

    description = match_obj.sub(format_keyword, description)
    return description


def find_data(name, skill_order, level, phase, skill_level, potential,
              level_compensation_flag=True, potential_check_flag=True):
    char_key = find_character_key(char_dict, name)
    char_info_dict = char_dict[char_key]

    # ---------- basic info ----------
    name = char_info_dict["name"]
    prof = char_info_dict["profession"].lower()
    rarity = int(char_info_dict["rarity"]) + 1

    # ---------- compensation ----------
    # For characters with rarity less than 4☆, set potential to 6.
    # For characters with rarity 3☆, with level greater than *Phase 1, Level 50*, set level to 55 (max level).
    if level_compensation_flag:
        if phase == 1 and level >= 50 and rarity == 3:
            level = 55
    if potential_check_flag:
        if rarity <= 4:
            potential = 6

    # ---------- traits, talents ----------
    trait, trait_description_list = dict(), list()
    if char_info_dict["trait"]:
        candidate = char_info_dict["trait"]
        trait_part, trait_description = find_trait(candidate["candidates"], level, phase, potential)
        trait.update(trait_part)
        trait_description_list.append(trait_description)
    talent, talent_description_list = dict(), list()
    if char_info_dict["talents"]:
        for candidate in char_info_dict["talents"]:
            talent_part, talent_description = find_talent(candidate["candidates"], level, phase, potential)
            talent.update(talent_part)
            talent_description_list.append(talent_description)

    # ---------- basic data, potential, favor ----------
    maxLevel = int(char_info_dict["phases"][phase]["maxLevel"])
    level = min(level, maxLevel)
    min_level_data = char_info_dict["phases"][phase]["attributesKeyFrames"][0]["data"]
    max_level_data = char_info_dict["phases"][phase]["attributesKeyFrames"][1]["data"]
    potential_raw = char_info_dict["potentialRanks"][0:potential - 1]
    potential_data, potential_description = find_potential(potential_raw) if potential_raw else ({}, [])
    favor_data = char_info_dict["favorKeyFrames"][1]["data"]

    # ---------- basic panel data ----------
    maxHP = (level - 1) / (maxLevel - 1) * max_level_data["maxHp"] + \
            (maxLevel - level) / (maxLevel - 1) * min_level_data["maxHp"] + \
            potential_data.get("maxHP", 0) + favor_data["maxHp"]
    attack = (level - 1) / (maxLevel - 1) * max_level_data["atk"] + \
             (maxLevel - level) / (maxLevel - 1) * min_level_data["atk"] + \
             potential_data.get("atk", 0) + favor_data["atk"]
    defense = (level - 1) / (maxLevel - 1) * max_level_data["def"] + \
              (maxLevel - level) / (maxLevel - 1) * min_level_data["def"] + \
              potential_data.get("def", 0) + favor_data["def"]
    magic_resistance = (level - 1) / (maxLevel - 1) * max_level_data["magicResistance"] + \
                       (maxLevel - level) / (maxLevel - 1) * min_level_data["magicResistance"] + \
                       potential_data.get("magicResistance", 0) + favor_data["magicResistance"]
    cost = min_level_data["cost"] + potential_data.get("cost", 0)
    respawnTime = min_level_data["respawnTime"] + potential_data.get("respawnTime", 0)
    base_attack_time = min_level_data["baseAttackTime"]
    attack_speed_modifier = potential_data.get("attackSpeed", 0)
    block_cnt = min_level_data["blockCnt"]

    # ---------- basic skill data ----------
    skill_key = char_info_dict["skills"][skill_order - 1]["skillId"]
    skill_info = skill_dict[skill_key]["levels"][skill_level - 1]

    skill_name = skill_info["name"]
    sp_type = skill_info["spData"]["spType"]
    # 1: auto charge, 2: attack-charge, 4: defense-charge, 8: passive
    skill_type = skill_info["skillType"]
    # 1: manual trigger, 2: auto trigger, not used

    max_charge_time = skill_info["spData"]["maxChargeTime"]
    sp_cost = skill_info["spData"]["spCost"]
    init_sp = skill_info["spData"]["initSp"]
    increment = skill_info["spData"]["increment"]
    duration = skill_info["duration"]
    # -1:  check blackboard oterwise eternal, 0: check blackboard otherwise passive, >=1: normal

    # ---------- generate skill description ----------
    skill_blackboard = dict()
    for item in skill_info["blackboard"]:
        skill_blackboard[item["key"]] = item["value"]
        skill_key_set.add(item["key"])

    skill_description = get_skill_description(skill_info["description"], skill_blackboard)

    # ---------- generate general description ----------
    general_description = "角色 : %s, 精英化 : %s, 等级 : %s\n" % (name, phase, level) + \
                          "技能 : %s, 技能等级 : %s\n" % (skill_name, skill_level) + \
                          "面板数据 :\n" + \
                          "\t生命 : %d\n\t攻击 : %d\n" % (maxHP, attack) + \
                          "\t防御 : %d\n\t法抗 : %d\n" % (defense, magic_resistance) + \
                          "\tCost : %d\n\t攻击间隔 : %.2fs\n" % (cost, base_attack_time) + \
                          "\t再部署 : %-2ss\n\t阻挡数 : %s\n" % (respawnTime, block_cnt) + \
                          "技能数据 :\n" + \
                          "\t%-2s级, %s\n" % (skill_level, skill_name) + \
                          "\t回复类型 : %s\n" % sp_type_key[sp_type] + \
                          "\t释放类型 : %s\n" % skill_type_key[skill_type] + \
                          "\t技力消耗 : %-3s\n\t初始技力 : %-3s\n" % (sp_cost, init_sp) + \
                          "\t持续时间 : %-3s\n\t充能次数 : %s\n" % (duration, max_charge_time) + \
                          "\t技能效果 : %s\n" % skill_description + \
                          "潜能数据 :\n" + \
                          "\t%s" % '\n\t'.join(potential_description)

    # print(general_description)
    used_info = [rarity, round(attack), base_attack_time, attack_speed_modifier,
                 sp_type_key[sp_type], sp_cost, init_sp, duration,
                 trait, trait_description_list,
                 talent, talent_description_list,
                 skill_blackboard, skill_description]
    return general_description, used_info


def find_1507_data(name, skill_order):
    general_description, used_info = find_data(name=name, skill_order=skill_order, level=50,
                                               phase=1, skill_level=7, potential=1)
    return general_description, used_info


def find_2307_data(name, skill_order):
    general_description, used_info = find_data(name=name, skill_order=skill_order, level=30,
                                               phase=2, skill_level=7, potential=1)
    return general_description, used_info


def find_25010_data(name, skill_order):
    general_description, used_info = find_data(name=name, skill_order=skill_order, level=50,
                                               phase=2, skill_level=10, potential=1)
    return general_description, used_info


def find_29010_data(name, skill_order):
    general_description, used_info = find_data(name=name, skill_order=skill_order, level=90,
                                               phase=2, skill_level=10, potential=1)
    return general_description, used_info


def main():
    f = open("raw/RawData.csv", "w")
    f = csv.writer(f, dialect="excel")
    header = ["Stage", "Profession", "Detailed Profession",
              "Char Name", "Skill Order", "Rarity",
              "Attack", "Attack Interval", "Attack Speed Modifier",
              "SP Type", "SP Cost", "Init SP", "Skill Duration",
              "Trait Dict", "Trait Desc",
              "Talent Dict", "Talent Desc",
              "Skill Dict", "Skill Desc"]
    f.writerow(header)

    # ---------- Write "1507" Data ----------
    for prof, prof_dict in char_tree.items():
        for detailed_prof, char_list in prof_dict.items():
            if char_list:
                if "1" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_1507_data(char, 1)
                        row = [1507, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                elif "2" in list(detailed_prof) or "3" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_1507_data(char, 1)
                        row = [1507, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_1507_data(char, 2)
                        row = [1507, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)

    # ---------- Write "2307" Data ----------
    for prof, prof_dict in char_tree.items():
        for detailed_prof, char_list in prof_dict.items():
            if char_list:
                if "2" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_2307_data(char, 1)
                        row = [2307, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_2307_data(char, 2)
                        row = [2307, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                elif "3" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_2307_data(char, 1)
                        row = [2307, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_2307_data(char, 2)
                        row = [2307, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_2307_data(char, 3)
                        row = [2307, prof, detailed_prof, char, 3]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)

    # ---------- Write "25010" Data ----------
    for prof, prof_dict in char_tree.items():
        for detailed_prof, char_list in prof_dict.items():
            if char_list:
                if "2" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_25010_data(char, 1)
                        row = [25010, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_25010_data(char, 2)
                        row = [25010, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                elif "3" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_25010_data(char, 1)
                        row = [25010, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_25010_data(char, 2)
                        row = [25010, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_25010_data(char, 3)
                        row = [25010, prof, detailed_prof, char, 3]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)

    # ---------- Write "29010" Data ----------
    for prof, prof_dict in char_tree.items():
        for detailed_prof, char_list in prof_dict.items():
            if char_list:
                if "2" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_29010_data(char, 1)
                        row = [29010, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_29010_data(char, 2)
                        row = [29010, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                elif "3" in list(detailed_prof):
                    for char in char_list:
                        _, used_info = find_29010_data(char, 1)
                        row = [29010, prof, detailed_prof, char, 1]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_29010_data(char, 2)
                        row = [29010, prof, detailed_prof, char, 2]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)
                        _, used_info = find_29010_data(char, 3)
                        row = [29010, prof, detailed_prof, char, 3]
                        row.extend(used_info)
                        print(row)
                        f.writerow(row)

if __name__ == "__main__":
    main()
