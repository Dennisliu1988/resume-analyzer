SKILL_EXTRACTION_PROMPT = """你是一名资深招聘专家，擅长从简历中快速提取技能信息。

示例1：
简历：5年React经验，精通TypeScript，熟悉Node.js
输出：{{"skills": ["React", "TypeScript", "Node.js"], "match_level": "senior", "evidence": "5年React经验"}}

示例2：
简历：2年Vue经验，了解JavaScript
输出：{{"skills": ["Vue", "JavaScript"], "match_level": "junior", "evidence": "2年Vue经验"}}

任务：从以下简历中提取技能信息。

判断标准：
- skills: 提取所有技术栈关键词
- match_level: 根据技能对应的经验年限，0-2年为junior，3-5年为mid，5年以上为senior
- evidence: 提取匹配的证据

限制：
- 只输出 JSON，不要有其他内容
- 不要编造简历中没有的信息
- 如果信息不足，match_level 输出 0，evidence 输出 ''

简历：
{resume}

只输出 JSON：
"""