# Agentic AI System Blueprint (8-Agent Content Machine)

## Má»¥c tiÃªu
XÃ¢y má»™t há»‡ thá»‘ng multi-agent Ä‘á»ƒ:
1. sÄƒn xu hÆ°á»›ng,
2. táº¡o hooks/titles,
3. viáº¿t script dÃ i,
4. repurpose sang Shorts,
5. táº¡o thumbnail prompt,
6. viáº¿t metadata SEO,
7. viáº¿t newsletter,
8. phÃ¢n tÃ­ch hiá»‡u suáº¥t video sau khi Ä‘Äƒng.

Há»‡ thá»‘ng nÃ y dÃ¹ng mÃ´ hÃ¬nh **human defines goals, AI builds + maintains workflows** theo cÃ¡ch thá»±c dá»¥ng: con ngÆ°á»i Ä‘áº·t má»¥c tiÃªu, giá»›i háº¡n vÃ  tiÃªu chÃ­ Ä‘áº§u ra; AI tá»± láº­p káº¿ hoáº¡ch, gá»i tool, xuáº¥t artifact vÃ  há»c tá»« dá»¯ liá»‡u hiá»‡u suáº¥t.

---

## 1) Kiáº¿n trÃºc khuyáº¿n nghá»‹

### Core stack
- **Orchestrator / Agent runtime:** LangGraph hoáº·c OpenAI Agents SDK
- **Automation / I/O:** n8n
- **Database:** PostgreSQL
- **Content store:** Notion hoáº·c Airtable
- **LLM:** OpenAI hoáº·c Claude
- **Search / trend ingestion:** RSS, YouTube Data API, web search
- **Analytics ingestion:** YouTube Studio CSV export hoáº·c YouTube Data API
- **Optional memory:** vector DB (Chroma, Weaviate, Pinecone)

### Táº¡i sao chá»n mÃ´ hÃ¬nh nÃ y
- LangGraph phÃ¹ há»£p vá»›i workflow dÃ i, tráº¡ng thÃ¡i rÃµ rÃ ng, cÃ³ nhÃ¡nh vÃ  retry.
- OpenAI Agents SDK há»— trá»£ tool-calling, specialist handoff, vÃ  state Ä‘á»§ Ä‘á»ƒ lÃ m viá»‡c multi-step.
- n8n há»£p Ä‘á»ƒ nháº­n webhook, cháº¡y lá»‹ch, gá»i API vÃ  Ä‘áº©y dá»¯ liá»‡u sang Notion/Airtable.
- Notion/Airtable phÃ¹ há»£p lÃ m â€œsingle source of truthâ€ cho content pipeline.

---

## 2) Luá»“ng tá»•ng thá»ƒ

```text
[Scheduler / Webhook]
        â†“
[Agent 0: Orchestrator / Router]
        â†“
[Agent 1: Researcher]
        â†“
[Agent 2: Ideator & Hook Master]
        â†“
[Agent 3: Scriptwriter]
        â†“
[Agent 4: Repurposer]
        â†“
[Agent 5: Visual Director]
        â†“
[Agent 6: SEO & Metadata Expert]
        â†“
[Agent 7: Newsletter Writer]
        â†“
[QA / Validator]
        â†“
[Publish to Notion / Airtable / Drive / Slack]
        â†“
[Agent 8: Analyst]
        â†“
[Feedback loop to future content]
```

---

## 3) Vai trÃ² tá»«ng agent

### Agent 0 â€” Orchestrator / Router
Nhiá»‡m vá»¥:
- nháº­n goal cá»§a báº¡n,
- táº¡o plan,
- quyáº¿t Ä‘á»‹nh agent nÃ o cháº¡y trÆ°á»›c,
- theo dÃµi tráº¡ng thÃ¡i tá»«ng bÆ°á»›c.

Äáº§u ra:
- `content_brief`
- `execution_plan`
- `task_status`

### Agent 1 â€” Researcher
Nhiá»‡m vá»¥:
- quÃ©t RSS, YouTube, blog, social signals,
- láº¥y 5 Ã½ tÆ°á»Ÿng má»›i/ngÃ y,
- phÃ¡t hiá»‡n video/outlier topic.

Äáº§u ra:
- `topic_candidates[]`
- `trend_score`
- `source_urls[]`

### Agent 2 â€” Ideator & Hook Master
Nhiá»‡m vá»¥:
- biáº¿n topic thÃ nh angles,
- táº¡o 5 titles,
- táº¡o 1â€“3 hooks ngáº¯n.

Äáº§u ra:
- `angles[]`
- `titles[]`
- `hook_options[]`

### Agent 3 â€” Scriptwriter
Nhiá»‡m vá»¥:
- viáº¿t script dÃ i 1.200â€“2.000 tá»«,
- phÃ¢n Ä‘oáº¡n rÃµ hook / intro / value / climax / CTA,
- tÃ¡ch `[HÃ¬nh áº£nh hiá»ƒn thá»‹]` vÃ  `[Lá»i nÃ³i]`.

Äáº§u ra:
- `full_script`
- `scene_outline`

### Agent 4 â€” Repurposer
Nhiá»‡m vá»¥:
- cáº¯t script dÃ i thÃ nh 3â€“5 short scripts,
- tá»‘i Æ°u cho Shorts/Reels/TikTok.

Äáº§u ra:
- `shorts_scripts[]`

### Agent 5 â€” Visual Director
Nhiá»‡m vá»¥:
- viáº¿t thumbnail concepts,
- viáº¿t prompt áº£nh ná»n tiáº¿ng Anh,
- gá»£i Ã½ bá»‘ cá»¥c text, contrast, focal point.

Äáº§u ra:
- `thumbnail_concepts[]`
- `image_prompts[]`

### Agent 6 â€” SEO & Metadata Expert
Nhiá»‡m vá»¥:
- viáº¿t description,
- tags,
- chapters/timestamps,
- community post,
- social post.

Äáº§u ra:
- `seo_description`
- `tags[]`
- `timestamps[]`
- `community_post`
- `social_post`

### Agent 7 â€” Newsletter Writer
Nhiá»‡m vá»¥:
- chuyá»ƒn ná»™i dung thÃ nh newsletter email,
- format: váº¥n Ä‘á» â†’ giáº£i phÃ¡p â†’ action steps.

Äáº§u ra:
- `newsletter_subject`
- `newsletter_body`

### Agent 8 â€” Analyst
Nhiá»‡m vá»¥:
- Ä‘á»c CTR, retention, view duration, click patterns,
- Ä‘á» xuáº¥t cÃ¡ch sá»­a hook, pacing, Ä‘oáº¡n rá»›t retention.

Äáº§u ra:
- `performance_summary`
- `next_video_recommendations`
- `script_fixes[]`

---

## 4) Dá»¯ liá»‡u chung (shared state)

DÃ¹ng 1 object chuáº©n cho toÃ n há»‡ thá»‘ng:

```json
{
  "project_id": "",
  "niche": "",
  "goal": "",
  "audience": "",
  "language": "vi",
  "content_brief": {
    "topic": "",
    "angle": "",
    "promise": "",
    "constraints": []
  },
  "research": {
    "sources": [],
    "topic_candidates": []
  },
  "hooks": {
    "titles": [],
    "hook_options": []
  },
  "script": {
    "full_script": "",
    "scene_outline": []
  },
  "repurposed": {
    "shorts_scripts": []
  },
  "visuals": {
    "thumbnail_concepts": [],
    "image_prompts": []
  },
  "seo": {
    "description": "",
    "tags": [],
    "timestamps": [],
    "community_post": "",
    "social_post": ""
  },
  "newsletter": {
    "subject": "",
    "body": ""
  },
  "analytics": {
    "ctr": null,
    "retention": null,
    "notes": []
  },
  "status": {
    "current_step": "",
    "completed_steps": [],
    "errors": []
  }
}
```

---

## 5) Orchestration logic

### Quy táº¯c chÃ­nh
- Náº¿u `research` chÆ°a cÃ³ data â†’ cháº¡y Agent 1.
- Náº¿u `topic_candidates` cÃ³ Ã­t nháº¥t 1 topic tá»‘t â†’ cháº¡y Agent 2.
- Náº¿u Ä‘Ã£ chá»n 1 hook tá»‘t â†’ cháº¡y Agent 3.
- Sau script dÃ i â†’ cháº¡y Agent 4, 5, 6, 7 song song.
- TrÆ°á»›c khi publish â†’ cháº¡y QA.
- Sau khi publish vÃ  cÃ³ analytics â†’ cháº¡y Agent 8.

### Máº«u Ä‘iá»u phá»‘i
```text
Goal input
â†’ normalize
â†’ route
â†’ execute specialist agents
â†’ validate outputs
â†’ store artifacts
â†’ publish
â†’ learn from analytics
```

---

## 6) Cáº¥u trÃºc tool registry

Má»—i agent chá»‰ Ä‘Æ°á»£c gá»i Ä‘Ãºng tool cáº§n thiáº¿t.

### Tool tá»‘i thiá»ƒu
- `search_rss(query)`
- `search_youtube(query)`
- `fetch_url(url)`
- `write_notion_page(database_id, payload)`
- `update_airtable_record(base_id, table, payload)`
- `read_analytics(csv_path or api_query)`
- `send_slack(message)`
- `save_file(path, content)`

### NguyÃªn táº¯c
- Tool pháº£i cÃ³ schema rÃµ rÃ ng.
- Tool tráº£ vá» JSON chuáº©n hÃ³a.
- Agent khÃ´ng Ä‘Æ°á»£c tá»± bá»‹a output khi tool fail.
- Náº¿u tool fail â†’ retry â†’ fallback â†’ escalate.

---

## 7) Thiáº¿t káº¿ tá»«ng agent prompt

### Prompt template chung
```text
You are [ROLE].
Mission:
- [1â€“3 bullet points]

Input:
- context JSON

Output rules:
- Return JSON only
- No markdown
- No extra commentary
- Follow schema exactly
```

### Prompt cho Agent 1
Má»¥c tiÃªu:
- tÃ¬m topic má»›i,
- tráº£ vá» nguá»“n vÃ  score.

Output schema:
```json
{
  "topic_candidates": [
    {
      "title": "",
      "summary": "",
      "why_it_matters": "",
      "trend_score": 0,
      "source_urls": []
    }
  ]
}
```

### Prompt cho Agent 2
Má»¥c tiÃªu:
- táº¡o hooks/titles theo tá»«ng angle.

Output schema:
```json
{
  "angles": [],
  "titles": [],
  "hook_options": []
}
```

### Prompt cho Agent 3
Má»¥c tiÃªu:
- viáº¿t script Ä‘áº§y Ä‘á»§,
- tÃ¡ch hÃ¬nh áº£nh vÃ  lá»i nÃ³i.

Output schema:
```json
{
  "full_script": "",
  "scene_outline": [
    {
      "section": "",
      "visual": "",
      "speech": ""
    }
  ]
}
```

### Prompt cho Agent 8
Má»¥c tiÃªu:
- Ä‘á»c analytics,
- sá»­a pháº§n rá»›t retention.

Output schema:
```json
{
  "performance_summary": "",
  "drop_off_points": [],
  "next_video_recommendations": [],
  "script_fixes": []
}
```

---

## 8) MÃ´ hÃ¬nh triá»ƒn khai thá»±c táº¿

### Option A â€” Dá»… build nháº¥t
- n8n lÃ m trigger + data routing
- OpenAI Agents SDK hoáº·c LangGraph lÃ m brain
- Notion/Airtable lÃ m content hub
- Google Drive lÃ m file store

### Option B â€” Scale tá»‘t hÆ¡n
- API service riÃªng cho orchestrator
- queue worker cho tá»«ng agent
- Postgres cho state
- object storage cho file
- n8n chá»‰ lÃ m integration layer

### Recommendation
Báº¯t Ä‘áº§u báº±ng **Option A**, sau Ä‘Ã³ tÃ¡ch ra **Option B** khi volume tÄƒng.

---

## 9) Database / table nÃªn cÃ³

### `content_briefs`
- `id`
- `niche`
- `topic`
- `goal`
- `status`

### `research_results`
- `brief_id`
- `source_url`
- `title`
- `summary`
- `trend_score`

### `scripts`
- `brief_id`
- `hook`
- `full_script`
- `shorts_scripts`
- `newsletter_body`

### `assets`
- `brief_id`
- `thumbnail_concepts`
- `image_prompts`

### `analytics`
- `video_id`
- `ctr`
- `retention`
- `avg_view_duration`
- `notes`

---

## 10) Build plan theo tuáº§n

### Tuáº§n 1
- dá»±ng Notion/Airtable schema
- táº¡o webhook intake
- Ä‘á»‹nh nghÄ©a JSON state
- connect LLM API

### Tuáº§n 2
- Agent 1 + Agent 2
- lÆ°u topic vÃ  hook vÃ o database
- review cháº¥t lÆ°á»£ng Ä‘áº§u ra

### Tuáº§n 3
- Agent 3 + QA
- táº¡o script dÃ i cÃ³ cáº¥u trÃºc
- kiá»ƒm tra consistency

### Tuáº§n 4
- Agent 4, 5, 6, 7
- xuáº¥t bá»™ asset hoÃ n chá»‰nh cho 1 video

### Tuáº§n 5
- Agent 8
- import YouTube Studio CSV
- táº¡o feedback loop

### Tuáº§n 6
- tá»‘i Æ°u retry, logging, versioning
- template hÃ³a Ä‘á»ƒ bÃ¡n láº¡i cho client

---

## 11) CÃ¡c lá»—i thÆ°á»ng gáº·p

### Lá»—i 1: Má»™t agent lÃ m quÃ¡ nhiá»u viá»‡c
Giáº£i phÃ¡p:
- tÃ¡ch role rÃµ hÆ¡n
- má»—i agent chá»‰ chá»‹u 1 outcome

### Lá»—i 2: Output khÃ´ng Ä‘á»“ng nháº¥t
Giáº£i phÃ¡p:
- Ã©p JSON schema
- validate trÆ°á»›c khi chuyá»ƒn bÆ°á»›c

### Lá»—i 3: KhÃ´ng cÃ³ shared state
Giáº£i phÃ¡p:
- táº¥t cáº£ agent Ä‘á»c/ghi cÃ¹ng 1 object chuáº©n

### Lá»—i 4: KhÃ´ng cÃ³ feedback loop
Giáº£i phÃ¡p:
- báº¯t buá»™c Agent 8 Ä‘á»c analytics sau publish

---

## 12) PhiÃªn báº£n template Ä‘á»ƒ bÃ¡n láº¡i

Báº¡n cÃ³ thá»ƒ biáº¿n há»‡ nÃ y thÃ nh sáº£n pháº©m dá»‹ch vá»¥ theo 3 lá»›p:

### Basic
- research + hooks + script

### Pro
- thÃªm shorts + thumbnail + SEO

### Premium
- thÃªm newsletter + analytics loop + optimization

---

## 13) Káº¿t luáº­n

ÄÃ¢y khÃ´ng pháº£i lÃ  â€œ1 AI biáº¿t háº¿tâ€, mÃ  lÃ :
- 1 orchestrator
- 8 specialist agents
- 1 state chung
- 1 pipeline publish
- 1 feedback loop

CÃ ng tÃ¡ch rÃµ vai trÃ², há»‡ thá»‘ng cÃ ng dá»… báº£o trÃ¬, dá»… nhÃ¢n báº£n vÃ  dá»… bÃ¡n láº¡i cho khÃ¡ch hÃ ng khÃ¡c.

