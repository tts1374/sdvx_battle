APP_VERSION = "v0.2.1"
IS_RELEASE = False
DB_FILE = "result.db"
ZIP_NAME = "SDVX_Battle.zip"

# 対戦モード
BATTLE_MODE_TOTAL_SCORE_ARENA = 1
BATTLE_MODE_POINT_ARENA = 2
BATTLE_MODE_TOTAL_SCORE_SINGLE = 3
BATTLE_MODE_POINT_SINGLE = 4
BATTLE_MODE = [
    {"name": "ARENA スコア制", "value": BATTLE_MODE_TOTAL_SCORE_ARENA},
    {"name": "ARENA ポイント制", "value": BATTLE_MODE_POINT_ARENA},
    {"name": "SINGLE スコア制", "value": BATTLE_MODE_TOTAL_SCORE_SINGLE},
    {"name": "SINGLE ポイント制", "value": BATTLE_MODE_POINT_SINGLE},
]

# リザルト取得手段
RESULT_SOURCE_SDVX_HELPER = 1

# Websocket操作
OPERATION_REGISTER = "register"
OPERATION_DELETE = "delete"

# WebsocketURL
if IS_RELEASE:
    WEBSOCKET_URL = "wss://lnlfhmnve3.execute-api.ap-northeast-1.amazonaws.com/api"
else:
    WEBSOCKET_URL = "wss://a2vvmgf2t9.execute-api.ap-northeast-1.amazonaws.com/api"