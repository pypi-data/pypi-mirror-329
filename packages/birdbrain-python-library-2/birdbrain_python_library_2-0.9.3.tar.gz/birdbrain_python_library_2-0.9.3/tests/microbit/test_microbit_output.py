import pytest
import time

from birdbrain_device import BirdbrainDevice
from birdbrain_exception import BirdbrainException
from birdbrain_microbit import BirdbrainMicrobit
from birdbrain_microbit_output import BirdbrainMicrobitOutput
from birdbrain_request import BirdbrainRequest
from birdbrain_state import BirdbrainState

def test_microbit_display():
    state = BirdbrainState()

    BirdbrainMicrobitOutput.microbit_display(state, "A", [ 0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0 ])

    time.sleep(0.15)

    BirdbrainRequest.stop_all("A")

def test_microbit_display_wrong_size():
    with pytest.raises(BirdbrainException) as e:
        state = BirdbrainState()

        list = [ 0,1 ]

        BirdbrainMicrobitOutput.microbit_display(state, "A", list)
    assert e.value.message == "Error: microbit_display() requires a list of length 25"

def test_microbit_point_and_microbit_clear_display():
    state = BirdbrainState()

    for i in range(2):
        assert BirdbrainMicrobitOutput.microbit_point(state, "A", 1, 1, 1)
        assert BirdbrainMicrobitOutput.microbit_point(state, "A", 1, 5, 1)
        assert BirdbrainMicrobitOutput.microbit_point(state, "A", 5, 1, 1)
        assert BirdbrainMicrobitOutput.microbit_point(state, "A", 5, 5, 1)

        time.sleep(0.15)

        BirdbrainMicrobitOutput.microbit_clear_display(state, "A")

def test_microbit_point_true_or_false():
    state = BirdbrainState()

    assert BirdbrainMicrobitOutput.microbit_point(state, "A", 3, 3, True)

    time.sleep(0.15)

    assert BirdbrainMicrobitOutput.microbit_point(state, "A", 3, 3, False)

def test_microbit_point_out_of_range():
    with pytest.raises(BirdbrainException) as e:
        state = BirdbrainState()

        assert BirdbrainMicrobitOutput.microbit_point(state, "A", 999, 1, 1)
    assert e.value.message == "Error: microbit_point out of range"

def test_microbit_print():
    state = BirdbrainState()

    assert BirdbrainMicrobitOutput.microbit_print(state, "A", "B")
    time.sleep(1)

    assert BirdbrainMicrobitOutput.microbit_print(state, "A", " ")
    time.sleep(1)

def test_microbit_play_note():
    assert BirdbrainMicrobitOutput.microbit_play_note("A", 50, 0.25)
