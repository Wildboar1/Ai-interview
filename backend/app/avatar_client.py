import os
import json
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

# Base URL for the chosen avatar provider. We'll default to Simli, but the URL can be overridden via env.
AVATAR_API_BASE = os.getenv("AVATAR_API_BASE", "https://api.simli.ai/v1")
AVATAR_API_KEY = os.getenv("AVATAR_API_KEY", "YOUR_SIMLI_API_KEY")

class AvatarClient:
    """Abstract avatar client. Subclass for specific providers (Simli, Azure, D‑ID)."""

    def __init__(self, api_key: str = AVATAR_API_KEY, base_url: str = AVATAR_API_BASE):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.client = httpx.AsyncClient(timeout=None)

    async def generate_avatar_stream(self, text: str) -> Any:
        """Send *text* to the provider and receive a streaming WebRTC video track.

        The real implementation depends on the provider’s API contract. Here we
        provide a minimal Simli‑style request that returns an HLS URL – the
        frontend can ingest this via LiveKit’s `createVideoTrack` helper.
        """
        raise NotImplementedError("Sub‑class must implement generate_avatar_stream")

    async def close(self):
        await self.client.aclose()

class SimliAvatarClient(AvatarClient):
    async def generate_avatar_stream(self, text: str) -> str:
        """Call Simli's text‑to‑avatar endpoint and return a streaming URL.

        Expected response (simplified)::
            {"stream_url": "wss://..."}
        """
        payload = {"text": text, "voice": "default", "format": "webrtc"}
        response = await self.client.post(f"{self.base_url}/avatar/stream", json=payload, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get("stream_url")

# Future implementations for Azure and D‑ID can subclass AvatarClient similarly.
