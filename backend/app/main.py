import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载环境变量（读取你刚才在 .env 里填好的新 Key）
load_dotenv()

# 2. 初始化应用
app = FastAPI(
    title="Smart Body Scale API",
    description="后端核心分析服务 - 由 AI 驱动",
    version="1.0.0"
)

# 3. 初始化 AI 客户端
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

client = OpenAI(api_key=api_key, base_url=base_url)

# 4. 定义数据规范
class MeasurementData(BaseModel):
    weight: float
    fat_rate: float

# --- 核心接口 ---

@app.get("/")
async def health_check():
    """验证后端是否活着（不仅显示运行中，还检查 AI 配置）"""
    return {
        "status": "online",
        "ai_ready": api_key is not None,
        "message": "智能体脂秤后端核心服务已就绪"
    }

@app.post("/api/analyze")
async def generate_analysis(data: MeasurementData):
    """
    接收前端传来的体重体脂，返回 AI 深度分析报告
    """
    if not api_key:
        raise HTTPException(status_code=500, detail="后端未检测到 API Key，请检查 .env 文件")

    try:
        # 核心逻辑
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的健身和营养专家，语气友好且直接。"},
                {"role": "user", "content": f"用户测量数据：体重 {data.weight}kg，体脂率 {data.fat_rate}%。请给出100字左右的建议。"}
            ]
        )
        return {
            "success": True,
            "data": {
                "weight": data.weight,
                "fat_rate": data.fat_rate,
                "analysis": response.choices[0].message.content
            }
        }
    except Exception as e:
        # 如果 DeepSeek 报错，抓取原因
        raise HTTPException(status_code=500, detail=f"AI 分析失败: {str(e)}")

