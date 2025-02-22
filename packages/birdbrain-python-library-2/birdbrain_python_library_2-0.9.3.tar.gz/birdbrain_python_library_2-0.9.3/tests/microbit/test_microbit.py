from birdbrain_exception import BirdbrainException
from birdbrain_hummingbird import BirdbrainHummingbird
from birdbrain_microbit import BirdbrainMicrobit
from birdbrain_state import BirdbrainState

import pytest
import time
import random

def test_connect_device_name_as_none():
    with pytest.raises(BirdbrainException) as e:
        microbit = BirdbrainMicrobit(None)
    assert e.value.message == "Missing device name"

def test_connect_bad_device_name():
    with pytest.raises(BirdbrainException) as e:
        microbit = BirdbrainMicrobit.connect('D')
    assert e.value.message == "Invalid device name: D"

def test_connect_valid_device_name():
    microbit = BirdbrainMicrobit.connect("A")

    assert microbit.device == "A"

def test_is():
    microbit = BirdbrainMicrobit.connect("A")

    assert microbit.is_connected()
    assert not microbit.is_microbit()
    assert microbit.is_hummingbird()
    assert not microbit.is_finch()

    assert microbit.isConnectionValid()
    assert not microbit.isMicrobit()
    assert microbit.isHummingbird()
    assert not microbit.isFinch()

def test_microbit_display_with_alias():
    hummingbird = BirdbrainHummingbird("A")

    assert hummingbird.microbit_display([ 1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1 ])

    time.sleep(0.15)

    assert hummingbird.setDisplay([ 0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0 ])

    time.sleep(0.15)

    hummingbird.stop_all()

def test_microbit_display_wrong_size():
    with pytest.raises(BirdbrainException) as e:
        hummingbird = BirdbrainHummingbird("A")

        hummingbird.microbit_display([ 0,1 ])
    assert e.value.message == "Error: microbit_display() requires a list of length 25"

def test_microbit_point_and_microbit_clear_display_with_alias():
    hummingbird = BirdbrainHummingbird("A")

    for i in range(2):
        assert hummingbird.microbit_point(2, 2, 1)
        assert hummingbird.microbit_point(2, 4, 1)
        assert hummingbird.microbit_point(4, 2, 1)
        assert hummingbird.setPoint(4, 4, 1)

        time.sleep(0.15)

        hummingbird.microbit_clear_display()

def test_microbit_point_true_or_false():
    hummingbird = BirdbrainHummingbird("A")

    assert hummingbird.microbit_point(3, 3, True)

    time.sleep(0.15)

    assert hummingbird.microbit_point(3, 3, False)

def test_microbit_point_out_of_range():
    with pytest.raises(BirdbrainException) as e:
        hummingbird = BirdbrainHummingbird("A")

        assert hummingbird.microbit_point(999, 1, 1)
    assert e.value.message == "Error: microbit_point out of range"

def test_microbit_print():
    hummingbird = BirdbrainHummingbird("A")

    hummingbird.microbit_print("A")

    time.sleep(1)

def test_microbit_play_note_with_alias():
    hummingbird = BirdbrainHummingbird("A")

    hummingbird.microbit_play_note(75, 0.5)

    time.sleep(0.25)

    hummingbird.playNote(40, 0.5)

    time.sleep(0.25)

    hummingbird.beep()

def test_stop_all():
    hummingbird = BirdbrainHummingbird("A")

    hummingbird.stop_all()
    hummingbird.stopAll()
