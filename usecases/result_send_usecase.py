
import json
import time
import uuid
from config.config import RESULT_SOURCE_SDVX_HELPER
from models.settings import Settings
from repositories.api.i_websocket_client import IWebsocketClient
from usecases.i_result_send_usecase import IResultSendUsecase
from utils.common import safe_print
import xml.etree.ElementTree as ET

class ResultSendUsecase(IResultSendUsecase):
	def __init__(
		self, 
		websocket_client: IWebsocketClient
	):
		self.websocket_client = websocket_client

	def _generate_result_token(self) -> str:
		return str(uuid.uuid4()).replace("-", "") + str(int(time.time() * 1000))

	def execute(self, user_token: str, settings: Settings, content):
		result_data = None

		if settings.result_source == RESULT_SOURCE_SDVX_HELPER:
			root = ET.fromstring(content)
	
			level = root.findtext('lv')
			song_name = root.findtext('title')
			difficulty = root.findtext('difficulty').upper()
			first_result = root.find('Result')
			score = 0
			ex_score = 0
			if first_result is not None:
				score = first_result.findtext('score')

			result_data = {
				"mode": settings.mode,
				"roomId": settings.room_pass,
				"userId": user_token,
				"name": settings.djname,
				"resultToken": self._generate_result_token(),
				"result": {
					"level": level,
					"song_name": song_name,
					"difficulty": difficulty,
					"score": score,
					"ex_score": ex_score, #一旦EX SCOREは取れないので0
				}
			}

		if result_data is None:
			safe_print("送信データが無いため送信できません")
			return
		safe_print("[送信データ]")
		safe_print(json.dumps(result_data, ensure_ascii=False, indent=2))
		return self.websocket_client.send_with_retry(result_data)
