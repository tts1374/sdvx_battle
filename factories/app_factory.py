from application.main_app_service import MainAppService
from controllers.main_view_controller import MainViewController
from db.database import SessionLocal
from factories.i_app_factory import IAppFactory
from repositories.api.github_client import GithubClient
from repositories.api.websocket_client import WebsocketClient
from repositories.db.room_repository import RoomRepository
from repositories.db.song_repository import SongRepository
from repositories.db.song_result_repository import SongResultRepository
from repositories.db.user_repository import UserRepository
from repositories.files.output_file_repository import OutputFileRepository
from repositories.files.settings_file_repository import SettingsFileRepository
from repositories.system.screenshot_repository import ScreenshotRepository
from repositories.system.window_repository import WindowRepository
from usecases.battle_result_handler import BattleResultHandler
from services.update_service import UpdateService
from usecases.delete_song_usecase import DeleteSongUsecase
from usecases.result_send_usecase import ResultSendUsecase
from usecases.screenshot_usecase import ScreenshotUsecase
from usecases.skip_song_usecase import SkipSongUsecase
from usecases.start_battle_usecase import StartBattleUsecase


class AppFactory(IAppFactory):
    _websocket_client = None
     
    ################################
    ## SQL Session
    ################################
    @classmethod
    def create_session(cls):
        return SessionLocal()
    
    ################################
    ## Repository
    ################################
    @classmethod
    def create_github_client(cls):
        return GithubClient()
    @classmethod
    def create_websocket_client(cls):
        if cls._websocket_client is None:
            cls._websocket_client = WebsocketClient()
        return cls._websocket_client
    @classmethod
    def create_settings_file_repository(cls):
        return SettingsFileRepository()
    @classmethod
    def create_output_file_repository(cls):
        return OutputFileRepository()
    @classmethod
    def create_room_repository(cls, session):
        return RoomRepository(session)
    @classmethod
    def create_user_repository(cls, session):
        return UserRepository(session)
    @classmethod
    def create_song_repository(cls, session):
        return SongRepository(session)
    @classmethod
    def create_song_result_repository(cls, session):
        return SongResultRepository(session)
    @classmethod
    def create_screenshot_repository(cls):
        return ScreenshotRepository()
    @classmethod
    def create_window_repository(cls):
        return WindowRepository()
    
    
    ################################
    ## Service
    ################################
    @classmethod
    def create_update_service(cls):
        github_client = cls.create_github_client()
        return UpdateService(github_client)

    ################################
    ## Usecase
    ################################
    @classmethod
    def create_battle_result_handler(cls):
        session = cls.create_session()
        output_file_repository = cls.create_output_file_repository()
        room_repository = cls.create_room_repository(session)
        user_repository = cls.create_user_repository(session)
        song_repository = cls.create_song_repository(session)
        song_result_repository = cls.create_song_result_repository(session)
        return BattleResultHandler(
            output_file_repository=output_file_repository,
            session=session,
            room_repository=room_repository,
            user_repository=user_repository,
            song_repository=song_repository,
            song_result_repository=song_result_repository
        )
        
    @classmethod
    def create_start_battle_usecase(cls):
        session = cls.create_session()
        settings_file_repository = cls.create_settings_file_repository()
        output_file_repository = cls.create_output_file_repository()
        room_repository = cls.create_room_repository(session)
        user_repository = cls.create_user_repository(session)
        websocket_client = cls.create_websocket_client()
        battle_result_handler = cls.create_battle_result_handler()
        return StartBattleUsecase(
            settings_file_repository=settings_file_repository, 
            output_file_repository=output_file_repository,
            session=session, 
            room_repository=room_repository, 
            user_repository=user_repository, 
            websocket_clinet=websocket_client,
            battle_result_handler=battle_result_handler
        )
    @classmethod
    def create_result_send_usecase(cls):
        session = cls.create_session()
        websocket_client = cls.create_websocket_client()
        return ResultSendUsecase(websocket_client)
    @classmethod
    def create_skip_song_usecase(cls):
        session = cls.create_session()
        websocket_client = cls.create_websocket_client()
        room_repository = cls.create_room_repository(session)
        song_repository = cls.create_song_repository(session)
        return SkipSongUsecase(room_repository, song_repository, websocket_client)
    
    @classmethod
    def create_delete_song_usecase(cls):
        session = cls.create_session()
        websocket_client = cls.create_websocket_client()
        room_repository = cls.create_room_repository(session)
        user_repository = cls.create_user_repository(session)
        song_result_repository = cls.create_song_result_repository(session)
        return DeleteSongUsecase(room_repository, user_repository, song_result_repository, websocket_client)
    
    @classmethod
    def create_screenshot_usecase(cls):
        window_repository = cls.create_window_repository()
        screenshot_repository = cls.create_screenshot_repository()
        
        return ScreenshotUsecase(window_repository, screenshot_repository)

    ################################
    ## Application
    ################################
    @classmethod
    def create_main_app_service(cls):
        start_battle_usecase = cls.create_start_battle_usecase()
        result_send_usecase = cls.create_result_send_usecase()
        skip_song_usecase = cls.create_skip_song_usecase()
        delete_song_usecase = cls.create_delete_song_usecase()
        screenshot_usecase = cls.create_screenshot_usecase()
        update_service = cls.create_update_service()
        settings_file_repository = cls.create_settings_file_repository()
        output_file_repository = cls.create_output_file_repository()
        websocket_client = cls.create_websocket_client()
        return MainAppService(
            start_battle_usecase=start_battle_usecase,             
            result_send_usecase=result_send_usecase, 
            skip_song_usecase=skip_song_usecase,
            delete_song_usecase=delete_song_usecase, 
            screenshot_usecase=screenshot_usecase,
            update_service=update_service,
            settings_file_repository=settings_file_repository,
            output_file_repository=output_file_repository,
            websocket_client=websocket_client
        )

    ################################
    ## Controller
    ################################
    @classmethod
    def create_main_view_controller(cls, app):
        app_controller = cls.create_main_app_service()
        return MainViewController(app, app_controller)