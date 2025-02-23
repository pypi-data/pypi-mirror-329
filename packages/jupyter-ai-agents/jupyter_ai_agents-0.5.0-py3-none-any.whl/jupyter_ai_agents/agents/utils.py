# Copyright (c) 2023-2024 Datalayer, Inc.
#
# BSD 3-Clause License

from jupyter_ai_agents.providers.azure_openai import create_azure_openai_agent
from jupyter_ai_agents.providers.github_copilot import create_github_copilot_agent

def create_ai_agent(model_provider: str, model_name: str, system_prompt_final: str, tools: list):
    """Create an AI agent based on the model provider."""
    if model_provider == "azure-openai": 
        agent = create_azure_openai_agent(model_name, system_prompt_final, tools)
    elif model_provider == "github-copilot":
        agent = create_github_copilot_agent(model_name, system_prompt_final, tools)
    else:
        raise ValueError(f"Model provider {model_provider} is not supported.")
    return agent