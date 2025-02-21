from __future__ import annotations

from typing import Union
from aiohttp import ClientResponse
from requests import Response as RequestsResponse

from ..errors import ResponseStatusError, RateLimitError
from . import Response, StreamResponse

class CloudflareError(ResponseStatusError):
    ...

def is_cloudflare(text: str) -> bool:
    if "Generated by cloudfront" in text or '<p id="cf-spinner-please-wait">' in text:
        return True
    elif "<title>Attention Required! | Cloudflare</title>" in text or 'id="cf-cloudflare-status"' in text:
        return True
    return '<div id="cf-please-wait">' in text or "<title>Just a moment...</title>" in text

def is_openai(text: str) -> bool:
    return "<p>Unable to load site</p>" in text or 'id="challenge-error-text"' in text

async def raise_for_status_async(response: Union[StreamResponse, ClientResponse], message: str = None):
    if response.ok:
        return
    text = await response.text()
    if message is None:
        is_html = response.headers.get("content-type", "").startswith("text/html") or text.startswith("<!DOCTYPE")
        message = "HTML content" if is_html else text
    if message == "HTML content":
        if response.status == 520:
            message = "Unknown error (Cloudflare)"
        elif response.status in (429, 402):
            message = "Rate limit"
    if response.status == 403 and is_cloudflare(text):
        raise CloudflareError(f"Response {response.status}: Cloudflare detected")
    elif response.status == 403 and is_openai(text):
        raise ResponseStatusError(f"Response {response.status}: OpenAI Bot detected")
    elif response.status == 502:
        raise ResponseStatusError(f"Response {response.status}: Bad gateway")
    else:
        raise ResponseStatusError(f"Response {response.status}: {message}")

def raise_for_status(response: Union[Response, StreamResponse, ClientResponse, RequestsResponse], message: str = None):
    if hasattr(response, "status"):
        return raise_for_status_async(response, message)
    if response.ok:
        return
    if message is None:
        is_html = response.headers.get("content-type", "").startswith("text/html") or response.text.startswith("<!DOCTYPE")
        message = "HTML content" if is_html else response.text
    if message == "HTML content":
        if response.status_code == 520:
            message = "Unknown error (Cloudflare)"
        elif response.status_code in (429, 402):
            message = "Rate limit"
        raise RateLimitError(f"Response {response.status_code}: {message}")
    if response.status_code == 403 and is_cloudflare(response.text):
        raise CloudflareError(f"Response {response.status_code}: Cloudflare detected")
    elif response.status_code == 403 and is_openai(response.text):
        raise ResponseStatusError(f"Response {response.status_code}: OpenAI Bot detected")
    elif response.status_code == 502:
        raise ResponseStatusError(f"Response {response.status_code}: Bad gateway")
    else:
        raise ResponseStatusError(f"Response {response.status_code}: {message}")