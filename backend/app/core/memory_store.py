from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import chromadb

from app.core.config import get_settings


@dataclass
class MemoryExample:
    script_excerpt: str
    topic: str
    niche: str
    language: str


class ChromaMemoryStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
        self._collection = self._client.get_or_create_collection(name="successful_scripts")

    def add_successful_script(self, task_id: str, niche: str, language: str, topic: str, script_text: str) -> None:
        document = script_text.strip()
        if not document:
            return

        self._collection.add(
            ids=[f"{task_id}-{uuid4()}"],
            documents=[document],
            metadatas=[
                {
                    "task_id": task_id,
                    "niche": niche,
                    "language": language,
                    "topic": topic,
                }
            ],
        )

    def query_examples(self, niche: str, language: str, limit: int = 3) -> list[MemoryExample]:
        result: dict[str, Any] = self._collection.query(
            query_texts=[f"{niche} {language}"],
            n_results=limit,
            where={"niche": niche},
        )
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]

        examples: list[MemoryExample] = []
        for document, meta in zip(docs, metas):
            if not isinstance(meta, dict):
                continue
            if meta.get("language") != language:
                continue
            examples.append(
                MemoryExample(
                    script_excerpt=str(document)[:600],
                    topic=str(meta.get("topic", "")),
                    niche=str(meta.get("niche", niche)),
                    language=str(meta.get("language", language)),
                )
            )
        return examples


_memory_store: ChromaMemoryStore | None = None


def get_memory_store() -> ChromaMemoryStore:
    global _memory_store
    if _memory_store is None:
        _memory_store = ChromaMemoryStore()
    return _memory_store
