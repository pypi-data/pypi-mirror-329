from birdbrain_finch import BirdbrainFinch
from birdbrain_hummingbird import BirdbrainHummingbird
from birdbrain_microbit import BirdbrainMicrobit

from BirdBrain import Hummingbird
#from BirdBrain import *

def test_instantiating_devices_old_way():
    #finch = BirdbrainFinch('B')
    hummingbird = BirdbrainHummingbird('A')
    hummingbird = Hummingbird('A')
