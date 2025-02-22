from birdbrain_finch import BirdbrainFinch
from birdbrain_hummingbird import BirdbrainHummingbird
from birdbrain_microbit import BirdbrainMicrobit

def test_instantiating_devices_old_way():
    finch = BirdbrainFinch('B')
    hummingbird = BirdbrainHummingbird('A')
