import os
from typing import List, Dict
from importlib import import_module
from ai_kit.core.llms.client import Client
import logging

logger = logging.getLogger(__name__)

class ClientFactory:
    clients = {
        "together": {
            "client": "ai_kit.core.llms.together_client.TogetherClient",
            "supported_models": {"r1": "deepseek-ai/Deepseek-R1"},
            "api_key": {
                "name": "TOGETHER_API_KEY",
                "url": "https://api.together.xyz/settings/api-keys",
            },
        },
        "groq": {
            "client": "ai_kit.core.llms.groq_client.GroqClient",
            "supported_models": {"r1-70b": "deepseek-r1-distill-llama-70b"},
            "api_key": {
                "name": "GROQ_API_KEY",
                "url": "https://console.groq.com/keys",
            },
        },
        "google": {
            "client": "ai_kit.core.llms.google_genai_client.GoogleGenAIClient",
            "supported_models": {"gemini-2.0-flash": "gemini-2.0-flash-exp"},
            "api_key": {
                "name": "GEMINI_API_KEY",
                "url": "https://makersuite.google.com/app/apikey",
            },
        },
        "cohere": {
            "client": "ai_kit.core.llms.cohere_client.CohereClient",
            "supported_models": {"rerank-v3.5": "rerank-v3.5"},
            "api_key": {
                "name": "COHERE_API_KEY",
                "url": "https://dashboard.cohere.com/api-keys",
            },
        },
        "perplexity": {
            "client": "ai_kit.core.llms.perplexity_client.PerplexityClient",
            "supported_models": ["sonar-pro", "sonar-reasoning-pro", "sonar-reasoning"],
            "api_key": {
                "name": "PERPLEXITY_API_KEY",
                "url": "https://www.perplexity.ai/settings/api",
            },
        },
        "openrouter": {
            "client": "ai_kit.core.llms.openrouter_client.OpenRouterClient",
            "supported_models": {
                "r1": "deepseek/deepseek-r1",
                "r1-70b": "deepseek/deepseek-r1-distill-llama-70b",
                "gemini-2.0-flash": "google/gemini-2.0-flash-001"
            },
            "api_key": {
                "name": "OPENROUTER_API_KEY",
                "url": "https://openrouter.ai/keys",
            },
        },
    }

    @staticmethod
    def _get_client_class(client_path: str):
        """
        Dynamically import and return the client class based on the fully qualified path.
        """
        logger.debug("Resolving client class for %s", client_path)
        module_path, class_name = client_path.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)

    @staticmethod
    def get_api_keys_and_urls() -> List[Dict[str, str]]:
        return [
            {
                "name": client["api_key"]["name"],
                "url": client["api_key"]["url"],
                "key": os.getenv(client["api_key"]["name"]),
            }
            for client in ClientFactory.clients.values() 
            if os.getenv(client["api_key"]["name"])
        ]

    @staticmethod
    def get_client_by_model(model: str) -> Client:
        # Gather all clients that support the specified model.
        supported_clients = [
            client for client in ClientFactory.clients.values()
            if model in client["supported_models"]
        ]

        # Select the first client that also has a valid API key.
        for client in supported_clients:
            api_key = os.getenv(client["api_key"]["name"])
            if api_key:
                client_cls = ClientFactory._get_client_class(client["client"])
                logger.debug(f"Client Factory returning {client_cls} for model {model}")
                model_var: str = client["supported_models"][model]
                return client_cls(model=model_var)

        raise ValueError(
            f"No API key found for any supported client for model: {model}"
        )
