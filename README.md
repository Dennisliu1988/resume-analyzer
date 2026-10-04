# ResumeAI - 智能简历分析与人岗匹配诊断系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?logo=tailwind-css&logoColor=white)
![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9?logo=astral&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**基于大语言模型（LLM）的全栈智能招聘评估工具，支持原生 PDF 简历解析、技能图谱提取、人岗契合度诊断与定制化面试题生成。**

[快速开始](#-快速启动指南) • [核心特性](#-核心特性) • [系统架构](#-系统架构与工作流程) • [API 文档](#-api-接口参考) • [常见问题](#-常见问题--排错指南)

</div>

---

## 📖 项目简介

**ResumeAI** 是一款专为技术招聘、HR 专家、猎头及工程管理者打造的 AI 智能简历评估与人岗匹配系统。

在传统招聘流程中，人工筛选简历耗时长、评估标准易受主观偏好影响，且难以针对具体岗位的技能差（Skill Gap）精准定制面试考题。ResumeAI 通过解析求职者 PDF 简历与目标岗位 JD（Job Description），结合深度结构化提示词与主流大语言模型（支持 DeepSeek / 阿里通义千问 Qwen 等），提供**全流程实时流式（Server-Sent Events, SSE）**的人岗匹配度分析报告与定制化面试提问方案。

前端采用现代化精美 UI 仪表盘（原生 HTML5 + Fetch 流式读取 + Tailwind CSS），无需繁重的 Node.js 打包构建流程，轻量开箱即用。

---

## ✨ 核心特性

- 📄 **原生 PDF 简历快速解析**：基于 `pypdf` 快速、精准提取 PDF 格式简历中的结构化纯文本内容，过滤空白噪声。
- 🎯 **候选人技能图谱自动归纳**：
  - **技术标签云**：智能提取技能关键词（保全复合专有名词如 `Vue 3`、`Element Plus`、`RESTful API` 等，杜绝碎片化拆词）。
  - **核心专长定位**：自动归纳候选人的主要技术领域与综合职级定位（Junior / Mid / Senior）。
  - **履历证据链（Evidence）**：从简历中提取具体事实依据，确保评估结果真实可追溯。
- 📊 **多维度人岗匹配度诊断**：
  - **综合匹配指数**：0-100 分量化评分仪表盘与评级徽章（高匹配 / 良好匹配 / 一般匹配）。
  - **匹配评价摘要**：清晰阐明候选人技术优势、业务短板与岗位契合点。
  - **核心技能匹配矩阵**：逐项给出“强 / 中 / 弱”等级评定与简历上下文证据。
  - **针对性提升建议**：为面试官和候选人提供重点考察方向与技能提升路径。
- 💡 **AI 定制化分级面试题**：
  - 根据候选人实际项目经历与目标岗位技术差（Gap），分级生成“基础、进阶、行为”三大维度的问题。
  - 每道题目均附带**考察初衷（Why Asked）**，帮助面试官快速洞悉候选人底层原理与技术深度。
- ⚡ **全链路 SSE 实时流式打字机体验**：
  - 基于 Server-Sent Events（FastAPI `StreamingResponse`）分阶段打字机推送。
  - 界面提供专属深色终端控制台，实时滚动展示大模型推理过程中的 Token 流，大幅降低等待焦虑。
- 🔌 **可插拔的多模型 Provider 架构**：
  - 抽象统一 `LLMProvider` 基类，支持通过环境变量自由切换 `deepseek` / `qwen`。
  - 内置完善的 JSON 代码块清洗与安全占位符替换机制（`safe_format_prompt`），杜绝格式解析报错。


---

## 🛠️ 技术栈

| 层次            | 技术选型                         | 说明                                                       |
| :-------------- | :------------------------------- | :--------------------------------------------------------- |
| **语言环境**    | Python 3.12+                     | 现代化强类型注解与原生异步协程支持                         |
| **包管理工具**  | Astral `uv`                      | Rust 驱动的高性能 Python 依赖管理工具                      |
| **后端框架**    | FastAPI + Uvicorn                | 高并发异步 ASGI Web 服务框架                               |
| **数据建模**    | Pydantic v2                      | 严格的请求/响应参数校验与结构体规范                        |
| **PDF 解析**    | pypdf (v6.x)                     | 纯 Python 实现的轻量 PDF 文本提取库                        |
| **HTTP 客户端** | httpx                            | 异步流式 HTTP 客户端，支持 SSE 流读取与大模型通信          |
| **前端交互**    | 原生 HTML5 + Fetch + EventStream | 零打包配置、轻量快速、原生流式分块读取                     |
| **UI 样式设计** | Tailwind CSS (CDN) + Inter 字体  | 现代化科技感暗浅渐变、双列排版、卡片悬浮与自适应响应式布局 |

---

## 📁 目录结构

```text
resume-analyzer/
├── app/
│   ├── __init__.py
│   ├── config.py                  # 配置管理（自动读取加载 .env 环境变量）
│   ├── main.py                    # FastAPI 核心入口、静态文件挂载、SSE 流式路由
│   ├── models.py                  # Pydantic 数据模型定义（SkillAnalysis, JobMatchResult）
│   ├── prompts/                   # 领域提示词设计（Prompt Templates）
│   │   ├── __init__.py
│   │   ├── skill_extraction.py    # 候选人技能提取 Prompt
│   │   ├── job_match.py           # 人岗契合度分析与量化评分 Prompt
│   │   └── interview_questions.py # 分级定制面试题生成 Prompt
│   ├── providers/                 # LLM 服务提供商适配层（可插拔设计）
│   │   ├── __init__.py            # Provider 工厂函数 (get_provider)
│   │   ├── base.py                # LLMProvider 抽象基类
│   │   ├── deepseek.py            # DeepSeek API 实现（支持普通与流式）
│   │   └── qwen.py                # 通义千问 Qwen API 实现（支持普通与流式）
│   └── services/                  # 核心业务逻辑服务
│       ├── __init__.py
│       ├── analyzer.py            # 分析流程编排、Prompt 安全格式化、JSON 提取清洗
│       └── resume_parser.py       # PDF 文件验证与文本提取服务
├── static/
│   └── index.html                 # 前端单页应用（仪表盘、拖拽上传、流式控制台）
├── .env                           # 运行期本地环境变量配置（已加入 .gitignore）
├── .env.example                   # 环境变量配置示例模板
├── pyproject.toml                 # uv 项目配置与依赖清单
├── uv.lock                        # 锁定的依赖版本信息
└── README.md                      # 项目完整说明文档
```

---

## 🚀 快速启动指南

### 1. 环境准备

确保您的本地计算机已安装 **Python 3.12+**。推荐使用现代化的 Python 包管理工具 **[uv](https://github.com/astral-sh/uv)**。

安装 `uv`（如果尚未安装）：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 克隆项目与安装依赖

```bash
# 1. 克隆代码仓库并进入项目根目录
cd resume-analyzer

# 2. 使用 uv 一键同步并安装全部依赖
uv sync
```

*(如果偏好使用传统 pip，请执行：`pip install fastapi uvicorn pypdf httpx python-dotenv pydantic python-multipart`)*

### 3. 配置环境变量

在项目根目录下复制 `.env.example` 为 `.env`：

```bash
# Linux / macOS
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env
```

打开 `.env` 文件，填写您的大模型 API Key，并指定当前生效的提供商：

```env
# 默认使用的大模型提供商: deepseek 或 qwen
LLM_PROVIDER=deepseek

# DeepSeek 官方 API Key (可在 https://platform.deepseek.com 申请)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 阿里通义千问 API Key (可在 https://dashscope.console.aliyun.com 申请)
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. 启动开发服务器

通过 `uv` 启动支持代码热重载（Hot-reload）的 Uvicorn 服务：

```bash
uv run uvicorn app.main:app --reload
```

服务启动后，终端将输出如下信息：

```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

### 5. 访问与使用

- **前端交互界面**：打开浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API 交互式文档 (Swagger)**：访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **备用 API 文档 (ReDoc)**：访问 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🖥️ 功能操作与使用演示

1. **上传简历**：
   - 将求职者的 `.pdf` 格式简历拖拽至左侧上传区域，或点击上传框从本地选择文件。
2. **填写岗位需求（JD）**：
   - 在“目标职位描述 (JD)”文本框中粘贴招聘要求与岗位说明。
   - 也可以直接点击文本框右上角的**“填入测试JD”**按钮，自动载入预设的高级前端开发工程师岗位范本。
3. **启动深度分析**：
   - 点击**“开始深度分析”**按钮，前端将发起流式长连接请求。
4. **实时流式反馈**：
   - 界面上方的步骤指示器实时更新当前运行阶段（`1. 提取技能` ➔ `2. 岗位匹配` ➔ `3. 定制考题`）。
   - 右侧“实时分析日志”深色终端以打字机模式实时呈现大语言模型推理输出的每一个 Token。
5. **多维诊断报告交互**：
   - **综合匹配指数**：位于右侧诊断卡片顶部右侧，显示量化分数与“良好匹配/一般匹配”徽章。
   - **匹配评价摘要**：提炼求职者的核心竞争力与短板。
   - **核心技能匹配矩阵**：采用双列卡片自适应排版，展示各项技能的强弱度及履历证据。
   - **候选人技能图谱**：横向铺展展示技能分类、精通级别及完整的技能技术标签。
   - **AI 定制面试题**：按照“基础 / 进阶 / 行为”维度列出定制考题，并附带面试官考核意图。
   - **原始数据抽屉**：开发者可点击底部的“查看完整返回数据”折叠面板查验结构化 JSON 数据。

---

## 📡 API 接口参考

### 1. 简历与岗位深度分析（SSE 流式传输）

- **请求路径**：`POST /analyze/resume`
- **请求格式**：`multipart/form-data`
- **响应格式**：`text/event-stream; charset=utf-8`

#### 请求参数 (Form Data)

| 字段名            | 类型                  | 必填 | 描述                      |
| :---------------- | :-------------------- | :--- | :------------------------ |
| `resume`          | `UploadFile` (binary) | 是   | 候选人的 PDF 格式简历文件 |
| `job_description` | `string`              | 是   | 招聘岗位的描述文本与要求  |

#### SSE 事件流协议定义

后端按分析阶段依次推送以下数据格式：

##### ① 阶段开始事件 (`start`)
```json
{
  "stage": "skills",
  "status": "start"
}
```

##### ② 内容分块推送 (`chunk`)
```json
{
  "stage": "skills",
  "chunk": "{\"skill\": \"前端开发\"..."
}
```

##### ③ 阶段完成与数据装载 (`done`)
```json
{
  "stage": "skills",
  "status": "done",
  "data": {
    "skill": "Vue 3、TypeScript、Node.js、微前端",
    "skills": ["Vue 3", "TypeScript", "Node.js", "微前端"],
    "match_level": "senior",
    "evidence": ["10年大型企业级 SaaS 与高可用前端架构经验"]
  }
}
```

##### ④ 全部分析完成事件 (`completed`)
```json
{
  "stage": "all",
  "status": "completed"
}
```

---

## 🧬 数据模型定义 (Pydantic v2)

项目在 `app/models.py` 中严格定义了数据契约：

### 1. `SkillAnalysis`
```python
class SkillAnalysis(BaseModel):
    skill: str              # 技能名称或技能综述
    match_level: str        # 匹配等级: "强" / "中" / "弱" 或 "junior" / "mid" / "senior"
    evidence: list[str]     # 简历中的具体事实佐证列表
```

### 2. `JobMatchResult`
```python
class JobMatchResult(BaseModel):
    match_score: int                   # 0-100 的综合匹配量化得分
    summary: str                       # 整体人岗匹配评估摘要
    skill_matches: list[SkillAnalysis] # 岗位核心技能逐项比对列表
    suggestions: list[str]             # 面试官重点考察建议与提升方向
```

### 3. 面试问题结构
```json
[
  {
    "category": "进阶",
    "question": "在微前端架构下，您是如何处理主应用与子应用间的全局状态同步与 CSS 样式隔离的？",
    "why_asked": "候选人简历提到微前端落地经验，针对目标岗位的工程化要求进行深度原理考察。"
  }
]
```

---

## 💡 核心设计与工程实践

1. **提示词安全格式化 (`safe_format_prompt`)**：
   - 避免直接使用 Python 原生 `str.format()` 引起复杂的 JSON 格式大括号转义异常（`KeyError`）。
   - 采用安全的子串精准替换算法，确保大语言模型能 100% 稳定输出标准 JSON。
2. **健壮的 Markdown JSON 提取机制 (`clean_json_text`)**：
   - 模型在流式或非流式输出时经常夹带 ````json ... ```` 代码块标签或思考过程。
   - 系统内置正则提取器与最外层括号定位逻辑，自动修剪无关文本，保障 `json.loads()` 的高解析成功率。
3. **复合专有名词保留算法**：
   - 针对中文招聘场景常见的复合技术栈专有名词（如 `Vue 3`、`Element Plus`、`Spring Boot` 等），前端标签化时严格限定分隔符（`[、,，;；\n]+`），杜绝因空格切分造成的碎片化误显示。
4. **流式数据粘包与换行截断处理**：
   - 适配 Windows 与各主流浏览器的长连接机制，前端流式读取器兼容 `\r\n\r\n` 与 `\n\n` 多种边界分隔，防止数据粘包漏包。

---

## 🧩 扩展新的大模型提供商

系统采用标准化的工厂模式，如需接入 OpenAI、Claude、DeepSeek 私有化部署或 Ollama 本地模型，只需两步：

1. 在 `app/providers/` 目录下新建模型实现文件（如 `ollama.py`），继承 `LLMProvider` 基类：
   ```python
   from .base import LLMProvider
   from typing import AsyncGenerator

   class OllamaProvider(LLMProvider):
       async def chat(self, messages: list[dict]) -> str:
           # 实现普通对话
           ...

       async def stream_chat(self, messages: list[dict]) -> AsyncGenerator[str, None]:
           # 实现流式输出迭代器
           ...
   ```
2. 在 `app/providers/__init__.py` 的 `get_provider()` 工厂函数中注册即可：
   ```python
   elif provider_type == "ollama":
       return OllamaProvider(...)
   ```

---

## ❓ 常见问题 / 排错指南

### Q1: 上传 PDF 简历后提示“无法从简历中提取到文本内容”？
> **原因**：目前系统使用 `pypdf` 进行纯文本图层提取。如果上传的 PDF 是纯图片扫描件、拍照件或使用了特殊加密字体，文本图层为空。  
> **解决建议**：请确保上传的 PDF 简历支持文字选中文制（非纯图片扫描版）。后续版本将引入 OCR 模块。

### Q2: 控制台报错 `401 Unauthorized` 或 `API key not found`？
> **原因**：未在 `.env` 中正确配置对应大模型提供商的 API 密钥。  
> **解决建议**：检查根目录下的 `.env` 文件，确认 `LLM_PROVIDER` 与对应的 `DEEPSEEK_API_KEY` 或 `QWEN_API_KEY` 已经填写有效密钥。

### Q3: 端口 8000 被占用如何处理？
> **解决建议**：使用 `--port` 参数指定新端口启动，例如：
> ```bash
> uv run uvicorn app.main:app --reload --port 8080
> ```

---

## 🛣️ 后续演进计划 (Roadmap)

- [ ] 支持 Word (`.docx`)、Markdown 及图片型简历 OCR 提取。
- [ ] 诊断报告一键导出为 Markdown、PDF 评估简报。
- [ ] 接入本地量化开源模型（通过 Ollama / vLLM 零成本部署）。
- [ ] 历史候选人库本地持久化与人岗匹配度横向对比榜单。

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源发布，欢迎自由学习、研究和在此基础上进行二次商业开发。
