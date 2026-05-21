# ðŸ§  Project Context â€” Master Router
**Há»‡ thá»‘ng**: Multi-Agent Content Machine  
**PhiÃªn báº£n**: v1.0  
**Cáº­p nháº­t láº§n cuá»‘i**: 2026-05-15

---

## 1. Táº§m nhÃ¬n há»‡ thá»‘ng (Vision)

Há»‡ thá»‘ng nÃ y tá»± Ä‘á»™ng hÃ³a toÃ n bá»™ quy trÃ¬nh sáº£n xuáº¥t ná»™i dung tá»« **"Ä‘oÃ¡n mÃ²"** sang **"dá»±a trÃªn dá»¯ liá»‡u"**. 
Thay vÃ¬ chá»n chá»§ Ä‘á» ngáº«u nhiÃªn, há»‡ thá»‘ng quÃ©t YouTube Ä‘á»ƒ tÃ¬m ra nhá»¯ng chá»§ Ä‘á» **Ä‘ang cÃ³ momentum thá»±c sá»±**, 
rá»“i tá»± Ä‘á»™ng viáº¿t ká»‹ch báº£n, táº¡o brief thumbnail, vÃ  tÃ¡i cháº¿ ná»™i dung sang LinkedIn â€” táº¥t cáº£ trong má»™t pipeline thá»‘ng nháº¥t.

**Triáº¿t lÃ½ cá»‘t lÃµi**: *"You focus on execution, not guessing."*

---

## 2. Bá»‘n CÃ´ng Cá»¥ Cá»‘t LÃµi (The Four Tools)

| # | TÃªn Tool | MÃ´ táº£ | Agent phá»¥ trÃ¡ch |
|---|---|---|---|
| 1 | **Viral Detector** | QuÃ©t YouTube, tÃ­nh Outlier Score, xÃ¡c Ä‘á»‹nh chá»§ Ä‘á» cÃ³ momentum | `Researcher Agent` |
| 2 | **Script Hook Master** | Viáº¿t ká»‹ch báº£n theo cáº¥u trÃºc Hook chuáº©n 4 bÆ°á»›c | `Scriptwriter Agent` |
| 3 | **Thumbnail Strategist** | PhÃ¢n tÃ­ch thumbnail viral, táº¡o brief cho thumbnail má»›i | `Visual Director Agent` |
| 4 | **LinkedIn Repurposer** | Biáº¿n 1 video thÃ nh 6 bÃ i LinkedIn khÃ¡c nhau | `Repurposer Agent` |

---

## 3. Route Map â€” Trá» Ä‘áº¿n tÃ i nguyÃªn tÆ°Æ¡ng á»©ng

Khi nháº­n Ä‘Æ°á»£c má»™t tÃ¡c vá»¥, **Orchestrator** sáº½ Ä‘á»c file nÃ y trÆ°á»›c, sau Ä‘Ã³ trá» Ä‘áº¿n Ä‘Ãºng workflow vÃ  skill file:

### 3.1 Khi nháº­n task: "Sáº£n xuáº¥t content tá»« Ä‘áº§u" (Full Pipeline)
- **Workflow cáº§n Ä‘á»c**: [`knowledge/workflows/viral_content_production.md`](knowledge/workflows/viral_content_production.md)
- **Skills cáº§n load theo thá»© tá»±**:
  1. [`knowledge/skills/researcher.md`](knowledge/skills/researcher.md) â€” BÆ°á»›c 1: Viral Detection
  2. [`knowledge/skills/scriptwriter.md`](knowledge/skills/scriptwriter.md) â€” BÆ°á»›c 2: Script Writing
  3. [`knowledge/skills/visual_director.md`](knowledge/skills/visual_director.md) â€” BÆ°á»›c 3: Thumbnail Brief
  4. [`knowledge/skills/repurposer.md`](knowledge/skills/repurposer.md) â€” BÆ°á»›c 4: LinkedIn Repurposing

### 3.2 Khi nháº­n task: "Chá»‰ tÃ¬m Ã½ tÆ°á»Ÿng viral"
- **Skills cáº§n load**: [`knowledge/skills/researcher.md`](knowledge/skills/researcher.md)

### 3.3 Khi nháº­n task: "Chá»‰ viáº¿t ká»‹ch báº£n"
- **Skills cáº§n load**: [`knowledge/skills/scriptwriter.md`](knowledge/skills/scriptwriter.md)

### 3.4 Khi nháº­n task: "Táº¡o brief thumbnail"
- **Skills cáº§n load**: [`knowledge/skills/visual_director.md`](knowledge/skills/visual_director.md)

### 3.5 Khi nháº­n task: "Táº¡o ná»™i dung LinkedIn tá»« ká»‹ch báº£n cÃ³ sáºµn"
- **Skills cáº§n load**: [`knowledge/skills/repurposer.md`](knowledge/skills/repurposer.md)

---

## 4. NguyÃªn táº¯c váº­n hÃ nh (Operating Principles)

1. **Data-first**: Má»i quyáº¿t Ä‘á»‹nh vá» chá»§ Ä‘á» pháº£i dá»±a trÃªn Outlier Score. KhÃ´ng táº¡o ná»™i dung vá» chá»§ Ä‘á» cÃ³ score < 200.
2. **Brand consistency**: Scriptwriter Agent PHáº¢I Ä‘á»c Brand Voice section trong `knowledge/skills/scriptwriter.md` trÆ°á»›c khi viáº¿t.
3. **Human-in-the-loop**: Sau má»—i bÆ°á»›c, káº¿t quáº£ Ä‘Æ°á»£c gá»­i vá» UI Ä‘á»ƒ con ngÆ°á»i duyá»‡t trÆ°á»›c khi tiáº¿p tá»¥c.
4. **Fail gracefully**: Náº¿u má»™t Agent tháº¥t báº¡i, lÆ°u error vÃ o PostgreSQL vÃ  thÃ´ng bÃ¡o vá» UI. KhÃ´ng dá»«ng toÃ n bá»™ pipeline.

---

## 5. Cáº¥u trÃºc bá»™ nhá»› (Memory Architecture)

| Loáº¡i Memory | CÃ´ng nghá»‡ | DÃ¹ng Ä‘á»ƒ |
|---|---|---|
| Short-term | LangGraph State | Ngá»¯ cáº£nh há»™i thoáº¡i hiá»‡n táº¡i, káº¿t quáº£ tá»«ng bÆ°á»›c |
| Procedural/State | PostgreSQL | Lá»‹ch sá»­ task, tráº¡ng thÃ¡i content, channel metrics |
| Long-term Semantic | ChromaDB (RAG) | Ná»™i dung cÅ© thÃ nh cÃ´ng, brand guidelines |
| Static Knowledge | File-based Markdown | Skills, Workflows (thÆ° má»¥c nÃ y) |

