import logging

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from naima_lab.models.enums import LLMClients, EmbeddingsClients
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings



class InterfaceLangChain:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def get_chat_llm(self, client: LLMClients = LLMClients.ollama, 
                model: str = "llama3.2:1b",
                max_tokens: int = 4096, 
                temperature: float = 0,
                seed: int = 42,
                **args) -> ChatOpenAI | OllamaLLM:
        if client == LLMClients.ollama:
            llm = OllamaLLM(
                model=model,
                num_predict=max_tokens,
                temperature=temperature,
                seed=seed,
                **args
            )
        elif client == LLMClients.openai:
            llm = ChatOpenAI(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                seed=seed,
                **args
            )
        else:
            raise Exception("The client is not permitted.")
        
        return llm

    @classmethod
    def get_embeddings(self, client: EmbeddingsClients = EmbeddingsClients.ollama, 
                       model: str = "nomic-embed-text:latest",
                    **args) -> OpenAIEmbeddings | OllamaEmbeddings:
        if client == EmbeddingsClients.openai:
            embeddings = OpenAIEmbeddings(
                model=model,
                **args
            )
        elif client == EmbeddingsClients.ollama:
            embeddings = OllamaEmbeddings(
                model=model,
                **args
            )
        else:
            raise Exception("The client is not permitted.")            
        return embeddings