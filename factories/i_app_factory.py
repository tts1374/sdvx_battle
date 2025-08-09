from abc import ABC, abstractmethod

from application.i_main_app_service import IMainAppSerivce
from controllers.i_main_view_controller import IMainViewController
from repositories.api.i_github_client import IGithubClient
from repositories.api.i_websocket_client import IWebsocketClient
from repositories.db.i_room_repository import IRoomRepository
from repositories.db.i_song_repository import ISongRepository
from repositories.db.i_song_result_repository import ISongResultRepository
from repositories.db.i_user_repository import IUserRepository
from repositories.files.i_output_file_repository import IOutputFileRepository
from repositories.files.i_settings_file_repository import ISettingsFileRepository
from repositories.system.i_screenshot_repository import IScreenshotRepository
from repositories.system.i_window_repository import IWindowRepository
from services.i_update_service import IUpdateService
from usecases.i_battle_result_handler import IBattleResultHandler
from usecases.i_delete_song_usecase import IDeleteSongUsecase
from usecases.i_result_send_usecase import IResultSendUsecase
from usecases.i_screenshot_usecase import IScreenshotUsecase
from usecases.i_skip_song_usecase import ISkipSongUsecase
from usecases.i_start_battle_usecase import IStartBattleUsecase

class IAppFactory(ABC):
    ################################
    ## SQL Session
    ################################
    @abstractmethod
    def create_session(self):
        pass

    ################################
    ## Repository
    ################################
    @abstractmethod
    def create_github_client(cls) -> IGithubClient:
        pass
    @abstractmethod
    def create_websocket_client(cls) -> IWebsocketClient:
        pass
    @abstractmethod
    def create_settings_file_repository(cls) -> ISettingsFileRepository:
        pass
    @abstractmethod
    def create_output_file_repository(cls) -> IOutputFileRepository:
        pass
    @abstractmethod
    def create_room_repository(cls, session) -> IRoomRepository:
        pass
    @abstractmethod
    def create_user_repository(cls, session) -> IUserRepository:
        pass
    @abstractmethod
    def create_song_repository(cls, session) -> ISongRepository:
        pass
    @abstractmethod
    def create_song_result_repository(cls, session) -> ISongResultRepository:
        pass
    @abstractmethod
    def create_screenshot_repository(cls) -> IScreenshotRepository:
        pass
    @abstractmethod
    def create_window_repository(cls) -> IWindowRepository:
        pass
    
    ################################
    ## Service
    ################################
    @abstractmethod
    def create_update_service(self) -> IUpdateService:
        pass
    
    ################################
    ## Usecase
    ################################
    @abstractmethod
    def create_battle_result_handler(cls) -> IBattleResultHandler:
        pass
    @abstractmethod
    def create_start_battle_usecase(cls) -> IStartBattleUsecase:
        pass
    @abstractmethod
    def create_result_send_usecase(cls) -> IResultSendUsecase:
        pass
    @abstractmethod
    def create_skip_song_usecase(cls) -> ISkipSongUsecase:
        pass
    @abstractmethod
    def create_delete_song_usecase(cls) -> IDeleteSongUsecase:
        pass
    @abstractmethod
    def create_screenshot_usecase(cls) -> IScreenshotUsecase:
        pass
        
    ################################
    ## Application
    ################################
    @abstractmethod
    def create_main_app_service(self) -> IMainAppSerivce:
        pass
    
    ################################
    ## Controller
    ################################
    @abstractmethod
    def create_main_view_controller(self, app) -> IMainViewController:
        pass