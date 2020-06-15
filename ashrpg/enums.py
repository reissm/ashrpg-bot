from enum import Enum
from discord import Color

class FeatTypes(Enum):
    DIVINE = Color.from_rgb(255, 255, 255)
    MARTIAL = Color.orange()
    SKILL = Color.purple()
    WILD = Color.dark_green()

class ClassColors(Enum):
    BARBARIAN = Color.from_rgb(196, 30, 59)
    DRUID = Color.from_rgb(255, 125, 10)
    FIGHTER = Color.from_rgb(199, 156, 110)
    MONK = Color.from_rgb(0, 255, 150)
    PALADIN = Color.from_rgb(245, 140, 186)
    PRESTIGE = Color.from_rgb(222, 201, 17)
    PRIEST = Color.from_rgb(255, 255, 255)
    RANGER = Color.from_rgb(171, 212, 115)
    SORCERER = Color.from_rgb(148, 130, 201)
    SONGBLADE = Color.from_rgb(163, 48, 201)
    ROGUE = Color.from_rgb(255, 245, 105)
    WIZARD = Color.from_rgb(171, 212, 115)

    @classmethod
    def _missing_(cls, name):
        # A missing class name most likely means its a prestige class
        if name in cls.__members__:
            return cls[name]
        return cls.PRESTIGE
