from ashrpg.class_client import ClassClient
from ashrpg.feat_client import FeatClient
from ashrpg.roll_client import RollClient

rc = RollClient()
print(rc.roll_dice('4d6+2 6d4'))
