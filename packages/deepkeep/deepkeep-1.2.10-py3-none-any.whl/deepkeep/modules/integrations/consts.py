from enum import Enum


class IntegrationsType(Enum):
    Azure_OpenAI = "Azure_OpenAI"
    OpenAI = "OpenAI"
    Bedrock = "Bedrock"
    Gemini = "Gemini"
    # Add more integrations - when ready
