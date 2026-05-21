import aiofiles
import httpx
from openai import AsyncOpenAI
from app.core.config import get_settings

async def get_openai_client() -> AsyncOpenAI:
    settings = get_settings()
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured in environment variables.")
    return AsyncOpenAI(api_key=settings.openai_api_key)

async def generate_tts_openai(text: str, filepath: str, voice: str = "alloy") -> bool:
    """
    Sử dụng OpenAI TTS (Text-to-Speech) API để chuyển văn bản thành âm thanh.
    
    Args:
        text (str): Đoạn văn bản cần đọc.
        filepath (str): Đường dẫn lưu file (.mp3).
        voice (str): Giọng đọc (alloy, echo, fable, onyx, nova, shimmer).
        
    Returns:
        bool: True nếu thành công, False nếu thất bại.
    """
    client = await get_openai_client()
    try:
        response = await client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Ghi nội dung nhị phân vào file
        async with aiofiles.open(filepath, 'wb') as f:
            for chunk in response.iter_bytes():
                await f.write(chunk)
                
        return True
    except Exception as e:
        print(f"[OpenAI TTS] ERROR generating audio: {e}")
        return False

async def generate_image_dalle(prompt: str, filepath: str) -> bool:
    """
    Sử dụng OpenAI DALL-E 3 API để sinh hình ảnh từ prompt và tải về máy.
    Tỷ lệ ảnh mặc định là 1024x1792 (9:16) phù hợp cho video dọc.
    
    Args:
        prompt (str): Prompt mô tả hình ảnh.
        filepath (str): Đường dẫn lưu file ảnh (.png hoặc .jpg).
        
    Returns:
        bool: True nếu thành công, False nếu thất bại.
    """
    client = await get_openai_client()
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792", # 9:16 format
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        if not image_url:
            raise ValueError("No image URL returned from DALL-E 3 API.")
        
        # Tải ảnh từ URL về
        async with httpx.AsyncClient() as http_client:
            img_response = await http_client.get(image_url)
            img_response.raise_for_status()
            
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(img_response.content)
                
        return True
    except Exception as e:
        print(f"[OpenAI DALL-E 3] ERROR generating image: {e}")
        return False
