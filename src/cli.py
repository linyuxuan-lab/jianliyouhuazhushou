import argparse
import json
from pathlib import Path



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="简历优化助手 CLI")
    parser.add_argument("--resume-file", required=True, help="原始简历文件路径")
    parser.add_argument("--jd-file", required=True, help="目标 JD 文件路径")
    parser.add_argument("--output-dir", default="output", help="输出目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    resume_text = Path(args.resume_file).read_text(encoding="utf-8")
    jd_text = Path(args.jd_file).read_text(encoding="utf-8")

    from .resume_agent import ResumeOptimizerAgent

    agent = ResumeOptimizerAgent()
    result = agent.optimize(resume_text=resume_text, jd_text=jd_text)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "diagnosis.json").write_text(
        json.dumps(result.diagnosis.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "optimized_resume.md").write_text(
        result.optimized_resume_markdown,
        encoding="utf-8",
    )
    (output_dir / "interview_points.md").write_text(
        "\n".join(f"- {p}" for p in result.interview_talking_points),
        encoding="utf-8",
    )

    print(f"已输出到: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
