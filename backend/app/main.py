from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import measurement
from .services.database import init_db


app = FastAPI(
    title="智能体脂分析仪 API",
    description="STM32数据采集 + AI健康分析",
    version="1.0.0"
)

# CORS配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(measurement.router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能体脂分析仪 API",
        "docs": "/docs",
        "endpoints": {
            "status": "/api/status",
            "analyze": "/api/analyze (POST)",
            "websocket": "/api/ws"
        }
    }


@app.on_event("startup")
async def startup():
    print("🚀 后端服务启动")
    print("📖 API文档: http://localhost:8000/docs")
    
    # 初始化数据库
    init_db()
    print("📦 数据库已初始化")


@app.on_event("shutdown")
async def shutdown_event():
    """关闭时执行"""
    print("服务关闭")
    from .services.stm32_service import stm32_service
    stm32_service.disconnect()