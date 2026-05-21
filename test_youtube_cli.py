#!/usr/bin/env python3
"""
Standalone CLI Script to test YouTube Viral Video Discovery (Outlier Analysis)
Allows running the viral research node directly from command line.
"""

import os
import sys
import asyncio
import argparse

# Add backend directory to sys.path so app imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

# Force terminal encoding to UTF-8 to prevent cp1252/UnicodeEncodeError on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load environment variables from root .env
from dotenv import load_dotenv
load_dotenv()

from app.core.youtube_client import fetch_youtube_outliers
from app.core.config import get_settings


def _category_from_score(score: float) -> str:
    if score >= 500:
        return "Viral Outlier"
    if score >= 200:
        return "Strong Outlier"
    return "Below Threshold"


async def main():
    parser = argparse.ArgumentParser(description="Test YouTube Viral Video Outlier Detection")
    parser.add_argument("--niche", type=str, required=True, help="Content niche (e.g. 'AI development')")
    parser.add_argument("--keywords", type=str, nargs="*", default=[], help="Optional search keywords")
    parser.add_argument("--max-results", type=int, default=30, help="Max videos to analyze (default: 30)")
    parser.add_argument("--language", type=str, default="vi", help="Relevance language (default: 'vi')")
    
    args = parser.parse_args()

    settings = get_settings()
    if not settings.youtube_api_key or settings.youtube_api_key.startswith("AIza..."):
        print("\n[!] ERROR: YOUTUBE_API_KEY chưa được cấu hình chính xác trong file .env!")
        print("Vui lòng cập nhật YOUTUBE_API_KEY thực tế từ Google Cloud Console vào file .env ở thư mục gốc.")
        sys.exit(1)

    print(f"\n======================================================================")
    print(f" Đang thực hiện tìm kiếm video Viral cho ngách: '{args.niche}'")
    if args.keywords:
        print(f" Từ khóa bổ trợ: {args.keywords}")
    print(f" Ngôn ngữ: '{args.language}' | Giới hạn phân tích: {args.max_results} videos")
    print(f"======================================================================\n")
    print("⏳ Đang kết nối YouTube API & phân tích tỷ lệ Outlier của từng kênh...")

    try:
        rows = await fetch_youtube_outliers(
            niche=args.niche,
            keywords=args.keywords,
            language=args.language,
            max_results=args.max_results,
        )

        ranked = []
        for row in rows:
            score = (row.video_views / max(row.channel_average_views, 1.0)) * 100.0
            category = _category_from_score(score)
            
            # Chỉ lấy các video đạt ngưỡng Strong/Viral Outlier (>= 200%)
            if score >= 200:
                ranked.append({
                    "score": score,
                    "category": category,
                    "title": row.title,
                    "channel": row.channel_name,
                    "views": row.video_views,
                    "avg_views": int(row.channel_average_views),
                    "url": row.video_url
                })

        # Sắp xếp theo tỷ lệ Outlier Score giảm dần
        ranked.sort(key=lambda x: x["score"], reverse=True)

        if not ranked:
            print("\n❌ Không tìm thấy video nào đạt ngưỡng Outlier (Score >= 200%).")
            print("Gợi ý: Thử mở rộng niche hoặc sử dụng từ khóa phổ biến hơn.")
            return

        print(f"\n✅ Đã phân tích xong! Tìm thấy {len(ranked)} video đột biến (Outlier) trên tổng số {len(rows)} video đã quét:\n")
        
        # In kết quả dưới dạng bảng CLI
        header = f"{'Hạng':<5} | {'Điểm Outlier':<13} | {'Phân loại':<15} | {'Lượt xem':<10} | {'Mức TB kênh':<12} | {'Kênh':<20} | {'Tiêu đề video'}"
        print(header)
        print("-" * 120)
        
        for idx, item in enumerate(ranked, 1):
            title_truncated = item["title"][:50] + "..." if len(item["title"]) > 50 else item["title"]
            channel_truncated = item["channel"][:18] + "..." if len(item["channel"]) > 18 else item["channel"]
            score_str = f"{item['score']:.1f}%"
            
            row_str = (
                f"{idx:<5} | "
                f"{score_str:<13} | "
                f"{item['category']:<15} | "
                f"{item['views']:<10,} | "
                f"{item['avg_views']:<12,} | "
                f"{channel_truncated:<20} | "
                f"{title_truncated}"
            )
            print(row_str)
            print(f"      🔗 URL: {item['url']}")
            print("-" * 120)

    except Exception as e:
        print(f"\n[!] Đã xảy ra lỗi khi thực thi:")
        print(f"    {str(e)}")


if __name__ == "__main__":
    # Windows event loop fix for async subprocess/https calls
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
