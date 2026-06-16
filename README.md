# Overstats

守望先锋数据查询与展示系统，基于网易大神（Dashen）API 提供玩家资料、对局记录、排行榜、英雄数据等 **18 个查询模块**。

- **后端**：Python HTTP Server + Pillow 图片渲染 + SQLite 持久化
- **前端**：Vue 3 + TypeScript + Pinia + Element Plus SPA，支持桌面端和移动端

## 架构

```
Vue 3 SPA (Vite) ──→ Python HTTP Server (:18080) ──→ NetEase Dashen API
                           │
                           ├── Pillow 渲染 PNG 图片
                           ├── SQLite (比赛统计 / 请求指标 / 排行榜)
                           └── OpenAI 兼容 AI 分析 (DeepSeek)
```

后端监听 `127.0.0.1:18080`，前端 Vite 开发服务器将 `/api` 代理到后端。生产环境下后端直接服务 Vue 构建产物。

## 功能模块

### 玩家查询（需要 bnet_id / customer_token）

| 模块 | 说明 |
|------|------|
| 玩家资料 | 生涯概览、段位、英雄使用、雷达图 |
| 近期对局 | 比赛列表，支持分页和模式切换 |
| 单局详情 | 双方阵容、个人数据、AI 分析 |
| 同玩查询 | 两名玩家的共同比赛 |
| 同玩详情 | 同玩单局详情 + AI 锐评 |
| 段位历史 | 赛季段位变化时间线 |
| 快速强度 | 快速模式实力评估 |
| 竞技强度 | 竞技模式实力评估 |
| 今日总结 | 当日比赛全量分析 |
| 昨日总结 | 昨日比赛全量分析 |
| 本周总结 | 本周比赛全量分析（约 60s） |

### 公共数据（无需目标玩家）

| 模块 | 说明 |
|------|------|
| 省级排行榜 | 按省 / 职责查询大神排名 |
| 英雄省级榜 | 按省 / 英雄 / 队列查询 |
| 英雄选取率 | 全英雄榜单 + 单英雄历史曲线 |
| 威能总览 | 英雄主 / 次威能选取率 |
| OW 赛事 | 实时电竞赛事（PandaScore） |
| OW 商店 | 当前商城物品 |
| 补丁说明 | 暴雪 / 国服补丁（支持翻译） |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+

### 1. 安装依赖

```bash
pip install httpx pillow
```

### 2. 配置认证

编辑 `config.yaml`（放在项目根目录，已加入 .gitignore）：

```yaml
roleid: <你的 role_id>
token: <你的 token>
```

也可以设置环境变量（前缀 `OVERSTATS_`）。如何获取凭据见 `Overstats/Faststart.md`。

### 3. 启动后端

```bash
cd Overstats
python run.py
# → [overstats] serving on http://127.0.0.1:18080
```

### 4. 启动前端（开发）

```bash
cd Overstats/ui
npm install
npm run dev
# → http://127.0.0.1:5173/ui/
```

### 5. 生产构建

```bash
cd Overstats/ui
npm run build
```

构建后直接访问 `http://127.0.0.1:18080`，后端自动服务前端产物。

## 前端特性

- 密码登录验证保护
- 侧边栏分组折叠导航（4 组：玩家查询 / 总结报告 / 排行榜与数据 / 更多）
- 动态表单（文本 / 数字 / 选择 / 复选框），根据模块元数据自动渲染
- bnet_id 快捷填充按钮
- 查询结果图片展示 + JSON 数据预览
- 移动端适配：汉堡菜单侧滑导航、响应式布局
- LLM 智能路由：自然语言输入自动匹配查询模块

## API 端点

每个模块提供 2–3 类端点：

- `POST /api/v2/<module>` — JSON 数据
- `POST /api/v2/<module>/image` — PNG 图片（二进制）
- `POST /api/v2/<module>/replies` — JSON + base64 图片（机器人回复格式）

完整 API 文档见 `Overstats/OVERSTATS_API.md`。

## 项目结构

```
overstats/
├── README.md
├── .gitignore
├── config.yaml                     # 本地认证（不入库）
├── Overstats/
│   ├── run.py                      # 后端入口
│   ├── Faststart.md                # 凭据获取指南
│   ├── OVERSTATS_API.md            # API 文档
│   ├── config/
│   │   ├── config.py               # 运行配置
│   │   └── loader.py               # 配置加载（env 覆盖）
│   ├── src/
│   │   ├── server.py               # HTTP 服务 & 路由
│   │   ├── client/apiclient.py     # Dashen API 客户端
│   │   ├── modules/                # 18 个业务模块
│   │   ├── http_server/            # 静态服务 & 模块注册表
│   │   ├── db/                     # SQLite 持久化
│   │   └── constants/              # 英雄名 / 背景图常量
│   ├── res/                        # 渲染资源（字体 / 背景 / 图标）
│   └── ui/                         # Vue 3 前端
│       ├── src/
│       │   ├── pages/              # 页面组件
│       │   ├── components/         # 通用组件
│       │   ├── stores/             # Pinia 状态管理
│       │   ├── api/                # API 客户端
│       │   └── types/              # TypeScript 类型
│       └── dist/                   # 构建输出
└── .claude/                        # Claude Code 配置
    └── skills/web-design-engineer/ # 设计 Skill
```

## 安全说明

- `config.yaml` 包含真实凭据，已加入 `.gitignore`，请勿提交
- `Overstats/config/config.py` 中的 `DASHEN_ACCOUNTS` 和 `ANALYSIS_API_KEY` 使用占位符
- 发布前请确认所有敏感值已替换
