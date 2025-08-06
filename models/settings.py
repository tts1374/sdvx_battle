from dataclasses import dataclass
import os
import re
from typing import Optional

from config.config import BATTLE_MODE_TOTAL_SCORE_ARENA, BATTLE_MODE_TOTAL_SCORE_SINGLE, BATTLE_MODE_POINT_ARENA, BATTLE_MODE_POINT_SINGLE, RESULT_SOURCE_SDVX_HELPER

MUSICTABLE_VERSION = "1.1"

@dataclass
class Settings:
    djname: str = ""
    room_pass: str = ""
    mode: int = BATTLE_MODE_TOTAL_SCORE_ARENA
    user_num: int = 2
    result_source: int = RESULT_SOURCE_SDVX_HELPER
    result_dir: Optional[str] = None
    
    # リザルトファイル
    def get_result_file(self) -> str:
        if self.result_source == RESULT_SOURCE_SDVX_HELPER:
            return os.path.join(self.result_dir, "out", "history_cursong.xml")
        else:
            raise None
        
    def result_file_exists(self) -> bool:
        file_path = self.get_result_file()
        return os.path.isfile(file_path)
    
    def is_valid(self) -> bool:
        djname_ok = re.fullmatch(r'^[a-zA-Z0-9.\-\*&!?#$]{1,6}$', self.djname) is not None
        room_pass_ok = re.fullmatch(r'^[a-zA-Z0-9_-]{4,36}$', self.room_pass) is not None
        mode_ok = self.mode in [BATTLE_MODE_TOTAL_SCORE_ARENA, BATTLE_MODE_POINT_ARENA, BATTLE_MODE_TOTAL_SCORE_SINGLE, BATTLE_MODE_POINT_SINGLE]
        user_num_ok = (self.mode in [BATTLE_MODE_TOTAL_SCORE_SINGLE, BATTLE_MODE_POINT_SINGLE]) or (self.user_num != 0)
        result_source_ok = self.result_source in [RESULT_SOURCE_SDVX_HELPER]
        file_ok = self.result_dir is not None and self.result_file_exists()

        return djname_ok and room_pass_ok and mode_ok and user_num_ok and result_source_ok and file_ok