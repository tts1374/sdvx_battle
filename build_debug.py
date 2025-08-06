import os
import re
import subprocess
import shutil

from utils.common import safe_print

CONFIG_FILE = "./config/config.py"
output_dir = "dist/SDVX_Battle"

def set_release_mode(is_release=True):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # IS_RELEASE の部分を書き換え
    new_content = re.sub(r"IS_RELEASE\s*=\s*(True|False)", f"IS_RELEASE = {str(is_release)}", content)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    safe_print(f"[Success] config.py を {'リリース' if is_release else '開発'}モードに設定しました。")

def clean():
    """過去のビルドファイル削除"""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

def build():
    # ---- mainのビルド -----
    cmd = [
        "flet",
        "pack",
        "-y",  # 対話なし
        "-n", "SDVX_Battle",  # exe名指定
        "--distpath", output_dir,          # 出力先指定
        "--icon", "icon.ico",      # アイコン
        "main.py",                        # メインスクリプト
        "--hidden-import", "logging.config",
        "--add-data", "alembic.ini;.",
        "--add-data", "alembic;alembic",
    ]
    safe_print("SDVX_Battle.exe のビルドを開始します...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        safe_print("ビルド失敗しました。詳細ログ：")
        safe_print(result.stdout)
        safe_print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, cmd)
    
    # exe出力後に独立ファイルをコピー
    shutil.copy("sdvx_battle.html", os.path.join(output_dir, "sdvx_battle.html"))
    shutil.copy("sdvx_battle_style.css", os.path.join(output_dir, "sdvx_battle_style.css"))
    shutil.copy("sdvx_battle_script.js", os.path.join(output_dir, "sdvx_battle_script.js"))
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    shutil.copy("images/icon.png", os.path.join(images_dir, "icon.png"))
    shutil.copy("icon.ico", os.path.join(output_dir, "icon.ico"))
    shutil.copy("README.md", os.path.join(output_dir, "README.md"))
    safe_print("SDVX_Battle.exe のビルド完了。")
    
    # ----- updaterのビルド -----
    updater_output_dir = os.path.join(output_dir, "updater")
    os.makedirs(updater_output_dir, exist_ok=True)

    updater_cmd = [
        "flet",
        "pack",
        "-y",
        "-n", "updater",
        "--distpath", updater_output_dir,
        "updater.py",
    ]
    safe_print("updater.exe のビルドを開始します...")
    result = subprocess.run(updater_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        safe_print("updater ビルド失敗しました。詳細ログ：")
        safe_print(result.stdout)
        safe_print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, updater_cmd)

    # updater.exe をメイン実行ファイルと同じ場所にコピー
    shutil.copy(os.path.join(updater_output_dir, "updater.exe"), os.path.join(output_dir, "updater.exe"))

    # 不要になったupdaterフォルダを削除
    shutil.rmtree(updater_output_dir)
    
    safe_print("updater.exe のビルド完了。")
    safe_print(f"ビルドが完了しました。{output_dir} に出力されています。")

if __name__ == "__main__":
    try:
        # ① デバッグモードに設定
        set_release_mode(False)

        # ② クリーンアップ＆ビルド実行
        clean()
        build()

    finally:
        pass
