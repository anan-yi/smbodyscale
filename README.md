# 智能体重体脂分析仪 - Web数据与AI分析模块

> 本项目为嵌入式系统课程实践项目，负责接收STM32传感器数据并提供AI健康分析Web服务。

## 📋 项目简介

本项目是智能体重体脂仪器的软件部分，实现以下核心功能：
- **硬件通信**：通过串口接收STM32传输的体重/体脂数据
- **实时推送**：WebSocket向前端实时推送测量数据
- **AI分析**：结合用户档案（年龄/性别/身高）调用AI API生成健康建议
- **Web界面**：提供数据可视化和交互式分析报告

## 🏗️ 系统架构

```
┌─────────────┐    UART/USB     ┌─────────────┐    HTTP/WS     ┌─────────────┐
│  STM32      │ ───────────────→ │  后端API    │ ←────────────→ │   Web前端   │
│ (传感器)    │   原始体重体脂数据 │  (Python)   │   用户数据+AI  │  (Vue3)     │
└─────────────┘                  └──────┬──────┘                └─────────────┘
                                        │
                                   ┌────┴────┐
                                   │  AI服务  │
                                   │(DeepSeek)│
                                   └─────────┘
```

## 🛠️ 技术栈与版本

### 必须统一的环境版本

| 组件 | 版本 | 安装命令/下载链接 | 验证命令 |
|:---|:---|:---|:---|
| **Python** | 3.10.x | [官网下载](https://www.python.org/downloads/release/python-31011/) | `python --version` |
| **Node.js** | 18.x LTS | [官网下载](https://nodejs.org/en/download/) | `node --version` |
| **npm** | 9.x+ | 随Node.js安装 | `npm --version` |
| **Git** | 2.40+ | [官网下载](https://git-scm.com/downloads) | `git --version` |
| **VS Code** | 最新 | [官网下载](https://code.visualstudio.com/) | - |

### 项目依赖版本（锁定）

**后端依赖** (`backend/requirements.txt`):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pyserial==3.5
websockets==12.0
pydantic==2.5.0
python-dotenv==1.0.0
openai==1.6.0
python-multipart==0.0.6
```

**前端依赖** (`frontend/package.json` 关键项):
```json
{
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "typescript": "^5.3.2",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.6"
  }
}
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone [项目仓库地址]
cd smbodyscale
```

### 2. 后端环境配置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（必须）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖（严格按锁定版本）
pip install -r requirements.txt

# 创建环境变量文件
copy .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### 3. 前端环境配置

```bash
# 进入前端目录
cd frontend

# 安装依赖（严格按package.json）
npm install

# 如果安装失败，清除缓存重试
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 4. 启动开发服务器

**后端** (端口8000):
```bash
cd backend
# 确保虚拟环境已激活
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端** (端口5173):
```bash
cd frontend
npm run dev
```

访问 http://localhost:5173 查看应用

## 📁 项目结构规范

```
smbodyscale/                 # 项目根目录
├── .gitignore                   # Git忽略规则
├── README.md                    # 本文件
├── docs/                        # 文档目录
│   ├── api/                     # API接口文档
│   ├── stm32_protocol.md        # STM32通信协议
│   └── deployment.md            # 部署指南
├── backend/                     # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI入口
│   │   ├── config.py            # 配置管理
│   │   ├── routers/             # API路由
│   │   │   ├── __init__.py
│   │   │   ├── measurement.py   # 测量数据接口
│   │   │   └── analysis.py      # AI分析接口
│   │   ├── services/            # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── stm32_service.py # STM32通信
│   │   │   └── ai_service.py    # AI分析
│   │   └── models/              # 数据模型
│   │       └── schemas.py       # Pydantic模型
│   ├── tests/                   # 测试代码
│   ├── requirements.txt         # 依赖清单
│   ├── .env.example             # 环境变量模板
│   └── .env                     # 本地环境变量（不提交）
├── frontend/                    # 前端代码
│   ├── src/
│   │   ├── assets/              # 静态资源
│   │   ├── components/          # 通用组件
│   │   │   ├── common/          # 基础组件
│   │   │   └── measurement/     # 测量相关组件
│   │   ├── views/               # 页面视图
│   │   │   ├── HomeView.vue
│   │   │   └── MeasurementView.vue
│   │   ├── stores/              # Pinia状态管理
│   │   ├── services/            # API服务
│   │   ├── utils/               # 工具函数
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── hardware/                    # 硬件相关（参考）
    └── protocol.md              # 通信协议定义
```

## 📝 代码规范

### Python 代码规范 (后端)

**必须遵守** [PEP 8](https://pep8.org/) 规范，使用以下工具检查：

```bash
# 安装检查工具
pip install flake8 black isort

# 自动格式化代码
black app/
isort app/

# 检查规范
flake8 app/ --max-line-length=100 --ignore=E203,W503
```

**关键规范**:
- 缩进：4个空格（禁止使用Tab）
- 行长度：最大100字符
- 命名：
  - 模块名：`lowercase_snake_case.py`
  - 类名：`CapitalizedWords`
  - 函数/变量：`lowercase_snake_case`
  - 常量：`UPPER_SNAKE_CASE`
- 注释：使用Google风格Docstring

```python
# 示例：符合规范的函数
async def analyze_body_composition(
    weight: float,
    body_fat: float,
    user_profile: UserProfile
) -> AnalysisResult:
    """分析身体成分并生成健康建议。

    Args:
        weight: 体重，单位kg
        body_fat: 体脂率，百分比
        user_profile: 用户档案信息

    Returns:
        AnalysisResult: 包含指标评估和AI建议的分析结果

    Raises:
        ValueError: 当输入数据无效时抛出
    """
    if weight <= 0 or body_fat < 0:
        raise ValueError("体重和体脂率必须为正数")

    bmi = calculate_bmi(weight, user_profile.height)
    return AnalysisResult(bmi=bmi, suggestions=[])
```

### TypeScript/Vue 代码规范 (前端)

**必须遵守**:
- 使用 **TypeScript** 严格模式（不允许`any`类型）
- 组件名：`PascalCase.vue`
- 组合式函数：`useXXX.ts`
- 常量：`UPPER_SNAKE_CASE`
- 接口/类型：`PascalCase` + `I`前缀（如`IUserProfile`）

```vue
<!-- 示例：符合规范的Vue组件 -->
<script setup lang="ts">
import { ref, computed } from 'vue'

// 类型定义必须在顶部
interface IMeasurementData {
  weight: number
  bodyFatPercent: number
  timestamp: string
}

// Props定义
const props = defineProps<{
  initialData?: IMeasurementData
}>()

// 响应式状态
const measurementData = ref<IMeasurementData | null>(props.initialData || null)
const isLoading = ref<boolean>(false)

// 计算属性
const bmi = computed<number | null>(() => {
  if (!measurementData.value) return null
  const heightInMeters = userHeight.value / 100
  return measurementData.value.weight / (heightInMeters ** 2)
})

// 方法
async function fetchMeasurement(): Promise<void> {
  isLoading.value = true
  try {
    const response = await api.get('/measurement/latest')
    measurementData.value = response.data
  } catch (error) {
    console.error('获取测量数据失败:', error)
  } finally {
    isLoading.value = false
  }
}
</script>
```

### Git 提交规范

**分支策略**:
```
main                    # 生产分支，保护分支
├── develop             # 开发分支，日常合并到此
│   ├── feature/stm32   # STM32通信功能
│   ├── feature/api     # 后端API开发
│   ├── feature/web     # 前端界面开发
│   └── feature/ai      # AI分析集成
└── hotfix/xxx          # 紧急修复
```

**提交信息格式**（严格遵循 [Conventional Commits](https://www.conventionalcommits.org/)）:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**常用类型**:
| 类型 | 用途 | 示例 |
|:---|:---|:---|
| `feat` | 新功能 | `feat(api): 添加AI分析接口` |
| `fix` | 修复bug | `fix(stm32): 修复串口数据解析错误` |
| `docs` | 文档更新 | `docs(readme): 添加部署说明` |
| `style` | 代码格式 | `style(frontend): 格式化Vue组件` |
| `refactor` | 重构 | `refactor(backend): 优化数据库查询` |
| `test` | 测试代码 | `test(api): 添加测量接口单元测试` |
| `chore` | 构建/工具 | `chore(deps): 更新依赖版本` |

**完整示例**:
```bash
git commit -m "feat(api): 添加用户档案验证功能

- 实现年龄范围验证（1-120岁）
- 添加身高体重合理性检查
- 完善错误提示信息

Closes #12"
```

## 🔄 协作流程

### 1. 开始新功能开发

```bash
# 1. 切换到develop分支并更新
git checkout develop
git pull origin develop

# 2. 创建功能分支（命名规范：feature/功能描述）
git checkout -b feature/stm32-protocol

# 3. 开发过程中多次提交
git add .
git commit -m "feat(stm32): 实现数据帧解析器"

# 4. 开发完成后，先同步develop最新代码
git checkout develop
git pull origin develop
git checkout feature/stm32-protocol
git rebase develop  # 或使用 merge: git merge develop

# 5. 解决冲突后推送到远程
git push origin feature/stm32-protocol

# 6. 在GitHub/GitLab创建Pull Request，请求合并到develop
# 必须至少1人Code Review通过后才能合并
```

```

使用项目管理工具（如GitHub Projects/飞书文档）记录任务状态。

## 🔧 开发环境配置

### VS Code 必装插件

1. **Python**: Microsoft官方Python扩展
2. **Volar**: Vue 3官方扩展（禁用Vetur）
3. **ESLint**: 代码规范检查
4. **Prettier**: 代码格式化
5. **Tailwind CSS IntelliSense**: CSS提示
6. **Thunder Client**: API测试（替代Postman）

### 推荐设置

创建 `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/.git": true
  }
}
```

## 🧪 测试要求

### 后端测试

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

**必须测试的场景**:
- STM32数据解析（正常帧/错误帧/粘包）
- API接口参数验证
- AI服务异常处理（API超时/限流）

### 前端测试

```bash
cd frontend
npm run test:unit
```
## ⚠️ 常见问题

### Q: STM32连接不上？
A: 检查步骤：
1. 确认USB转串口驱动已安装（Windows设备管理器查看COM口）
2. 检查`backend/.env`中的`SERIAL_PORT`配置（Windows通常是`COM3`，Linux是`/dev/ttyUSB0`）
3. 确认波特率与STM32代码一致（默认115200）

### Q: AI API调用失败？
A: 
1. 检查`.env`文件中的`DEEPSEEK_API_KEY`是否填写正确
2. 确认网络可以访问api.deepseek.com
3. 查看`backend/logs/`中的错误日志

### Q: 前端无法连接后端？
A:
1. 确认后端服务已启动（访问 http://localhost:8000/docs 应看到Swagger文档）
2. 检查`frontend/.env`中的`VITE_API_BASE_URL`是否为`http://localhost:8000`
3. 浏览器F12查看Network面板，确认请求地址正确

---

**最后更新**: 2026-04-07  
**维护者**: [逸居]
