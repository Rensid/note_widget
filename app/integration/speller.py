import aiohttp
from fastapi import HTTPException


async def check_text_for_errors(text: str):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {"text": text, "lang": "ru,en"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(
                    f"Error {response.status}")
            return await response.json()


async def validate_errors(text: str):
    errors = await check_text_for_errors(text)
    if errors:
        error_words = [error["word"] for error in errors]
        raise HTTPException(
            status_code=400, detail=f"В тексте обнаружены ошибки в следующих словах: {', '.join(error_words)}")
