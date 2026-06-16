# Overstats → 微信小程序转换计划

## Context

将现有的 Vue 3 SPA 前端替换为 uni-app 微信小程序前端。后端（Python HTTP Server + Pillow 渲染）完全不变，Cloudflare Tunnel 继续提供 HTTPS 公网访问。目标是三页面结构：登录验证 → 模块列表 → 表单查询/图片展示。

## 项目结构

```
overstats-miniapp/                    # 新建，与现有 Overstats/ 平级
├── src/
│   ├── pages/
│   │   ├── login/index.vue           # 密码验证页 (0320)
│   │   ├── index/index.vue           # 模块列表（分组折叠）
│   │   └── module/index.vue          # 通用查询页（动态表单 + 图片展示）
│   ├── stores/
│   │   ├── modules.ts                # 模块注册表（从 bootstrap API 加载）
│   │   └── request.ts                # 请求状态管理
│   ├── api/
│   │   └── client.ts                 # uni.request 封装 + bootstrap + 图片请求
│   ├── types/
│   │   └── index.ts                  # 从现有项目复制类型定义
│   ├── components/
│   │   ├── ModuleGroup.vue           # 可折叠模块分组
│   │   ├── FieldForm.vue             # 动态表单（text/number/select/checkbox）
│   │   └── ImageViewer.vue           # 图片展示 + 全屏预览
│   ├── utils/
│   │   └── storage.ts                # localStorage 替代（uni.storage API）
│   ├── static/
│   │   └── logo.png
│   ├── App.vue                       # 根组件（登陆守卫）
│   ├── main.ts                       # 入口
│   ├── manifest.json                 # uni-app 配置
│   ├── pages.json                    # 页面路由
│   └── uni.scss                      # 全局样式变量
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 页面路由和导航

```
pages.json:
  login  → pages/login/index      # 启动页，未认证时显示
  index  → pages/index/index      # 模块列表主页
  module → pages/module/index     # 通用查询页（带 query params: moduleId）

导航规则：
- App.vue 检查 uni.storage 中的 auth 标记
- 未认证 → 始终重定向到 login
- 已认证 → 显示 index 页面
- 点击模块 → navigateTo module?moduleId=dashen-profile
```

## 实现细节

### 1. Login 页 (`pages/login/index.vue`)

- 设计：全屏居中卡片，暖色渐变背景，与现有 LoginView.vue 风格一致
- 密码输入框（type=password，maxlength=4）
- 校验 "0320"；错误时抖动动画 + "密码不对哦～"
- 成功后写入 `uni.setStorageSync('overstats_auth', '1')`，跳转 index
- 标题："Overstats"，描述："这是Tinyman（小笨蛋）给潼潼宝宝（小坏蛋）做的独享查询网站"

### 2. Index 页 (`pages/index/index.vue`)

- 顶部标题栏："数据查询" + 描述文字
- 模块按 4 组折叠显示（复用 Vue 中 ModuleNav.vue 的分组逻辑）：
  - 玩家查询：profile, match, match-detail, sameplay, sameplay-detail, rank-history, quick-strength, competitive-strength
  - 总结报告：summary-today, summary-yesterday, summary-week
  - 排行榜与数据：rank-leaderboard, hero-leaderboard, hero-pick-rate, hero-perk
  - 更多：esports, shop, patch-notes
- 每组可点击展开/收起（默认展开）
- 点击单个模块 → `uni.navigateTo({ url: '/pages/module/index?moduleId=' + id })`

### 3. Module 页 (`pages/module/index.vue`)

- 通过 `onLoad(options.moduleId)` 接收模块 ID
- 从 modules store 获取模块规格（title, description, fields, requires_target, default_target_key）
- 顶部：模块标题 + 描述（对应 ModuleHero.vue）
- 表单区：
  - 如果 `requires_target=true`：显示目标类型选择（bnet_id/customer_token）+ 目标值输入框 + 两个快捷按钮（小坏蛋/意志坚强酱）
  - 动态字段：根据 fields 数组遍历渲染（text/number/select/checkbox），控件直接使用 uni-app 原生组件
  - bnet_id 字段旁显示快捷填充按钮
- 查询按钮："生成图片"（渐变橙色按钮）
- 结果区：
  - 加载中：旋转动画
  - 成功：`<image>` 显示图片，支持点击全屏预览（`uni.previewImage`）
  - 失败：错误提示
- 底部快捷按钮：对于 summary 模块，增加 today/yesterday/week 切换标签

### 4. API 客户端 (`api/client.ts`)

```typescript
// 核心：uni.request 封装
const API_BASE = 'https://jetson.owstatfortt.xyz'  // 生产环境
// 开发时可改为 localhost

async function request<T>(method, url, data?, responseType?): Promise<T>

// 专用函数
fetchBootstrap()                        → GET /api/v2/ui/bootstrap
fetchModuleImage(endpoint, payload)     → POST endpoint, responseType:'arraybuffer'
```

- 替换 axios → `uni.request`
- arraybuffer 响应 → `uni.arrayBufferToBase64(res.data)` → `data:image/png;base64,${b64}` → 直接用于 `<image>` src
- 超时 120 秒（与现有一致）

### 5. 状态管理 (`stores/`)

使用 Pinia（uni-app 完全支持）：

**modules store**：
- `modules: ModuleSpec[]` — 从 bootstrap 加载
- `activeModuleId: string`
- `loading/error` 状态
- `loadModules()` — 调用 bootstrap API
- `setActiveModule(id)` — 切换模块

**request store**：
- `targetType: 'bnet_id' | 'customer_token' | ''`
- `targetValue: string`
- `fields: Record<string, any>` — 动态字段值
- `result: { url: string, title: string } | null`
- `status: 'idle' | 'loading' | 'success' | 'error'`
- `sendRequest(module: ModuleSpec)` — 调用 API，处理响应

### 6. 图片处理 (`components/ImageViewer.vue`)

- 展示：`<image :src="resultUrl" mode="widthFix" />`
- 全屏预览：`uni.previewImage({ urls: [resultUrl] })`
- 长按保存：`uni.saveImageToPhotosAlbum()` (需用户授权)
- 注意：base64 data URI 长度限制。如果图片 > 2MB，写入临时文件路径再显示

### 7. 全局样式 (`uni.scss`)

- 复用现有 CSS 变量（橙色调 accent #d87b38，暖色背景 #f7f3eb）
- 适配微信小程序 750rpx 设计稿
- 页面背景：径向渐变 + 线性渐变，与现有 AppShell 一致

### 8. 关键差异处理

| 原 Vue 项目 | uni-app 小程序 |
|---|---|
| `vue-router` | `pages.json` + `uni.navigateTo` |
| `localStorage` | `uni.setStorageSync` / `uni.getStorageSync` |
| `axios` + `URL.createObjectURL` | `uni.request` + `arrayBufferToBase64` + data URI |
| `@media` 响应式 | `rpx` 单位 + `uni.upx2px` + 条件编译 |
| Element Plus 组件 | uni-app 原生组件 + 自定义样式 |
| Blob URL | base64 data URI 或临时文件 |

## 实施步骤

1. 初始化 uni-app 项目（`npx degit dcloudio/uni-preset-vue#vite-ts overstats-miniapp`）
2. 复制 TypeScript 类型定义到 `src/types/index.ts`
3. 实现 `api/client.ts` — uni.request 封装
4. 实现 stores（modules.ts, request.ts）
5. 实现 `pages/login/index.vue`
6. 实现 `pages/index/index.vue` + `ModuleGroup.vue`
7. 实现 `pages/module/index.vue` + `FieldForm.vue` + `ImageViewer.vue`
8. 实现 `App.vue` 登录守卫
9. 配置 `pages.json`、`manifest.json`
10. 全局样式 uni.scss
11. 构建测试（`npm run dev:mp-weixin`）
12. 用微信开发者工具导入 dist/dev/mp-weixin 预览

## 验证

1. 启动本地后端：`curl http://127.0.0.1:18080/healthz` 确认 200
2. 构建小程序：`npm run dev:mp-weixin`
3. 微信开发者工具打开，确认：
   - 登录页显示，输入错误密码抖动，输入 0320 进入主页
   - 主页模块分组折叠展开正常
   - 点击"玩家资料"，bnet_id 输入框旁有快捷按钮，填入后点查询能展示图片
   - 非 requires_target 模块（如商店）能直接查询
4. 切换到生产域名 `https://jetson.owstatfortt.xyz` 测试真机
5. 微信公众平台配置 request 合法域名后真机扫码预览
