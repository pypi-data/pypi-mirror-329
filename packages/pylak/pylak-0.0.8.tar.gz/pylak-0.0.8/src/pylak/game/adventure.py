"""
assets for adventure game
"""

from ..fileloader import getFilepathInResources
from ..asset import AssetCollection

GRASS = AssetCollection(getFilepathInResources('MiniWorldSprites/Ground/TexturedGrass.png'), 3,2)
DEADGRASS = AssetCollection(getFilepathInResources('MiniWorldSprites/Ground/DeadGrass.png'), 3,2)
SHORE = AssetCollection(getFilepathInResources('MiniWorldSprites/Ground/Shore.png'), 5, 1)
HOUSES = AssetCollection(getFilepathInResources('MiniWorldSprites/Buildings/Wood/Houses.png'), 3, 4)
DOCKS = AssetCollection(getFilepathInResources('MiniWorldSprites/Buildings/Wood/Docks.png'), 4, 2)
WARRIOR = AssetCollection(getFilepathInResources('Tiny_Swords/Factions/Knights/Troops/Warrior/Purple/Warrior_Purple.png'), 6, 8)