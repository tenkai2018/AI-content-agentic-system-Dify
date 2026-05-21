# Äáº·c táº£ Ká»¹ thuáº­t: Quy trÃ¬nh Tá»± Ä‘á»™ng hÃ³a Video (Video Automation Pipeline)

**PhiÃªn báº£n:** 1.0  
**NgÃ y táº¡o:** 2026-05-16  

## 1. Tá»•ng quan Há»‡ thá»‘ng (System Overview)
Má»¥c tiÃªu cá»§a module nÃ y lÃ  tá»± Ä‘á»™ng hÃ³a viá»‡c táº¡o hÃ¬nh áº£nh (Visuals) vÃ  Ã¢m thanh (Voiceover) tá»« ká»‹ch báº£n AI, cho phÃ©p duyá»‡t ná»™i dung (Human-in-the-loop), vÃ  cuá»‘i cÃ¹ng render thÃ nh video hoÃ n chá»‰nh báº±ng Remotion mÃ  khÃ´ng cáº§n chÃ¨n assets thá»§ cÃ´ng.

## 2. CÃ¡c cÃ´ng nghá»‡ vÃ  API sá»­ dá»¥ng
*   **HÃ¬nh áº£nh (Visuals):** OpenAI API (DALL-E 3).
*   **Giá»ng Ä‘á»c (Voiceover/TTS):** OpenAI API (TTS-1).
*   **Nháº¡c ná»n (BGM):** Sá»­ dá»¥ng cÃ¡c file nháº¡c cÃ³ sáºµn trong thÆ° má»¥c `remotion_app/public/audio/bgm/`.
*   **Video Engine:** Remotion.
*   **Orchestration:** LangGraph (Python).

## 3. Quy trÃ¬nh chi tiáº¿t (Pipeline Flow)

Quy trÃ¬nh gá»‘c sáº½ Ä‘Æ°á»£c bá»• sung thÃªm 2 Node má»›i:

### BÆ°á»›c 3.1: Asset Generator Node
*   **Input:** `script_result` (ká»‹ch báº£n chi tiáº¿t) vÃ  `thumbnail_brief`.
*   **Xá»­ lÃ½ Audio:** 
    *   TÃ¡ch ká»‹ch báº£n thÃ nh cÃ¡c cÃ¢u/slide.
    *   Gá»i OpenAI TTS Ä‘á»ƒ chuyá»ƒn vÄƒn báº£n thÃ nh file `.mp3`.
*   **Xá»­ lÃ½ HÃ¬nh áº£nh:**
    *   Sá»­ dá»¥ng LLM (GPT-4o) táº¡o prompt DALL-E 3 cho tá»«ng cÃ¢u/slide dá»±a trÃªn ngá»¯ cáº£nh ká»‹ch báº£n.
    *   Gá»i DALL-E 3 sinh áº£nh tá»· lá»‡ 9:16 (Ä‘á»ƒ lÃ m video dá»c).
*   **LÆ°u trá»¯:** 
    *   Assets Ä‘Æ°á»£c táº£i vá» vÃ  lÆ°u vÃ o thÆ° má»¥c: `remotion_app/public/assets/generated/{task_id}/`.
*   **Output:** `assets_result` (chá»©a danh sÃ¡ch URL local cá»§a audio vÃ  image theo tá»«ng slide).

### BÆ°á»›c 3.2: Human-in-the-Loop (HITL) - Kiá»ƒm duyá»‡t Assets
*   **Tráº¡ng thÃ¡i:** Pipeline táº¡m dá»«ng (Pause).
*   **HÃ nh Ä‘á»™ng:** NgÆ°á»i dÃ¹ng kiá»ƒm tra cháº¥t lÆ°á»£ng hÃ¬nh áº£nh vÃ  file ghi Ã¢m trÃªn UI.
*   **Routing:** Náº¿u Approve, chuyá»ƒn sang bÆ°á»›c Video Producer. Náº¿u Reject, cháº¡y láº¡i Asset Generator hoáº·c káº¿t thÃºc sá»›m Ä‘á»ƒ sá»­a Ä‘á»•i script.

### BÆ°á»›c 3.3: Video Producer Node
*   **Input:** `assets_result` Ä‘Ã£ Ä‘Æ°á»£c duyá»‡t.
*   **Xá»­ lÃ½ Data:**
    *   Backend tá»± Ä‘á»™ng táº¡o ra file `manifest_{task_id}.json` lÆ°u táº¡i `remotion_app/src/data/` (hoáº·c truyá»n qua CLI props).
    *   Manifest bao gá»“m: ThÃ´ng tin tá»«ng slide (vÄƒn báº£n, Ä‘Æ°á»ng dáº«n áº£nh, Ä‘Æ°á»ng dáº«n audio, thá»i lÆ°á»£ng).
*   **Render:**
    *   Gá»i lá»‡nh subprocess: `npx remotion render WalkthroughVideo public/output_{task_id}.mp4 --props=./path_to_manifest.json` tá»« thÆ° má»¥c `remotion_app`.
*   **Output:** `video_result` (Ä‘Æ°á»ng dáº«n tá»›i file `.mp4` hoÃ n chá»‰nh).

## 4. CÃ¡c thay Ä‘á»•i vá» Code

### 4.1. Backend (Python)
*   **`orchestrator.py`**:
    *   ThÃªm `asset_generator_node` vÃ  `video_producer_node`.
    *   Cáº­p nháº­t `PipelineState` thÃªm cÃ¡c khÃ³a: `assets_result`, `video_result`, `assets_approved`.
    *   Cáº­p nháº­t Conditional Edges cho phÃ©p ngáº¯t luá»“ng táº¡i `assets_approved`.

### 4.2. Frontend/Video (Remotion)
*   **`Root.tsx`**:
    *   Cáº­p nháº­t hÃ m `calculateMetadata` Ä‘á»ƒ tÃ­nh toÃ¡n tá»•ng `durationInFrames` tá»± Ä‘á»™ng dá»±a trÃªn Ä‘á»™ dÃ i cá»§a táº¥t cáº£ cÃ¡c file audio Ä‘Æ°á»£c chÃ¨n vÃ o.
*   **`ScreenSlide.tsx` / `Composition.tsx`**:
    *   Sá»­ dá»¥ng tháº» `<Audio src={...} />` cá»§a Remotion Ä‘á»ƒ phÃ¡t Ã¢m thanh TTS cá»§a tá»«ng slide.
    *   ThÃªm má»™t tháº» `<Audio src={...} volume={0.1} />` xuyÃªn suá»‘t composition cho Background Music.
    *   Sá»­a cáº¥u trÃºc UI Ä‘á»ƒ load `imageSrc` tá»« áº£nh do DALL-E 3 táº¡o ra.

## 5. Xá»­ lÃ½ lá»—i (Error Handling)
*   **API Limits:** Báº¯t cÃ¡c exception náº¿u OpenAI API háº¿t quota hoáº·c timeout, lÆ°u status error vÃ o State.
*   **File I/O:** Kiá»ƒm tra vÃ  táº¡o folder `generated/{task_id}` trÆ°á»›c khi lÆ°u áº£nh/Ã¢m thanh.
*   **Render Timeout:** CÃ i Ä‘áº·t timeout cho lá»‡nh `subprocess` cá»§a Remotion (do render cÃ³ thá»ƒ tá»‘n thá»i gian).

---
*TÃ i liá»‡u nÃ y sáº½ lÃ  cÆ¡ sá»Ÿ Ä‘á»ƒ triá»ƒn khai mÃ£ nguá»“n trong há»‡ thá»‘ng.*

