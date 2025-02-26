import json

import vertexai
from google.cloud import aiplatform
from google.oauth2 import service_account
from langchain_google_vertexai import ChatVertexAI

from src.infra.config.constants import Constants


class JtechChatVertexAI:
    def __init__(self, temperature: float = 0.0, model_name: str = "gemini-pro") -> None:
        self._credentials()
        self._init_vertextai()
        self.model_name = model_name
        self.parameters = {
            "temperature": temperature,
        }
        self.chat = ChatVertexAI(model_name=self.model_name, parameters=self.parameters)

    def _credentials(self):
        file = Constants.AUTH_PATH
        with open(file) as f:
            service_info = json.load(f)
        my_credentials = service_account.Credentials.from_service_account_info(service_info)
        aiplatform.init(
            credentials=my_credentials,
        )

    def _init_vertextai(self):
        with open(Constants.AUTH_PATH, encoding="utf-8") as f:
            project_json = json.load(f)
            project_id = project_json["project_id"]
            project_location = "us-central1"

        vertexai.init(project=project_id, location=project_location)
