import os
import extensions
import constants

from buttons import Buttons


class Rocket:

    def __init__(self, row_spawn, column_spawn, rocet_frame):
        self.rows_direction = row_spawn
        self.columns_direction = column_spawn
        self.space_pressed = False
        self.rocet_frame = rocet_frame
        self.frame_height = 0
        self.frame_width = 0

    def rocket_controller(self, canvas):
        while True:
            pressed_key = canvas.getch()  # getkey()
            print(pressed_key)

            match pressed_key:
                case Buttons.UP_KEY:
                    self.rows_direction -= 1
                case Buttons.DOWN_KEY:
                    self.rows_direction += 1
                case Buttons.RIGHT_KEY:
                    self.columns_direction += 1
                case Buttons.LEFT_KEY:
                    self.columns_direction -= 1
                case Buttons.SPACE_KEY:
                    self.space_pressed = True
                case _:
                    break

            # Логика столкновений с границами игрового поля(Реализован через clamp)
            self.rows_direction = extensions.clamp(self.rows_direction, 0, constants.WINDOW_HEIGHT-self.frame_height-2)
            self.columns_direction = extensions.clamp(self.columns_direction, 1, constants.WINDOW_WIDTH-self.frame_width)

    def get_rocket_frame_size(self, rocket_frame):
        self.frame_height = len(rocket_frame)
        self.frame_width = max([len(line) for line in rocket_frame])


def get_rocket_frames(name_folder='rocket_frame'):
    rocet_frames = []
    file_names = os.listdir(name_folder)

    for file_name in file_names:
        path = os.path.join(name_folder, file_name)

        with open(path, "r") as file:
            rocet_frames.append(file.readlines())

    return rocet_frames
