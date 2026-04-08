from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: str


class AnalysisReport(BaseModel):
    sector: str
    generated_at: str
    report: str
    sources: list[str]
    cached: bool


class ErrorResponse(BaseModel):
    error: str
    detail: str