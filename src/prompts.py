SYSTEM_PROMPT = """
你是资深招聘顾问与简历优化专家。
目标：在不伪造经历和数据的前提下，提升候选人简历与JD匹配度和可读性。
规则：
1. 严禁编造公司、项目、职位、年份和指标。
2. 优先保留事实，只优化表达与结构。
3. 输出需ATS友好：清晰标题、关键词覆盖、动词开头、量化导向。
""".strip()

DIAGNOSIS_PROMPT = """
请分析下面的简历和JD，输出：
- strengths: 简历优势（3-8条）
- gaps: 与JD的差距（3-8条）
- missing_keywords: 缺失关键词（5-20个）
- rewrite_strategy: 可执行改写策略（5-12条）

简历：
{resume_text}

JD：
{jd_text}
""".strip()

REWRITE_PROMPT = """
基于诊断结果，改写简历为 ATS 友好的 Markdown 版本。
要求：
- 不新增虚构经历
- 项目描述尽量“动词 + 任务 + 方法 + 结果”
- 尽可能将已有事实量化
- 与JD关键词自然对齐

诊断结果：
{diagnosis_json}

原始简历：
{resume_text}

目标JD：
{jd_text}

请同时输出：
1) optimized_resume_markdown
2) interview_talking_points（3-8条）
""".strip()
