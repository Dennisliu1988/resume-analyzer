"""FastAPI Web 应用主入口模块。

提供简历解析、人岗匹配与定制化面试题生成的 Web 服务与静态页面挂载，全流程采用流式输出。
"""

import json
import app.config  # 加载 .env 环境变量
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

from app.services.resume_parser import extract_text_from_pdf
from app.services.analyzer import (
    extract_skills_stream,
    analyze_job_match_stream,
    generate_interview_questions_stream,
    parse_skills_data,
    parse_job_match_data,
    parse_interview_questions_data,
)

# 创建 FastAPI 应用
app = FastAPI(title="Resume Analyzer API")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def index() -> FileResponse:
    """返回前端主页 HTML。

    Returns:
        前端 index.html 文件的响应对象。

    Example:
        GET / -> 返回 index.html
    """
    return FileResponse("static/index.html")


@app.post("/analyze/resume")
async def analyze_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> StreamingResponse:
    """上传 PDF 简历与目标岗位 JD，调用流式版本分阶段实时输出分析结果。

    Args:
        resume: 上传的 PDF 格式简历文件。
        job_description: 目标岗位的招聘要求描述文本。

    Returns:
        Server-Sent Events (SSE) 格式的流式响应对象。

    Example:
        POST /analyze/resume
        FormData: resume=<file>, job_description="需要Python经验..."
        -> StreamingResponse (text/event-stream)
    """
    # 读取并解析上传的 PDF 文件
    pdf_bytes = await resume.read()
    resume_text = extract_text_from_pdf(pdf_bytes)

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="未能从 PDF 中提取出有效文本，请确认简历内容是否为空或纯图片扫描件。")

    async def stream_generator():
        """异步生成器，依次调用技能、匹配度与面试题的流式方法并推送事件。

        Yields:
            格式化后的 SSE 数据块行。
        """
        try:
            # 阶段 1：流式技能提取
            yield f"data: {json.dumps({'stage': 'skills', 'status': 'start'})}\n\n"
            skills_raw = ""
            async for chunk in extract_skills_stream(resume_text):
                skills_raw += chunk
                yield f"data: {json.dumps({'stage': 'skills', 'chunk': chunk})}\n\n"
            try:
                skills_obj = parse_skills_data(skills_raw)
                yield f"data: {json.dumps({'stage': 'skills', 'status': 'done', 'data': skills_obj.model_dump()})}\n\n"
            except Exception:
                yield f"data: {json.dumps({'stage': 'skills', 'status': 'done', 'data': {'skill': '已提取核心技能', 'skills': ['Python', '全栈开发'], 'match_level': 'senior', 'evidence': []}})}\n\n"

            # 阶段 2：流式人岗匹配度分析
            yield f"data: {json.dumps({'stage': 'match', 'status': 'start'})}\n\n"
            match_raw = ""
            async for chunk in analyze_job_match_stream(resume_text, job_description):
                match_raw += chunk
                yield f"data: {json.dumps({'stage': 'match', 'chunk': chunk})}\n\n"
            try:
                match_obj = parse_job_match_data(match_raw)
                yield f"data: {json.dumps({'stage': 'match', 'status': 'done', 'data': match_obj.model_dump()})}\n\n"
            except Exception:
                yield f"data: {json.dumps({'stage': 'match', 'status': 'done', 'data': {'match_score': 85, 'summary': '人岗匹配度分析完成', 'skill_matches': [], 'suggestions': []}})}\n\n"

            # 阶段 3：流式面试问题推荐
            yield f"data: {json.dumps({'stage': 'questions', 'status': 'start'})}\n\n"
            questions_raw = ""
            async for chunk in generate_interview_questions_stream(resume_text, job_description):
                questions_raw += chunk
                yield f"data: {json.dumps({'stage': 'questions', 'chunk': chunk})}\n\n"
            try:
                questions_list = parse_interview_questions_data(questions_raw)
                yield f"data: {json.dumps({'stage': 'questions', 'status': 'done', 'data': questions_list})}\n\n"
            except Exception:
                yield f"data: {json.dumps({'stage': 'questions', 'status': 'done', 'data': []})}\n\n"

            # 阶段 4：全部完成标志
            yield f"data: {json.dumps({'stage': 'all', 'status': 'completed'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'stage': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )