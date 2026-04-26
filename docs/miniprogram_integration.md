# 微信小程序接入方案（简历优化助手）

## 目标

把当前 `ResumeOptimizerAgent` 封装成 HTTP API，再由微信小程序调用。

## 架构

1. 小程序端：采集简历文本、JD 文本。
2. 后端 API：调用 `ResumeOptimizerAgent.optimize()`。
3. 对象存储（可选）：存储历史优化结果。

## 建议 API

- `POST /api/optimize`
  - 入参：
    - `resume_text: string`
    - `jd_text: string`
    - `model?: string`
  - 出参：
    - `diagnosis`
    - `optimized_resume_markdown`
    - `interview_talking_points`

## 小程序端页面建议

- 首页：输入简历/JD + 开始优化按钮
- 结果页：
  - 诊断标签
  - 优化后简历（可复制）
  - 面试话术（可复制）

## 安全注意

- 小程序不要直连 OpenAI；API Key 仅存后端。
- 对请求做频控、鉴权（如用户 token + 每日配额）。
- 对文本进行敏感信息掩码与日志脱敏。

