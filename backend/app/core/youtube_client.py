from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import get_settings


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


@dataclass
class VideoMetric:
    video_id: str
    title: str
    channel_id: str
    channel_name: str
    video_views: int
    channel_average_views: float
    published_at: str
    thumbnail_url: str
    video_url: str


class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._http = httpx.AsyncClient(timeout=20.0)
        self._channel_avg_cache: dict[str, float] = {}

    async def close(self) -> None:
        await self._http.aclose()

    async def _get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        req_params = {"key": self.api_key, **params}
        resp = await self._http.get(f"{YOUTUBE_API_BASE}/{endpoint}", params=req_params)
        resp.raise_for_status()
        return resp.json()

    async def search_videos(self, query: str, language: str, max_results: int = 25) -> list[dict[str, Any]]:
        data = await self._get(
            "search",
            {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": min(max_results, 50),
                "relevanceLanguage": language,
            },
        )
        return data.get("items", [])

    async def get_videos_details(self, video_ids: list[str]) -> list[dict[str, Any]]:
        if not video_ids:
            return []
        data = await self._get(
            "videos",
            {
                "part": "snippet,statistics",
                "id": ",".join(video_ids[:50]),
                "maxResults": 50,
            },
        )
        return data.get("items", [])

    async def get_channel_average_views(self, channel_id: str, language: str = "en") -> float:
        if channel_id in self._channel_avg_cache:
            return self._channel_avg_cache[channel_id]

        search_data = await self._get(
            "search",
            {
                "part": "snippet",
                "channelId": channel_id,
                "type": "video",
                "order": "date",
                "maxResults": 10,
                "relevanceLanguage": language,
            },
        )
        video_ids = [item["id"]["videoId"] for item in search_data.get("items", []) if item.get("id", {}).get("videoId")]
        if not video_ids:
            self._channel_avg_cache[channel_id] = 1.0
            return 1.0

        details = await self.get_videos_details(video_ids)
        views = []
        for item in details:
            stats = item.get("statistics", {})
            try:
                views.append(int(stats.get("viewCount", 0)))
            except (TypeError, ValueError):
                continue

        avg = float(sum(views) / len(views)) if views else 1.0
        self._channel_avg_cache[channel_id] = max(avg, 1.0)
        return max(avg, 1.0)


async def fetch_youtube_outliers(niche: str, keywords: list[str], language: str = "en", max_results: int = 30) -> list[VideoMetric]:
    settings = get_settings()
    if not settings.youtube_api_key:
        raise ValueError("YOUTUBE_API_KEY is not set in environment.")

    query = niche
    if keywords:
        query = f"{niche} {' '.join(keywords)}"

    client = YouTubeClient(settings.youtube_api_key)
    try:
        search_items = await client.search_videos(query=query, language=language, max_results=max_results)
        video_ids = [item["id"]["videoId"] for item in search_items if item.get("id", {}).get("videoId")]
        details = await client.get_videos_details(video_ids)

        metrics: list[VideoMetric] = []
        for item in details:
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            video_id = item.get("id")
            channel_id = snippet.get("channelId")
            if not video_id or not channel_id:
                continue

            try:
                video_views = int(stats.get("viewCount", 0))
            except (TypeError, ValueError):
                video_views = 0

            channel_avg = await client.get_channel_average_views(channel_id=channel_id, language=language)
            thumbnails = snippet.get("thumbnails", {})
            thumb = thumbnails.get("high") or thumbnails.get("medium") or thumbnails.get("default") or {}

            metrics.append(
                VideoMetric(
                    video_id=video_id,
                    title=snippet.get("title", ""),
                    channel_id=channel_id,
                    channel_name=snippet.get("channelTitle", ""),
                    video_views=video_views,
                    channel_average_views=channel_avg,
                    published_at=snippet.get("publishedAt", ""),
                    thumbnail_url=thumb.get("url", ""),
                    video_url=f"https://youtube.com/watch?v={video_id}",
                )
            )

        return metrics
    finally:
        await client.close()
