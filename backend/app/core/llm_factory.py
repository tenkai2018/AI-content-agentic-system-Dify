"""
LLM Factory — Trả về đúng LLM instance theo provider và role.

Cách dùng:
    from app.core.llm_factory import get_llm
    llm = get_llm(role="reasoning")   # → GPT-4o hoặc Ollama reasoning model
    llm = get_llm(role="writing")     # → Claude 3.5 hoặc Ollama writing model
    llm = get_llm(role="vision")      # → GPT-4o Vision (không có Ollama fallback tốt bằng)

Provider được chọn qua biến môi trường LLM_PROVIDER:
    LLM_PROVIDER="openai"    → dùng OpenAI + Anthropic (cloud)
    LLM_PROVIDER="anthropic" → dùng Anthropic cho writing, OpenAI cho reasoning
    LLM_PROVIDER="ollama"    → dùng Ollama local cho tất cả (trừ vision nếu không có llava)
    LLM_PROVIDER="mixed"     → Ollama cho writing, OpenAI/Anthropic cho reasoning (tiết kiệm chi phí)
"""

from functools import lru_cache
from langchain_core.language_models import BaseChatModel

from app.core.config import get_settings


def get_llm(role: str = "reasoning") -> BaseChatModel:
    """
    Factory function trả về LLM instance phù hợp.

    Args:
        role: Mục đích sử dụng của LLM:
            - "reasoning"  → Phân tích dữ liệu, logic, orchestration (GPT-4o / Ollama reasoning)
            - "writing"    → Sáng tạo nội dung, kịch bản, bài viết (Claude 3.5 / Ollama writing)
            - "vision"     → Phân tích hình ảnh thumbnail (GPT-4o Vision / Ollama llava)

    Returns:
        BaseChatModel instance đã được cấu hình
    """
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "openai":
        return _get_openai_llm(role, settings)

    elif provider == "anthropic":
        if role == "writing":
            return _get_anthropic_llm(settings)
        return _get_openai_llm(role, settings)

    elif provider == "ollama":
        return _get_ollama_llm(role, settings)

    elif provider == "mixed":
        # Tiết kiệm API cost: dùng Ollama cho writing, cloud cho reasoning/vision
        if role == "writing":
            return _get_ollama_llm(role, settings)
        return _get_openai_llm(role, settings)

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: '{provider}'. "
            "Supported values: 'openai', 'anthropic', 'ollama', 'mixed'"
        )


def _get_openai_llm(role: str, settings) -> BaseChatModel:
    """OpenAI GPT-4o / GPT-4o-mini"""
    from langchain_openai import ChatOpenAI

    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    # Vision role dùng GPT-4o (hỗ trợ image input)
    model = settings.openai_model_vision if role == "vision" else settings.openai_model

    return ChatOpenAI(
        model=model,
        api_key=settings.openai_api_key,
        temperature=0.3 if role == "reasoning" else 0.7,
        max_tokens=4096,
    )


def _get_anthropic_llm(settings) -> BaseChatModel:
    """Anthropic Claude 3.5 Sonnet — tốt nhất cho writing"""
    from langchain_anthropic import ChatAnthropic

    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in .env")

    return ChatAnthropic(
        model=settings.anthropic_model,
        api_key=settings.anthropic_api_key,
        temperature=0.7,
        max_tokens=4096,
    )


def _get_ollama_llm(role: str, settings) -> BaseChatModel:
    """
    Ollama local LLM — kết nối đến container Ollama đang chạy.
    
    Base URL:
    - Nếu backend chạy NATIVE (python trực tiếp): localhost:11434
    - Nếu backend chạy trong Docker (cùng network): ollama:11434
    """
    from langchain_ollama import ChatOllama

    # Chọn model theo role
    if role == "vision":
        model = settings.ollama_model_vision   # VD: llava, llava-llama3
    elif role == "writing":
        model = settings.ollama_model_writing  # VD: llama3.2, mistral
    else:
        model = settings.ollama_model_reasoning  # VD: llama3.2, qwen2.5

    return ChatOllama(
        model=model,
        base_url=settings.ollama_base_url,
        temperature=0.3 if role == "reasoning" else 0.7,
        num_predict=4096,  # Max tokens
    )


def get_llm_info() -> dict:
    """
    Trả về thông tin về LLM đang được cấu hình.
    Dùng cho /api/health endpoint để hiển thị cấu hình hiện tại.
    """
    settings = get_settings()
    provider = settings.llm_provider.lower()

    info = {
        "provider": provider,
        "models": {}
    }

    if provider == "openai":
        info["models"] = {
            "reasoning": settings.openai_model,
            "writing": settings.openai_model,
            "vision": settings.openai_model_vision,
        }
    elif provider == "anthropic":
        info["models"] = {
            "reasoning": settings.openai_model,
            "writing": settings.anthropic_model,
            "vision": settings.openai_model_vision,
        }
    elif provider == "ollama":
        info["models"] = {
            "reasoning": settings.ollama_model_reasoning,
            "writing": settings.ollama_model_writing,
            "vision": settings.ollama_model_vision,
        }
        info["ollama_url"] = settings.ollama_base_url
    elif provider == "mixed":
        info["models"] = {
            "reasoning": settings.openai_model,
            "writing": settings.ollama_model_writing,
            "vision": settings.openai_model_vision,
        }
        info["ollama_url"] = settings.ollama_base_url

    return info
