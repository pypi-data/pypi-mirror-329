# stegawave/models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Event(BaseModel):
    eventID: str
    eventName: str
    active: bool
    startTime: datetime
    endTime: datetime
    ipWhitelist: List[str]
    running: bool
    testOutput: Optional[str] = None
    sessionInitPrefix: Optional[str] = None
    hlsPlaybackPrefix: Optional[str] = None

class DecodingResult(BaseModel):
    eventID: str
    results: List[str]