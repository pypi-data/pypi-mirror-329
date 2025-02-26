import requests
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Iden:
    def __init__(
        self,
        *,
        base_url: str,
        token: str,
        model_id: int,
        index_uuid: str,
    ):
        self.token = token
        self.base_url = base_url
        self.index_uuid = index_uuid
        self.model_id = model_id

    def chat(self, query: str):
        logger.info(
            f"Chatting with model_id: {self.model_id}, index: {self.index_uuid} and query: {query}"
        )
        response = requests.post(
            f"{self.base_url}/core/models/{self.model_id}/chat/",
            json={"query": query, "index_uuid": self.index_uuid},
            headers={"Authorization": f"Token {self.token}"},
        )
        if response.status_code != 200:
            logger.error(f"Failed to chat: {response.text}")
        else:
            logger.info("Chat successful")
        return response.json()
