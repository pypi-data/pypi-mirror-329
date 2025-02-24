from enum import Enum


class LLMClients(str, Enum):
    ollama = "ollama"
    openai = "openai"


class EmbeddingsClients(str, Enum):
    openai = "openai"
    ollama = "ollama"

class ModelType(str, Enum):
    base = "base"
    instruct = "instruct"
    
class AzureSearchMode(str, Enum):
    TEXT = 'text'
    VECTOR = 'vector'
    HYBRID = 'hybrid'
    SEMANTIC = 'semantic'
    HYBRID_SEMANTIC = 'hybrid_semantic'    
    
    
class SaveMethod(str, Enum):
    ADAPTERS = "adapters"
    FULL = "full"