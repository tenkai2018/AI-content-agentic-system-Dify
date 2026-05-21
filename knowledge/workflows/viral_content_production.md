# Workflow: Viral Content Production Pipeline
**ID**: `viral_content_production`  
**Trigger**: User nháº­p Niche/Topic trÃªn Frontend  
**Output**: Ká»‹ch báº£n video + Thumbnail Brief + 6 bÃ i LinkedIn

---

## MÃ´ táº£ tá»•ng quan

Pipeline 4 bÆ°á»›c sáº£n xuáº¥t ná»™i dung hoÃ n chá»‰nh, tá»« viá»‡c tÃ¬m Ã½ tÆ°á»Ÿng dá»±a trÃªn dá»¯ liá»‡u YouTube Ä‘áº¿n táº¡o ra táº¥t cáº£ tÃ i nguyÃªn (assets) cáº§n thiáº¿t Ä‘á»ƒ publish. Má»—i bÆ°á»›c lÃ  má»™t Agent chuyÃªn biá»‡t vÃ  pháº£i Ä‘Æ°á»£c con ngÆ°á»i duyá»‡t (Human-in-the-loop) trÆ°á»›c khi sang bÆ°á»›c tiáº¿p theo.

---

## BÆ°á»›c 1: Viral Detection (Researcher Agent)

**Agent**: `Researcher`  
**Skill file**: `knowledge/skills/researcher.md`  
**Tool sá»­ dá»¥ng**: YouTube Data API v3 (qua n8n)

### HÃ nh Ä‘á»™ng:
1. Nháº­n `niche` vÃ  `keywords` tá»« User Input
2. Gá»i YouTube API Ä‘á»ƒ láº¥y danh sÃ¡ch video trong niche (tá»‘i thiá»ƒu 20 video)
3. Vá»›i má»—i video, láº¥y: `video_views`, `channel_average_views`, `title`, `thumbnail_url`, `published_at`
4. TÃ­nh **Outlier Score** cho má»—i video:
   ```
   outlier_score = (video_views / channel_average_views) * 100
   ```
5. Lá»c vÃ  sáº¯p xáº¿p theo Outlier Score giáº£m dáº§n
6. PhÃ¢n loáº¡i káº¿t quáº£:
   - `outlier_score >= 500` â†’ **ðŸ”¥ Viral Outlier**
   - `outlier_score >= 200` â†’ **â­ Strong Outlier**
   - `outlier_score < 200` â†’ Loáº¡i bá» (khÃ´ng Ä‘á»§ momentum)

### Output (lÆ°u vÃ o LangGraph State):
```json
{
  "step": "viral_detection",
  "status": "awaiting_approval",
  "results": [
    {
      "rank": 1,
      "title": "...",
      "channel": "...",
      "outlier_score": 623,
      "category": "Viral Outlier",
      "video_url": "...",
      "thumbnail_url": "...",
      "views": 1200000,
      "channel_avg_views": 192000
    }
  ]
}
```

### Human-in-the-loop Checkpoint:
- Hiá»ƒn thá»‹ danh sÃ¡ch outlier trÃªn UI
- User chá»n 1 video/topic Ä‘á»ƒ tiáº¿p tá»¥c âž” BÆ°á»›c 2

---

## BÆ°á»›c 2: Script Writing (Scriptwriter Agent)

**Agent**: `Scriptwriter`  
**Skill file**: `knowledge/skills/scriptwriter.md`  
**LLM**: Claude 3.5 Sonnet (thiÃªn vá» vÄƒn phong tá»± nhiÃªn)

### HÃ nh Ä‘á»™ng:
1. Nháº­n `selected_topic` vÃ  `video_data` tá»« BÆ°á»›c 1
2. Load System Prompt tá»« `knowledge/skills/scriptwriter.md`
3. PhÃ¢n tÃ­ch title video gá»‘c Ä‘á»ƒ hiá»ƒu "angle" (gÃ³c tiáº¿p cáº­n)
4. Viáº¿t ká»‹ch báº£n theo **Hook Structure báº¯t buá»™c 4 bÆ°á»›c**:
   - **Step 1 - Identify**: XÃ¡c Ä‘á»‹nh viewer Ä‘ang gáº·p váº¥n Ä‘á» gÃ¬
   - **Step 2 - Missed Opportunity**: CÆ¡ há»™i há» Ä‘ang bá» lá»¡ lÃ  gÃ¬
   - **Step 3 - Outcome**: Káº¿t quáº£ cá»¥ thá»ƒ há» sáº½ Ä‘áº¡t Ä‘Æ°á»£c
   - **Step 4 - Visual Preview**: MÃ´ táº£ hÃ¬nh áº£nh/cáº£nh quay má»Ÿ Ä‘áº§u
5. Viáº¿t toÃ n bá»™ ká»‹ch báº£n video (3-10 phÃºt tÃ¹y yÃªu cáº§u)

### Output (lÆ°u vÃ o LangGraph State):
```json
{
  "step": "script_writing",
  "status": "awaiting_approval",
  "script": {
    "hook": {
      "identify": "...",
      "missed_opportunity": "...",
      "outcome": "...",
      "visual_preview": "..."
    },
    "full_script": "..."
  }
}
```

### Human-in-the-loop Checkpoint:
- Hiá»ƒn thá»‹ ká»‹ch báº£n trÃªn UI
- User cÃ³ thá»ƒ chá»‰nh sá»­a trá»±c tiáº¿p hoáº·c yÃªu cáº§u viáº¿t láº¡i
- User nháº¥n "Duyá»‡t" âž” BÆ°á»›c 3

---

## BÆ°á»›c 3: Thumbnail Brief (Visual Director Agent)

**Agent**: `Visual Director`  
**Skill file**: `knowledge/skills/visual_director.md`  
**LLM**: GPT-4o Vision (Ä‘á»ƒ phÃ¢n tÃ­ch hÃ¬nh áº£nh)

### HÃ nh Ä‘á»™ng:
1. Nháº­n `thumbnail_url` tá»« cÃ¡c top outlier video á»Ÿ BÆ°á»›c 1
2. Gá»i GPT-4o Vision API Ä‘á»ƒ phÃ¢n tÃ­ch tá»«ng thumbnail:
   - MÃ u sáº¯c chá»§ Ä‘áº¡o (color palette)
   - Biá»ƒu cáº£m khuÃ´n máº·t (náº¿u cÃ³)
   - Text overlay vÃ  font style
   - Layout vÃ  composition
3. Tá»•ng há»£p nhá»¯ng yáº¿u tá»‘ chung cá»§a cÃ¡c thumbnail viral
4. Dá»±a vÃ o ká»‹ch báº£n á»Ÿ BÆ°á»›c 2, táº¡o **Thumbnail Brief** cho designer:
   - Background concept
   - Color recommendation
   - Text overlay (max 5 tá»«)
   - Emotion/expression guide
   - Yáº¿u tá»‘ Cáº¦N TRÃNH (Ä‘á»ƒ khÃ´ng copy thumbnail cÅ©)

### Output:
```json
{
  "step": "thumbnail_brief",
  "status": "awaiting_approval",
  "brief": {
    "concept": "...",
    "background": "...",
    "colors": ["#...", "#..."],
    "text_overlay": "...",
    "emotion": "...",
    "avoid": ["...", "..."],
    "reference_analysis": "..."
  }
}
```

### Human-in-the-loop Checkpoint:
- Hiá»ƒn thá»‹ brief + áº£nh phÃ¢n tÃ­ch trÃªn UI
- User duyá»‡t brief âž” BÆ°á»›c 4

---

## BÆ°á»›c 4: LinkedIn Repurposing (Repurposer Agent)

**Agent**: `Repurposer`  
**Skill file**: `knowledge/skills/repurposer.md`  
**LLM**: Claude 3.5 Sonnet

### HÃ nh Ä‘á»™ng:
1. Nháº­n `full_script` tá»« BÆ°á»›c 2
2. Load 6 LinkedIn format templates tá»« `knowledge/skills/repurposer.md`
3. Táº¡o **6 bÃ i viáº¿t LinkedIn song song** (parallel generation):
   - `Format 1`: Personal Story â€” Ká»ƒ cÃ¢u chuyá»‡n cÃ¡ nhÃ¢n liÃªn quan Ä‘áº¿n topic
   - `Format 2`: Strong Opinion â€” Chia sáº» quan Ä‘iá»ƒm gÃ¢y tranh luáº­n
   - `Format 3`: Step-by-step â€” HÆ°á»›ng dáº«n thá»±c hÃ nh dáº¡ng list
   - `Format 4`: Question Hook â€” Má»Ÿ Ä‘áº§u báº±ng cÃ¢u há»i kÃ­ch thÃ­ch suy nghÄ©
   - `Format 5`: Data & Insight â€” Dáº«n sá»‘ liá»‡u, insight tá»« nghiÃªn cá»©u
   - `Format 6`: Failure & Lesson â€” Chia sáº» tháº¥t báº¡i vÃ  bÃ i há»c rÃºt ra

### Output:
```json
{
  "step": "linkedin_repurposing",
  "status": "completed",
  "posts": {
    "personal_story": "...",
    "strong_opinion": "...",
    "step_by_step": "...",
    "question_hook": "...",
    "data_insight": "...",
    "failure_lesson": "..."
  }
}
```

### Final Step:
- LÆ°u toÃ n bá»™ káº¿t quáº£ vÃ o **PostgreSQL** (báº£ng `content_tasks`)
- LÆ°u embedding cá»§a ká»‹ch báº£n vÃ o **ChromaDB** (Ä‘á»ƒ RAG tham kháº£o sau)
- Cáº­p nháº­t tráº¡ng thÃ¡i task thÃ nh `completed` trÃªn UI

