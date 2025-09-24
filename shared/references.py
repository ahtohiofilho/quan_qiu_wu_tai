class Referencias:
    def __init__(self):
        self.culturas = [
            'English', 'Chinese', 'Spanish',
            'French', 'Indian', 'Russian',
            'Vietnamese', 'Turkish', 'Arabic',
            'Indonesian', 'Persian', 'Hausa',
            'Swahili', 'Portuguese', 'Telugu',
            'Bengali', 'Japanese', 'Marathi',
            'Wu', 'Yue', 'Min',
            'Korean', 'Italian', 'German'
        ]
        self.civs_cores = {
            'Midnight Blue': (0, 0, 127), 'Blue': (0, 0, 255),
            'Dark Green': (0, 127, 0), 'Teal': (0, 127, 127), 'Sky Blue': (32, 127, 223),
            'Green': (0, 255, 0), 'Spring Green': (0, 255, 127), 'Cyan': (0, 223, 223),
            'Maroon': (127, 0, 0), 'Purple': (127, 0, 127), 'Violet': (127, 0, 255),
            'Olive': (127, 127, 0), 'Lavender': (127, 127, 255),
            'Chartreuse': (127, 255, 0), 'Light Green': (127, 223, 127), 'Pale Cyan': (127, 255, 255),
            'Red': (234, 33, 37), 'Rose': (255, 0, 127), 'Magenta': (255, 0, 255),
            'Orange': (223, 127, 32), 'Salmon': (255, 127, 127), 'Orchid': (255, 127, 255),
            'Yellow': (255, 255, 0), 'Light Yellow': (255, 255, 127)
        }

        self.tons_de_pele = [(245, 212, 205), (212, 160, 147), (163, 106, 95), (101, 61, 53)]
        self.tons_de_cabelo = [(209, 195, 2), (140, 106, 0), (99, 55, 26), (52, 48, 47)]

        self.produtividade_base = {
            'Meadow':     6.0,
            'Forest':     5.0,
            'Hills':      4.0,
            'Savanna':    3.0,
            'Coast':      3.0,
            'Desert':     2.0,
            'Sea':        2.0,
            'Mountains':  1.0,
            'Ocean':      1.0,
            'Ice':        0.0
        }

        self.overlay_paths = {
            "hex_up": {
                "center": "assets/hover/hexagon/up/center.png",
                "left": "assets/hover/hexagon/up/left.png",
                "right": "assets/hover/hexagon/up/right.png",
                "topleft": "assets/hover/hexagon/up/topleft.png",
                "topright": "assets/hover/hexagon/up/topright.png",
                "bottomleft": "assets/hover/hexagon/up/bottomleft.png",
                "bottomright": "assets/hover/hexagon/up/bottomright.png",
            },
            "hex_side": {
                "center": "assets/hover/hexagon/side/center.png",
                "top": "assets/hover/hexagon/side/top.png",
                "bottom": "assets/hover/hexagon/side/bottom.png",
                "topleft": "assets/hover/hexagon/side/topleft.png",
                "topright": "assets/hover/hexagon/side/topright.png",
                "bottomleft": "assets/hover/hexagon/side/bottomleft.png",
                "bottomright": "assets/hover/hexagon/side/bottomright.png",
            },
            "pent_up": {
                "center": "assets/hover/pentagon/up/center.png",
                "topleft": "assets/hover/pentagon/up/topleft.png",
                "topright": "assets/hover/pentagon/up/topright.png",
                "bottom": "assets/hover/pentagon/up/bottom.png",
                "bottomleft": "assets/hover/pentagon/up/bottomleft.png",
                "bottomright": "assets/hover/pentagon/up/bottomright.png",
            },
            "pent_down": {
                "center": "assets/hover/pentagon/down/center.png",
                "top": "assets/hover/pentagon/down/top.png",
                "topleft": "assets/hover/pentagon/down/topleft.png",
                "topright": "assets/hover/pentagon/down/topright.png",
                "bottomleft": "assets/hover/pentagon/down/bottomleft.png",
                "bottomright": "assets/hover/pentagon/down/bottomright.png",
            }
        }
