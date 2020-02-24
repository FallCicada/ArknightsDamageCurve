#!/usr/bin/env python
# coding:utf-8

import prepare
import character
import plot

if __name__ == "__main__":
    Stage = "29010"
    D = plot.DefaultPickList
    prepare.main()
    for Pick in [D["MeleePhysical"], D["MeleeMagic"], D["RangedPhysical"], D["RangedMagic"], D["Control"]]:
        for Enemy in character.enemy_dict.keys():
            PickList = Pick["PickList"]
            PickListName = Pick["PickListName"]
            Baseline = Pick["Baseline"]
            ShowSlayLine = Pick.get("ShowSlayLine", True)
            MultiTarget = Pick.get("MultiTarget", True)
            IgnorePolish = Pick.get("IgnorePolish", False)
            SimulateTime = 120

            plot.plot(Stage, PickList, PickListName, Baseline, Enemy, simulate_time=SimulateTime,
                      show_slay_line=ShowSlayLine, multi_target=MultiTarget, ignore_polish=IgnorePolish)
