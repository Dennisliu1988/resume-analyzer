# Pydantic 模型
# 简历分析响应数据模型
from pydantic import BaseModel

class SkillAnalysis(BaseModel):
    skill: str
    match_level: str          # "强" / "中" / "弱"
    evidence: list[str]     # 证据语句列表

class JobMatchResult(BaseModel):
    match_score: int          # 0-100
    summary: str              # 简短分析
    skill_matches: list[SkillAnalysis]
    suggestions: list[str]