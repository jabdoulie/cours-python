from pydantic import BaseModel, Field


class ServerIn(BaseModel):
    """Schema for creating a server."""
    host: str
    port: int = Field(default=8080, ge=1, le=65535)   # 1 ≤ port ≤ 65535
    name: str


class ServerOut(ServerIn):
    """Schema returned to the client — extends ServerIn."""
    id: int
    status: str = "unknown"