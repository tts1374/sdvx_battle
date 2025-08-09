from datetime import datetime
import sys
import os
import io

from config.config import BATTLE_MODE, IS_RELEASE

def now_str():
    return datetime.now().isoformat()

def resource_path(relative_path):
    """PyInstaller実行時と通常実行時のパス切り替え"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.getcwd(), relative_path)

def get_log_dir():
    if getattr(sys, 'frozen', False):
        # PyInstaller実行時
        return os.path.dirname(sys.executable)
    else:
        # 通常のPython実行時
        return os.path.dirname(os.path.abspath(__file__))

def safe_print(*args, **kwargs):
    try:
        if not IS_RELEASE:
            # ログファイルに出力（開発時のみ）
            log_dir = get_log_dir()
            log_path = os.path.join(log_dir, "debug.log")
            with open(log_path, "a", encoding="utf-8") as f:
                print(now_str(), *args, **kwargs, file=f)

            # 開発時はコンソールにも出力
            if not getattr(sys, 'frozen', False):
                if sys.stdout and sys.stdout.isatty():
                    print(now_str(), *args, **kwargs)

    except (io.UnsupportedOperation, AttributeError, PermissionError):
        pass

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
    
# モードがルールを持っているかどうか
def has_rule_in_mode(mode: int, rule: str) -> bool:
    for battle_mode in BATTLE_MODE:
        if battle_mode["value"] == mode:
            return rule in battle_mode["rule"]
    return False  # 指定のmodeが存在しない場合はFalse
