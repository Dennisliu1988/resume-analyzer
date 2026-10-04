<!-- 项目功能
启动步骤
API 文档
技术栈
架构说明 -->

# 简历分析服务

基于 LangChain 的简历分析服务，支持 DeepSeek 大模型，提供技能提取、岗位匹配、面试问题生成等功能。

## 项目功能

- 技能提取：从简历中自动提取技能，并评估掌握程度
- 岗位匹配：分析简历与岗位描述的匹配度
- 面试准备：生成针对性面试问题
- 流式响应：支持实时输出，提升用户体验
- 可插拔架构：支持轻松切换不同的 LLM 提供商
- 错误重试：自动重试 3 次，提高稳定性

## 启动步骤

1. **安装依赖**
```bash
pip install langchain langchain-community httpx pydantic
```

2. **配置环境变量**
在项目根目录创建 `.env` 文件（或者直接在系统环境变量中配置）：
```bash
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_api_key_here
```

3. **运行服务**
```bash
uv run app.server
```

服务将在 `http://[IP_ADDRESS]` 启动。

## API 文档

### 技能提取
**POST /skills**

提取简历中的技能信息。

**Request:**
```json
{
  "resume_text": "求职者拥有 5 年 Java 开发经验..."
}
```

**Response:**
```json
{
  "skills": [
    {
      "name": "Python",
      "level": "强",
      "evidence": ["精通 Python Web 开发..."]
    }
  ]
}
```

### 岗位匹配
**POST /match**

分析简历与岗位的匹配度。

**Request:**
```json
{
  "resume_text": "求职者拥有 5 年 Java 开发经验...",
  "job_description": "需要有 3 年以上 Java 经验..."
}
```

**Response:**
```json
{
  "match_score": 85,
  "summary": "整体匹配度较高...",
  "skill_matches": [
    {
      "skill": "Java",
      "match_level": "强",
      "evidence": ["有 5 年 Java 开发经验"]
    }
  ],
  "suggestions": ["建议补充 Spring Boot 经验"]
}
```

### 面试问题生成
**POST /interview**

生成面试问题。

**Request:**
```json
{
  "resume_text": "求职者拥有 5 年 Java 开发经验...",
  "job_description": "需要有 3 年以上 Java 经验..."
}
```

**Response:**
```json
{
  "questions": [
    {
      "type": "tech",
      "question": "请介绍一下你在 Java 开发方面的经验..."
    }
  ]
}
```

### 流式 API
- `POST /skills/stream`
- `POST /match/stream`
- `POST /interview/stream`

支持流式输出，每个 Chunk 格式为：
```json
{
  "partial_data": "..."
}
```

## 技术栈

- **语言**：Python 3.8+
- **框架**：FastAPI
- **LLM 编排**：LangChain
- **LLM 提供商**：DeepSeek
- **数据模型**：Pydantic
- **HTTP 客户端**：httpx
- **配置管理**：python-dotenv

## 架构说明

### 模块化设计

项目采用模块化架构，主要包含以下模块：

- **app/server.py**：FastAPI 应用入口，提供 RESTful API 接口
- **app/services/analyzer.py**：核心分析逻辑，封装 LangChain 调用
- **app/providers/**：LLM 提供商抽象层
  - **base.py**：通用接口定义
  - **deepseek.py**：DeepSeek 实现
- **app/prompts/**：提示词管理
- **app/models.py**：数据模型定义
- **app/utils.py**：工具函数
- **app/config.py**：配置管理

### 接口设计

API 接口设计遵循 RESTful 原则，支持同步和流式两种方式：

```
/skills → 技能提取
/skills/stream → 技能提取（流式）
/match → 岗位匹配
/match/stream → 岗位匹配（流式）
/interview → 面试问题生成
/interview/stream → 面试问题生成（流式）
```

### 配置体系

支持通过环境变量配置不同的 LLM 提供商：

```python
# app/config.py
# 从环境变量中自动选择提供商
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
```

通过配置中心可以方便地添加新的 LLM 提供商，只需实现 `LLMProvider` 接口并添加到 `PROVIDERS` 映射中。

### 错误处理

- **API 错误**：使用 `httpx.HTTPStatusError` 统一处理 HTTP 错误
- **模型错误**：使用 `try/except` 捕获 LLM 调用错误
- **流式错误**：流式生成器使用 `try/except` 捕获异常并中止生成
- **重试机制**：主要分析功能支持自动重试 3 次

## 扩展性

为了支持新的 LLM 提供商（如 OpenAI、Azure、文心一言等），只需完成以下步骤：

1. **实现 `LLMProvider` 接口**
   在 `app/providers/` 目录下创建新模块，实现 `chat` 和 `stream_chat` 方法

2. **更新配置**
   将新的提供商添加到 `app/config.py` 中的 `PROVIDERS` 映射

3. **更新提示词（可选）**
   如果新模型需要不同的提示词格式，可以在 `app/prompts/` 中创建新的提示词文件

4. **测试**
   更新 `.env` 文件中的 `LLM_PROVIDER` 配置，启动服务并测试新提供商

## 注意事项

- 确保已安装所有依赖：`pip install -r requirements.txt`
- 必须配置 `DEEPSEEK_API_KEY` 环境变量
- 流式响应使用 `Server-Sent Events` (SSE)，前端需正确处理
- 所有模型输出都经过 JSON 验证，确保数据质量

## 运行截图

### 技能提取
![技能提取](screenshots/skill_extraction.png)

### 岗位匹配
![岗位匹配](screenshots/job_match.png)

### 面试问题
![面试问题](screenshots/interview_questions.png)

## 项目结构

```
resume-analyzer/
├── app/
│   ├── __init__.py
│   ├── server.py             # FastAPI 入口
│   ├── config.py             # 配置管理
│   ├── models.py             # 数据模型
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py           # 抽象接口
│   │   ├── deepseek.py       # DeepSeek 实现
│   ├── prompts/
│   │   ├── skill_extraction.py
│   │   ├── job_match.py
│   │   ├── interview_questions.py
│   ├── services/
│   │   ├── analyzer.py       # 核心分析逻辑
│   └── utils.py              # 工具函数
├── .env                        # 环境变量（示例）
├── requirements.txt
├── README.md
└── screenshots/
    ├── skill_extraction.png
    ├── job_match.png
    └── interview_questions.png
```

## 授权

这是一个开源项目，你可以自由使用、修改和分发。
