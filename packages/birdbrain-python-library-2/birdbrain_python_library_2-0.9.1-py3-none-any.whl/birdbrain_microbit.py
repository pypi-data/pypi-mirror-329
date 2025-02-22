from birdbrain_device import BirdbrainDevice
from birdbrain_exception import BirdbrainException
from birdbrain_microbit_input import BirdbrainMicrobitInput
from birdbrain_microbit_output import BirdbrainMicrobitOutput
from birdbrain_request import BirdbrainRequest

class BirdbrainMicrobit(BirdbrainDevice):
    def __init__(self, device = 'A', raise_exception_if_no_connection = True):
        self.device_object = BirdbrainMicrobit.connect(device, raise_exception_if_no_connection)

        if not self.is_microbit():
            raise BirdbrainException("Error: Device " + device + " is not a Microbit")

    def microbit_display(self, list):
        return BirdbrainMicrobitOutput.microbit_display(self.state, self.device, list)

    def microbit_clear_display(self):
        return BirdbrainMicrobitOutput.microbit_clear_display(self.state, self.device)

    def microbit_point(self, x, y, value):
        return BirdbrainMicrobitOutput.microbit_point(self.state, self.device, x, y, value)

    def microbit_print(self, message):
        return BirdbrainMicrobitOutput.microbit_print(self.state, self.device, message)

    def microbit_play_note(self, note, beats):
        return BirdbrainMicrobitOutput.microbit_play_note(self.device, note, beats)

    def beep(self):
        return BirdbrainMicrobitOutput.microbit_play_note(self.device, 80, 0.333)

    def acceleration(self):
        return BirdbrainMicrobitInput.acceleration(self.device)

    def compass(self):
        return BirdbrainMicrobitInput.compass(self.device)

    def magnetometer(self):
        return BirdbrainMicrobitInput.magnetometer(self.device)

    def button(self, button):
        return BirdbrainMicrobitInput.button(self.device, button)

    def sound(self, port = None):
        return BirdbrainMicrobitInput.sound(self.device)

    def temperature(self):
        return BirdbrainMicrobitInput.temperature(self.device)

    def is_shaking(self):
        return BirdbrainMicrobitInput.is_shaking(self.device)

    def orientation(self):
        return BirdbrainMicrobitInput.orientation(self.device)

    def stop_all(self):
        BirdbrainRequest.stop_all(self.device)

    getAcceleration = acceleration
    getButton = button
    getCompass = compass
    setDisplay = microbit_display
    isShaking = is_shaking
    getMagnetometer = magnetometer
    getOrientation = orientation
    playNote = microbit_play_note
    setPoint = microbit_point
    getSound = sound
    stopAll = stop_all
    getTemperature = temperature
