from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class MeasurementData(BaseModel):
    """测量数据模型"""
    weight: float = Field(..., description="体重(kg)", gt=0, lt=300)
    body_fat_percent: Optional[float] = Field(None, description="体脂率(%)", ge=0, le=100)
    muscle_percent: Optional[float] = Field(None, description="肌肉率(%)", ge=0, le=100)
    water_percent: Optional[float] = Field(None, description="水分率(%)", ge=0, le=100)
    bone_mass: Optional[float] = Field(None, description="骨量(kg)", ge=0, lt=10)
    bmr: Optional[int] = Field(None, description="基础代谢(kcal)", ge=0, lt=5000)
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class UserProfile(BaseModel):
    """用户档案模型"""
    age: int = Field(..., description="年龄", ge=1, le=120)
    gender: Literal["male", "female"] = Field(..., description="性别")
    height: float = Field(..., description="身高(cm)", ge=50, le=250)
    target_weight: Optional[float] = Field(None, description="目标体重(kg)")
    activity_level: Literal["sedentary", "light", "moderate", "active"] = Field(
        default="moderate", description="活动量"
    )


class AnalysisRequest(BaseModel):
    """分析请求模型"""
    measurement: MeasurementData
    user: UserProfile


class HealthMetrics(BaseModel):
    """健康指标计算结果"""
    bmi: float = Field(..., description="BMI指数")
    bmi_status: str = Field(..., description="BMI状态：偏瘦/正常/超重/肥胖")
    ideal_weight_range: tuple[float, float] = Field(..., description="理想体重范围(kg)")
    body_fat_status: Optional[str] = Field(None, description="体脂状态")


class AIAnalysisResult(BaseModel):
    """AI分析结果"""
    summary: str = Field(..., description="综合评估摘要")
    full_analysis: str = Field(..., description="详细分析建议")
    recommendations: list[str] = Field(default_factory=list, description="行动建议列表")
    risk_warnings: Optional[list[str]] = Field(None, description="风险提示")


class AnalysisResponse(BaseModel):
    """完整分析响应"""
    metrics: HealthMetrics
    ai_result: AIAnalysisResult
    raw_data: AnalysisRequest
    analysis_time: str = Field(default_factory=lambda: datetime.now().isoformat())