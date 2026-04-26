# 简历优化助手 Agent（MVP）

这是一个可直接启动的 **简历优化助手** 项目骨架，目标是帮助用户把原始简历按目标 JD（岗位描述）进行优化，并输出可投递版本。

## MVP 能力

- 输入：原始简历（Markdown / 纯文本）+ 目标 JD
- 输出：
  - 诊断报告（缺失技能、关键词覆盖、量化不足项）
  - 优化后简历（ATS 友好）
  - 面试补充材料（项目亮点与 STAR 话术）
- 支持一键导出 Markdown 文件

## 项目结构

```text
.
├── README.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── cli.py
    ├── models.py
    ├── prompts.py
    └── resume_agent.py
```

## 快速开始

1. 安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 配置环境变量：

```bash
export OPENAI_API_KEY="你的 Key"
# 可选
export OPENAI_MODEL="gpt-4.1-mini"
```

3. 运行：

```bash
python -m src.cli \
  --resume-file examples/resume.md \
  --jd-file examples/jd.md \
  --output-dir output
```

## 设计要点

- **结构化输入输出**：使用 Pydantic 对结果进行结构化，方便前端展示。
- **双阶段生成**：
  1) 诊断问题；2) 根据诊断重写简历，降低幻觉风险。
- **安全策略**：明确要求“不得编造经历、不得虚构指标”，只允许改写表达。
- **可扩展性**：后续可接入 PDF 解析、打分器（rubric）、多轮对话澄清。

## 下一步建议

- 增加 Web UI（Streamlit / Next.js）
- 增加简历评分器（ATS 命中率、量化密度、动词强度）
- 增加多版本输出（校招版、社招版、管理岗版）



## 网页版（Streamlit）

安装依赖后可直接启动网页：

```bash
streamlit run src/web_app.py
```

打开浏览器后即可在页面中输入简历和 JD，并下载优化后的 Markdown 简历。

## 微信小程序落地

已经提供小程序接入建议文档：

- `docs/miniprogram_integration.md`
