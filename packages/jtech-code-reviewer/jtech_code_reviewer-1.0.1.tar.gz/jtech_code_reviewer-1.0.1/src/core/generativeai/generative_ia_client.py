from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# from src.core.generativeai.jtech_vertexai import JtechChatVertexAI


class GenerativeAIClient:
    """
    A client class for interacting with a generative AI model.

    Attributes:
        llm (ChatGoogleGenerativeAI): The generative AI model instance.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.0) -> None:
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        # self.llm = JtechChatVertexAI().chat

    def get_response(self, prompt_template: ChatPromptTemplate, **kwargs) -> str:
        """
        Gets a response from the generative AI model using the given prompt template.

        Args:
            prompt_template (ChatPromptTemplate): The prompt template to use for generating a response.
            **kwargs: Additional keyword arguments to pass to the generative AI model.

        Returns:
            str: The generated response from the generative AI model.
        """
        chain = prompt_template | self.llm | StrOutputParser()
        return chain.invoke(kwargs)
