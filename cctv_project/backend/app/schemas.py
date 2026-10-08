import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class SourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название источника")
    url: str = Field(..., description="RTSP URL адрес")
    location: str = Field(..., min_length=1, max_length=255, description="Локация камеры")
    enabled: bool = True

    @field_validator("url")
    @classmethod
    def validate_rtsp_url(cls, v: str) -> str:
        v_stripped = v.strip()
        if not (v_stripped.startswith("rtsp://") or v_stripped.startswith("rtsps://") or v_stripped.startswith("http://") or v_stripped.startswith("https://")):
            raise ValueError("URL должен начинаться с протокола rtsp:// или http(s)://")
        return v_stripped

    @field_validator("name", "location")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    enabled: Optional[bool] = None

    @field_validator("url")
    @classmethod
    def validate_rtsp_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_stripped = v.strip()
        if not (v_stripped.startswith("rtsp://") or v_stripped.startswith("rtsps://") or v_stripped.startswith("http://") or v_stripped.startswith("https://")):
            raise ValueError("URL должен начинаться с протокола rtsp:// или http(s)://")
        return v_stripped

    @field_validator("name", "location")
    @classmethod
    def validate_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

class SourceResponse(SourceBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True