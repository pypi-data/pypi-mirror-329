#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chat Model Module

This module defines the ChatModel class and associated classes for 
managing different LLM chat models. 
It utilizes the Factory Pattern to allow for flexible extraction methods 
based on the document type.
"""

from typing import Type, Dict, Any
from self_serve_platform.chat.models.langchain_chat_openai import (
    LangChainChatOpenAIModel)
from self_serve_platform.chat.models.langchain_azure_chat_openai import (
    LangChainAzureChatOpenAIModel)
from self_serve_platform.chat.models.langchain_chat_google_genai import (
    LangChainChatGoogleGenAIModel)
from self_serve_platform.chat.models.langchain_chat_anthropic import (
    LangChainChatAnthropicModel)
from self_serve_platform.chat.models.langchain_chat_mistralai import (
    LangChainChatMistralAIModel)
from self_serve_platform.chat.models.langchain_chat_nvidia import (
    LangChainChatNvidiaModel)
from self_serve_platform.chat.models.langchain_chat_vllm import (
    LangChainChatVLLMModel)
from self_serve_platform.chat.models.llamaindex_openai import (
    LlamaIndexOpenAIModel)


class ChatModel:  # pylint: disable=R0903
    """
    A chat model class that uses a factory pattern to return
    the selected chat model.
    """

    _models: Dict[str, Type] = {
        'LangChainChatOpenAI': LangChainChatOpenAIModel,
        'LangChainAzureChatOpenAI': LangChainAzureChatOpenAIModel,
        'LangChainChatGoogleGenAI': LangChainChatGoogleGenAIModel,
        'LangChainChatAnthropic': LangChainChatAnthropicModel,
        'LangChainChatMistralAI': LangChainChatMistralAIModel,
        'LangChainChatNvidia': LangChainChatNvidiaModel,
        'LangChainChatVLLM': LangChainChatVLLMModel,
        'LlamaIndexOpenAI': LlamaIndexOpenAIModel,
    }

    @staticmethod
    def create(config: dict) -> Any:
        """
        Return the appropriate Chat Model based on the provided configuration.

        :param config: Configuration dictionary containing the type of model.
        :return: An instance of the selected chat model.
        :raises ValueError: If 'type' is not in config or an unsupported type is provided.
        """
        model_type = config.get('type')
        if not model_type:
            raise ValueError("Configuration must include 'type'.")
        model_class = ChatModel._models.get(model_type)
        if not model_class:
            raise ValueError(f"Unsupported extractor type: {model_type}")
        return model_class(config)
