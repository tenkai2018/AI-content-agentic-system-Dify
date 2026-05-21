from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, Field


class ResearchResultItem(BaseModel):
    rank: int
    category: str
    outlier_score: float
    title: str
    channel_name: str
    video_url: str
    thumbnail_url: str
    video_views: int
    channel_average_views: float
    published_at: str
    why_viral: str


class TopRecommendedTopic(BaseModel):
    title: str
    angle: str
    reason: str


class ResearcherOutput(BaseModel):
    agent: str = "researcher"
    step: str = "viral_detection"
    input_niche: str
    analysis_summary: str
    total_analyzed: int
    qualifying_videos: int
    results: list[ResearchResultItem]
    top_recommended_topic: TopRecommendedTopic


class HookBlock(BaseModel):
    identify: str
    missed_opportunity: str
    outcome: str
    visual_preview: str


class ScriptPoint(BaseModel):
    point_number: int
    title: str
    explanation: str
    example: str
    takeaway: str


class ScriptBody(BaseModel):
    hook: HookBlock
    credibility: str
    main_content: list[ScriptPoint]
    cta: str
    full_script_text: str


class ScriptwriterOutput(BaseModel):
    agent: str = "scriptwriter"
    step: str = "script_writing"
    topic: str
    estimated_duration_minutes: int = Field(ge=1)
    script: ScriptBody


class ThumbnailBackground(BaseModel):
    type: str
    color_hex: str


class ThumbnailPalette(BaseModel):
    primary: str
    accent: str
    text: str


class ThumbnailTextOverlay(BaseModel):
    main_text: str
    placement: str


class ThumbnailPerson(BaseModel):
    include: bool
    expression: str
    gesture: str


class ThumbnailBriefContent(BaseModel):
    concept: str
    background: ThumbnailBackground
    color_palette: ThumbnailPalette
    text_overlay: ThumbnailTextOverlay
    person: ThumbnailPerson
    emotion_target: str
    avoid: list[str]


class VisualDirectorOutput(BaseModel):
    agent: str = "visual_director"
    step: str = "thumbnail_brief"
    pattern_summary: str
    brief: ThumbnailBriefContent


class PostingScheduleSuggestion(BaseModel):
    monday: str
    wednesday: str
    friday: str
    note: str


class RepurposerPosts(BaseModel):
    personal_story: str
    strong_opinion: str
    step_by_step: str
    question_hook: str
    data_insight: str
    failure_lesson: str


class RepurposerOutput(BaseModel):
    agent: str = "repurposer"
    step: str = "linkedin_repurposing"
    source_topic: str
    posts: RepurposerPosts
    posting_schedule_suggestion: PostingScheduleSuggestion


class SEOOutput(BaseModel):
    agent: str = "seo"
    step: str = "seo_optimization"
    source_topic: str
    youtube_title_options: list[str] = Field(min_length=3, max_length=5)
    focus_keywords: list[str] = Field(min_length=5, max_length=12)
    youtube_tags: list[str] = Field(min_length=8, max_length=20)
    meta_description: str


class NewsletterOutput(BaseModel):
    agent: str = "newsletter"
    step: str = "newsletter_generation"
    source_topic: str
    subject_line: str
    preview_text: str
    newsletter_markdown: str
    call_to_action: str


class AnalystOutput(BaseModel):
    agent: str = "analyst"
    step: str = "performance_analysis"
    source_topic: str
    kpis: list[str] = Field(min_length=3, max_length=8)
    experiment_plan: list[str] = Field(min_length=3, max_length=8)
    risk_notes: list[str] = Field(min_length=2, max_length=6)
    next_actions: list[str] = Field(min_length=3, max_length=8)


def parse_json_from_llm_output(content: str) -> dict[str, Any]:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()
    return json.loads(text)
