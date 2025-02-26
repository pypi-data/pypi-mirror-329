import json

import vertexai
from google.cloud import aiplatform
from google.oauth2 import service_account
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI

from src.infra.config.constants import Constants


def main():
    file = Constants.AUTH_PATH
    with open(file) as f:
        service_info = json.load(f)

    my_credentials = service_account.Credentials.from_service_account_info(service_info)

    aiplatform.init(
        credentials=my_credentials,
    )

    with open(file, encoding="utf-8") as f:
        project_json = json.load(f)
        project_id = project_json["project_id"]

    vertexai.init(project=project_id, location="us-central1")
    parameters = {
        "temperature": 0.8,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }

    chat = ChatVertexAI(model_name="gemini-pro", parameters=parameters)

    prompt = "Você é um agente de IA responderá rapidamente essa questão: {question}"

    template = ChatPromptTemplate.from_template(prompt)

    output = StrOutputParser()

    chain = template | chat | output

    response = chain.invoke({"question": "Qual é a capital do Brasil?"})
    print(response)


if __name__ == "__main__":
    main()
