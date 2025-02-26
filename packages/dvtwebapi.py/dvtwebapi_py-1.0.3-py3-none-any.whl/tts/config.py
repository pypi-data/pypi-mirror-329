from __future__ import annotations

from typing import Literal

try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass

import os

SPEAKERS = Literal["show", "haruka", "hikari", "takeru", "santa", "bear"]
EMOTIONS = Literal["happiness", "anger", "sadness"]

API_KEY = os.getenv("VOICE_API_KEY")
BASE_URL = os.getenv("VOICE_BASE_URL")
