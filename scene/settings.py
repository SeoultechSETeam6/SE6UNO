import controller.game_data_controller

class Settings:
    def __init__(self):
        self.settings_data = controller.game_data_controller.load_settings_data()
        # self.resolution = settings_data["resolution"]
        # self.color_weakness = settings_data["color_weakness"]
        # self.key_setting = settings_data["key_setting"]
        # self.sound_volume = settings_data["volume"]["sound"]
        # self.background_volume = settings_data["volume"]["background"]
        # self.effect_volume = settings_data["volume"]["effect_volume"]

        # 화면 크기 설정
        if self.settings_data["resolution"]["height"] == 1920:
            self.font_size = font_size[0]
            self.button_size = button_size[0]
        elif self.settings_data["resolution"]["height"] == 1600:
            self.font_size = font_size[1]
            self.button_size = button_size[1]
        else:
            self.font_size = font_size[2]
            self.button_size = button_size[2]

