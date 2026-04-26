import json
import os

from .models import Diagnosis, OptimizationResult
from .prompts import DIAGNOSIS_PROMPT, REWRITE_PROMPT, SYSTEM_PROMPT


class ResumeOptimizerAgent:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        try:
            from openai import OpenAI  # type: ignore
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError("缺少依赖 openai，请先执行: pip install -r requirements.txt") from exc
        self.client = OpenAI()

    def _chat_json(self, prompt: str, schema_name: str) -> dict:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "gaps": {"type": "array", "items": {"type": "string"}},
                            "missing_keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "rewrite_strategy": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "optimized_resume_markdown": {"type": "string"},
                            "interview_talking_points": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": [
                            "strengths",
                            "gaps",
                            "missing_keywords",
                            "rewrite_strategy",
                            "optimized_resume_markdown",
                            "interview_talking_points",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
        )
        return json.loads(response.output_text)

    def diagnose(self, resume_text: str, jd_text: str) -> Diagnosis:
        prompt = DIAGNOSIS_PROMPT.format(resume_text=resume_text, jd_text=jd_text)
        raw = self._chat_json(prompt, schema_name="resume_diagnosis_and_rewrite")
        return Diagnosis(
            strengths=raw["strengths"],
            gaps=raw["gaps"],
            missing_keywords=raw["missing_keywords"],
            rewrite_strategy=raw["rewrite_strategy"],
        )

    def optimize(self, resume_text: str, jd_text: str) -> OptimizationResult:
        diagnosis = self.diagnose(resume_text, jd_text)
        prompt = REWRITE_PROMPT.format(
            diagnosis_json=diagnosis.model_dump_json(indent=2),
            resume_text=resume_text,
            jd_text=jd_text,
        )
        raw = self._chat_json(prompt, schema_name="resume_diagnosis_and_rewrite")
        return OptimizationResult(
            diagnosis=diagnosis,
            optimized_resume_markdown=raw["optimized_resume_markdown"],
            interview_talking_points=raw["interview_talking_points"],
        )
