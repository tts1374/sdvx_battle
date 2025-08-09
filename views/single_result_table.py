import flet as ft
from config.config import BATTLE_MODE_POINT_SINGLE, BATTLE_RULE_NORMAL, BATTLE_RULE_POINT
from utils.common import has_rule_in_mode

# 難易度色マッピング
DIFFICULTY_COLOR_MAP = {
    "NOV": "#aaaaff",
    "ADV": "#ffffaa",
    "EXH": "#ffaaaa",
    "APPEND": "#ffccff",
}
TITLE_NAME_COLOR = ft.Colors.WHITE
MAIN_COLOR = "#EEEEEE"
SONG_ICON_COLOR = ft.Colors.WHITE
class SingleResultTable:
    def __init__(self, page: ft.Page, result_data: dict, on_skip_callback, on_delete_callback, setting_visible:bool, is_enable_operation:bool):
        super().__init__()
        self.page = page
        self.result_data = result_data
        self.on_skip_callback = on_skip_callback
        self.on_delete_callback = on_delete_callback
        self.setting_visible = setting_visible
        self.is_enable_operation = is_enable_operation
        
    # header生成
    def _build_header(self) -> ft.Row:
        # 最大2人想定。いなければ空白。
        user_colors = ["#639bff", "#ff4841"]
        user_names = [u.get("user_name", "") for u in self.result_data.get("users", [])]

        # 必ず2要素に調整（1人以下でも空白を補完）
        while len(user_names) < 2:
            user_names.append("")

        name_boxes = [
            self._user_name_box(user_names[i], user_colors[i])
            for i in range(2)
        ]

        return ft.Row(name_boxes, opacity=0.95, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # user名出力
    def _user_name_box(self, name: str, bgcolor: str) -> ft.Container:
            return ft.Container(
                content=ft.Text(name, size=28, color=TITLE_NAME_COLOR, weight=ft.FontWeight.BOLD),
                bgcolor=bgcolor,
                alignment=ft.alignment.center,
                expand=True,
                padding=5
            )
    # ユーザスコア出力
    def _user_score(self, result: dict | None, mode: int, is_left: bool) -> ft.Row:
        label = "SCORE" if has_rule_in_mode(mode, BATTLE_RULE_NORMAL) else "EX SCORE"
        if result:
            value = result["score"] if has_rule_in_mode(mode, BATTLE_RULE_NORMAL) else result["ex_score"]
            if has_rule_in_mode(mode, BATTLE_RULE_POINT):
                highlight = result.get("pt", 0) > 0
            else:
                highlight = False
        else:
            value = "-"
            highlight = False

        icon_size = 40
        icon_path = "icon.ico"

        margin_icon = ft.margin.only(right=50) if is_left else ft.margin.only(left=50)
        margin_score = ft.margin.only(right=100) if is_left else ft.margin.only(left=100)

        icon_container = ft.Container(
            content=ft.Image(
                src=icon_path,
                width=icon_size,
                height=icon_size,
                visible=highlight
            ),
            width=icon_size,
            height=icon_size,
            margin=margin_icon,
            alignment=ft.alignment.center
        )

        score_column = ft.Container(
            content=ft.Column([
                    ft.Text(label, size=10, color=MAIN_COLOR),
                    ft.Text(
                        str(value),
                        size=28,
                        color="#fab27b" if highlight else MAIN_COLOR,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            margin=margin_score
        )
        
        spacer = ft.Container(expand=True)

        # アイコンの位置に応じて並べる
        if is_left:
            return ft.Row(
                controls=[spacer, icon_container, score_column],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        else:
            return ft.Row(
                controls=[score_column, icon_container, spacer],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )


    # 曲情報
    def _song_info(self, song: dict) -> ft.Column:
        stage_no = song.get("stage_no", 1)
        stage_suffix = {1: "ST", 2: "ND", 3: "RD"}.get(stage_no if stage_no < 20 else stage_no % 10, "TH")
        stage_label = f"{stage_no}{stage_suffix} TRACK"

        title = song.get("song_name", "")
        difficulty = song.get("difficulty", "")
        level = song.get("level", "")
        difficulty_color = DIFFICULTY_COLOR_MAP.get(difficulty.upper(), MAIN_COLOR)

        return ft.Column([
            ft.Text(stage_label, size=10, color=MAIN_COLOR),
            ft.Text(title, size=18, color=MAIN_COLOR, no_wrap=True),
            ft.Row([
                ft.Text(f"{difficulty} {level}", color=difficulty_color)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _make_button(self, song_id, is_deletable):
        return ft.ElevatedButton(
            text="削除" if is_deletable else "スキップ",
            icon=ft.Icons.DELETE if is_deletable else ft.Icons.SKIP_NEXT,
            on_click=lambda e: self.page.run_task(
                self.on_delete_callback if is_deletable else self.on_skip_callback,
                song_id
            ),
            style=ft.ButtonStyle(
                bgcolor="transparent",
                overlay_color="transparent",
                shadow_color="transparent",
                color=ft.Colors.RED if is_deletable else ft.Colors.BLUE
            )
        )
    # リザルトの各曲行（最大4件）
    def _build_song_rows(self) -> list[ft.Container]:
        mode = self.result_data.get("mode", BATTLE_MODE_POINT_SINGLE)
        users = self.result_data.get("users", [])
        user_ids = [u["user_id"] for u in users] + [None] * (2 - len(users))
        user_ids = user_ids[:2]  # 常に2人

        rows = []
        
        for song in sorted(self.result_data.get("songs", []), key=lambda s: s.get("stage_no", 0), reverse=True):
            results = song.get("results", [])

            result_user0 = next((r for r in results if r["user_id"] == user_ids[0]), None) if user_ids[0] else None
            result_user1 = next((r for r in results if r["user_id"] == user_ids[1]), None) if user_ids[1] else None

            button_overlay = ft.Ref[ft.Container]()

            def create_hover_handlers(overlay_ref):
                def on_enter(e):
                    if self.setting_visible or not self.is_enable_operation:
                        return
                    overlay_ref.current.opacity = 0.9
                    overlay_ref.current.bgcolor = ft.Colors.WHITE
                    overlay_ref.current.update()

                def on_exit(e):
                    if self.setting_visible or not self.is_enable_operation:
                        return
                    overlay_ref.current.opacity = 0.0
                    overlay_ref.current.bgcolor = "transparent"
                    overlay_ref.current.update()

                return on_enter, on_exit

            on_enter, on_exit = create_hover_handlers(button_overlay)

            # ボタンの内容を切り替え
            button = self._make_button(song["song_id"], result_user0 is not None)
            # GestureDetector を Stack の外に出す
            row = ft.GestureDetector(
                on_enter=on_enter,
                on_exit=on_exit,
                content=ft.Stack(
                    controls=[
                        # 背景＋スコア
                        ft.Container(
                            content=ft.Row([
                                self._user_score(result_user0, mode, is_left=True),
                                ft.Container(
                                    content=self._song_info(song),
                                    width=375,
                                    alignment=ft.alignment.center
                                ),
                                self._user_score(result_user1, mode, is_left=False),
                            ]),
                            bgcolor="#4B4B4B",
                            padding=10,
                            border_radius=5,
                            width=1200,
                            height=100
                        ),
                        # ボタン領域
                        ft.Container(
                            ref=button_overlay,
                            content=ft.Row([
                                ft.Container(
                                    content=button,
                                    width=1200,
                                    alignment=ft.alignment.center
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            padding=10,
                            width=1200,
                            height=100,
                            opacity=0.0,
                            bgcolor="transparent",  # 初期透明
                            animate_opacity=300
                        )
                    ]
                )
            )


            rows.append(row)

        # スクロール可能な領域に song_rows を配置
        return ft.Container(
            height=320 if self.setting_visible else 620,  
            content=ft.Column(
                controls=rows,
                scroll="auto",
                spacing=10
            )
        )
    
    # 合計スコア算出
    def _get_total_pt(self, user_index: int) -> int:
        if len(self.result_data["users"]) > user_index:
            user_id = self.result_data["users"][user_index]["user_id"]
            total = 0
            for song in self.result_data["songs"]:
                matched = next(
                    (r for r in song["results"] if r["user_id"] == user_id), None
                )
                total += matched["pt"] if matched else 0
            return total
        return 0
    
    def _build_total_row(self) -> ft.Row:
        user1_total_score = self._get_total_pt(0)
        user2_total_score = self._get_total_pt(1)
        user1_highlight = user1_total_score >= user2_total_score
        user2_highlight = user2_total_score >= user1_total_score
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("TOTAL", size=10, color=MAIN_COLOR),
                    ft.Text(str(user1_total_score), size=24, color="#fab27b" if user1_highlight else MAIN_COLOR)
                ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                ft.Column([
                    ft.Text("TOTAL", size=10, color=MAIN_COLOR),
                    ft.Text(str(user2_total_score), size=24, color="#fab27b" if user2_highlight else MAIN_COLOR)
                ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            ]),
            bgcolor="#4B4B4B",
            padding=10,
            border_radius=5
        )
    def build(self):
        # ヘッダー（プレイヤー名）
        header = self._build_header()

        # リザルト1つ目
        song_rows = self._build_song_rows()
        
        # 合計スコア
        total_row = self._build_total_row()

        return ft.Column(
            controls=[header, song_rows, total_row],
            spacing=10,
            width=1200,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )