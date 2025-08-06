import json
import os
from config.config import BATTLE_MODE_TOTAL_SCORE_ARENA, RESULT_SOURCE_SDVX_HELPER
from models.settings import Settings
from repositories.files.i_settings_file_repository import ISettingsFileRepository

class SettingsFileRepository(ISettingsFileRepository):
    SETTINGS_PATH = "settings.json"

    def save(self, settings: Settings):
        with open(self.SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings.__dict__, f, ensure_ascii=False, indent=4)
            
    def load(self) -> Settings:
        if not os.path.exists(self.SETTINGS_PATH):
            return Settings()

        with open(self.SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Settings(
            djname=data.get("djname", ""),
            room_pass=data.get("room_pass", ""),
            mode=data.get("mode", BATTLE_MODE_TOTAL_SCORE_ARENA),
            result_source=data.get("result_source", RESULT_SOURCE_SDVX_HELPER),
            user_num=data.get("user_num", "2"),
            result_dir=data.get("result_dir")
        )