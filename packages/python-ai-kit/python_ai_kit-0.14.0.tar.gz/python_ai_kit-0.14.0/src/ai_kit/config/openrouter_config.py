class OpenRouterConfig:
    # ! Providers in order are case sensitive (updated 2/22/25)
    allowed_providers = [
        "OpenAI",
        "Anthropic",
        "Google",
        "Google AI Studio",
        "Amazon Bedrock",
        "Groq",
        "SambaNova",
        "Cohere",
        "Mistral",
        "Together",
        "Together 2",
        "Fireworks",
        "DeepInfra",
        "Lepton",
        "Novita",
        "Avian",
        "Lambda",
        "Azure",
        "Modal",
        "AnyScale",
        "Replicate",
        "Perplexity",
        "Recursal",
        "OctoAI",
        "DeepSeek",
        "Infermatic",
        "AI21",
        "Featherless",
        "Inflection",
        "xAI",
        "Cloudflare",
        "SF Compute",
        "Minimax",
        "Nineteen",
        "Liquid",
        "InferenceNet",
        "Friendli",
        "AionLabs",
        "Alibaba",
        "Nebius",
        "Chutes",
        "Kluster",
        "Crusoe",
        "Targon",
        "01.AI",
        "HuggingFace",
        "Mancer",
        "Mancer 2",
        "Hyperbolic",
        "Hyperbolic 2",
        "Lynn 2",
        "Lynn",
        "Reflection",
    ]

    config = {
        "chat": {},
        "reasoning": {
            "deepseek/deepseek-r1": {
                "include_reasoning": True,
                "provider": {
                    "order": ["Together"],
                    "allow_fallbacks": False,
                },
                "clients": ["together", "openrouter"],
            },
            "deepseek/deepseek-r1-distill-llama-70b": {
                "include_reasoning": True,
                "provider": {
                    "order": ["Groq"],
                    "allow_fallbacks": False,
                },
                "clients": [
                    "groq",
                    "openrouter",
                ],
            },
        },
        "structured_output": {
            "google/gemini-2.0-flash-001": {
                "provider": {
                    "order": ["Google"],
                    "allow_fallbacks": False,
                },
                "clients": [
                    "google",
                    "openrouter",
                ],
            },
        },
    }

    # Validate providers at class definition time
    for type_ in config.values():
        for model in type_.values():
            for provider in model["provider"]["order"]:
                if provider not in allowed_providers:
                    raise ValueError(
                        f"Invalid provider: {provider}. Supported providers are: {', '.join(allowed_providers)}."
                    )

    @staticmethod
    def get_config():
        return OpenRouterConfig.config

    @staticmethod
    def get_model_config(model: str):
        # Check each model type's config
        for model_type, models in OpenRouterConfig.config.items():
            if model in models:
                return models[model]

        # If model not found, create a list of all supported models
        all_models = []
        for models in OpenRouterConfig.config.values():
            all_models.extend(models.keys())

        raise ValueError(
            f"Invalid model: {model}. Supported models are: {', '.join(all_models)}."
        )

    @staticmethod
    def validate_model_type(model: str, model_type: str):
        if model_type not in OpenRouterConfig.config:
            raise ValueError(
                f"Invalid model type: {model_type}. Supported model types are: {', '.join(OpenRouterConfig.config.keys())}."
            )
        if model not in OpenRouterConfig.config[model_type]:
            raise ValueError(
                f"Invalid model: {model}. Supported models for {model_type} are: {', '.join(OpenRouterConfig.config[model_type].keys())}."
            )

