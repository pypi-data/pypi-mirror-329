class BirdbrainState:
    def __init__(self):
        self.microbit_display_map = BirdbrainState.microbit_empty_display_map()

    def microbit_display_map_clear(self):
        self.microbit_display_map = BirdbrainState.microbit_empty_display_map

    def set_list(self, list):
        self.microbit_display_map = list

    def set_pixel(self, x, y, value):
        self.microbit_display_map[((x * 5) + y - 6)] = value

    def microbit_display_map_normalize(self):
        return(["true" if ((pixel == 1) or (pixel is True)) else "false" for pixel in self.microbit_display_map])

    def microbit_display_map_as_string(self, list = None):
        if list is not None: self.set_list(list)

        return "/".join(self.microbit_display_map_normalize())

    @classmethod
    def microbit_empty_display_map(self):
        return([0] * 25)
