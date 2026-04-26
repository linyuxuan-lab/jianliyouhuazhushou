from __future__ import annotations

import traceback

import streamlit as st

from .resume_agent import ResumeOptimizerAgent


def run() -> None:
    st.set_page_config(page_title="简历优化助手", page_icon="📄", layout="wide")
    st.title("📄 简历优化助手")
    st.caption("输入原始简历与岗位 JD，一键生成诊断与优化版简历。")

    with st.sidebar:
        st.header("参数")
        model = st.text_input("模型", value="gpt-4.1-mini")
        st.markdown("---")
        st.write("说明：需要先在运行环境配置 `OPENAI_API_KEY`。")

    col1, col2 = st.columns(2)
    with col1:
        resume_text = st.text_area("原始简历", height=360, placeholder="粘贴你的简历内容...")
    with col2:
        jd_text = st.text_area("目标 JD", height=360, placeholder="粘贴目标岗位描述...")

    if st.button("开始优化", type="primary"):
        if not resume_text.strip() or not jd_text.strip():
            st.error("请先填写简历和 JD。")
            return

        try:
            with st.spinner("正在分析并改写，请稍候..."):
                agent = ResumeOptimizerAgent(model=model.strip() or None)
                result = agent.optimize(resume_text=resume_text, jd_text=jd_text)

            st.success("优化完成")

            st.subheader("诊断结果")
            st.json(result.diagnosis.model_dump())

            st.subheader("优化后简历（Markdown）")
            st.code(result.optimized_resume_markdown, language="markdown")

            st.download_button(
                label="下载优化后简历",
                data=result.optimized_resume_markdown,
                file_name="optimized_resume.md",
                mime="text/markdown",
            )

            points_md = "\n".join(f"- {x}" for x in result.interview_talking_points)
            st.subheader("面试亮点话术")
            st.markdown(points_md)

        except Exception as exc:  # noqa: BLE001
            st.error(f"执行失败：{exc}")
            st.code(traceback.format_exc(), language="text")


if __name__ == "__main__":
    run()
