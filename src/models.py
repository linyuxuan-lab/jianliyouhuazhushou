from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    strengths: list[str] = Field(default_factory=list, description="简历优势")
    gaps: list[str] = Field(default_factory=list, description="与JD的差距")
    missing_keywords: list[str] = Field(default_factory=list, description="缺失关键词")
    rewrite_strategy: list[str] = Field(default_factory=list, description="改写策略")


class OptimizationResult(BaseModel):
    diagnosis: Diagnosis
    optimized_resume_markdown: str
    interview_talking_points: list[str] = Field(default_factory=list)
