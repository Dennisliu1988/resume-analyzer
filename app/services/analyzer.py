import json
import re
from typing import Any, AsyncGenerator, Dict, List

from app.providers import get_provider
from app.models import SkillAnalysis, JobMatchResult
from app.prompts.skill_extraction import SKILL_EXTRACTION_PROMPT
from app.prompts.job_match import JOB_MATCH_PROMPT
from app.prompts.interview_questions import INTERVIEW_QUESTIONS_PROMPT


# 清理大模型输出的 JSON 文本
def clean_json_text(text: str) -> str:
    cleaned = text.strip()
    # 优先匹配 Markdown 代码块中的内容
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        cleaned = match.group(1).strip()
    
    # 进一步提取最外层的 JSON 对象 { ... } 或数组 [ ... ]，剔除前后闲话
    obj_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
    if obj_match:
        return obj_match.group(1).strip()
    return cleaned

# 解析大模型输出的技能分析 JSON 文本
def parse_skills_data(raw_text: str) -> SkillAnalysis:
    cleaned = clean_json_text(raw_text)
    data: Dict[str, Any] = json.loads(cleaned)

    # 字段适配：以 models.py 为准
    if "skill" not in data and "skills" in data:
        skills_val = data["skills"]
        data["skill"] = "、".join(skills_val) if isinstance(skills_val, list) else str(skills_val)

    if isinstance(data.get("evidence"), str):
        data["evidence"] = [data["evidence"]] if data["evidence"] else []

    return SkillAnalysis.model_validate(data)

# 解析大模型输出的人岗匹配 JSON 文本
def parse_job_match_data(raw_text: str) -> JobMatchResult:
    cleaned = clean_json_text(raw_text)
    data: Dict[str, Any] = json.loads(cleaned)
    return JobMatchResult.model_validate(data)

# 解析大模型输出的面试问题 JSON 文本
def parse_interview_questions_data(raw_text: str) -> List[Dict[str, Any]]:
    cleaned = clean_json_text(raw_text)
    data = json.loads(cleaned)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "questions" in data and isinstance(data["questions"], list):
        return data["questions"]
    return [data]


# ==================== 非流式输出版本 ====================

def safe_format_prompt(template: str, **kwargs) -> str:
    """安全填充提示词模板变量，避免 JSON 大括号导致的 KeyError。

    Args:
        template: 提示词模板文本。
        **kwargs: 待替换的变量键值对。

    Returns:
        填充后的完整提示词。
    """
    res = template
    for key, val in kwargs.items():
        res = res.replace(f"{{{key}}}", str(val))
    return res


# ==================== 非流式输出版本 ====================

async def extract_skills(resume_text: str) -> SkillAnalysis:
    """从简历文本中提取候选人技能画像信息。"""
    provider = get_provider()
    prompt = safe_format_prompt(SKILL_EXTRACTION_PROMPT, resume=resume_text, resume_text=resume_text)
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(3):
        raw = await provider.chat(messages)
        try:
            return parse_skills_data(raw)
        except Exception as e:
            if attempt == 2:
                raise ValueError(f"提取技能失败: {e}，原始返回: {raw}")
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"输出格式错误：{e}。请修正后严格仅输出标准 JSON。"})


async def analyze_job_match(resume_text: str, job_description: str) -> JobMatchResult:
    """分析简历与岗位描述的匹配程度。"""
    provider = get_provider()
    prompt = safe_format_prompt(JOB_MATCH_PROMPT, resume=resume_text, resume_text=resume_text, job_description=job_description)
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(3):
        raw = await provider.chat(messages)
        try:
            return parse_job_match_data(raw)
        except Exception as e:
            if attempt == 2:
                raise ValueError(f"匹配度分析失败: {e}，原始返回: {raw}")
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"输出格式错误：{e}。请修正后严格仅输出标准 JSON。"})


async def generate_interview_questions(resume_text: str, job_description: str) -> List[Dict[str, Any]]:
    """根据候选人简历背景与目标岗位要求，生成针对性的面试问题。"""
    provider = get_provider()
    prompt = safe_format_prompt(INTERVIEW_QUESTIONS_PROMPT, resume=resume_text, resume_text=resume_text, job_description=job_description)
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(3):
        raw = await provider.chat(messages)
        try:
            return parse_interview_questions_data(raw)
        except Exception as e:
            if attempt == 2:
                raise ValueError(f"生成面试题失败: {e}，原始返回: {raw}")
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"输出格式错误：{e}。请修正后严格仅输出标准 JSON 数组。"})


# ==================== 流式输出版本 ====================

async def extract_skills_stream(resume_text: str) -> AsyncGenerator[str, None]:
    provider = get_provider()
    prompt = safe_format_prompt(SKILL_EXTRACTION_PROMPT, resume=resume_text, resume_text=resume_text)
    messages = [{"role": "user", "content": prompt}]
    async for chunk in provider.stream_chat(messages):
        yield chunk


async def analyze_job_match_stream(resume_text: str, job_description: str) -> AsyncGenerator[str, None]:
    provider = get_provider()
    prompt = safe_format_prompt(JOB_MATCH_PROMPT, resume=resume_text, resume_text=resume_text, job_description=job_description)
    messages = [{"role": "user", "content": prompt}]
    async for chunk in provider.stream_chat(messages):
        yield chunk


async def generate_interview_questions_stream(resume_text: str, job_description: str) -> AsyncGenerator[str, None]:
    provider = get_provider()
    prompt = safe_format_prompt(INTERVIEW_QUESTIONS_PROMPT, resume=resume_text, resume_text=resume_text, job_description=job_description)
    messages = [{"role": "user", "content": prompt}]
    async for chunk in provider.stream_chat(messages):
        yield chunk