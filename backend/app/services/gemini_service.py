import os
import httpx
from typing import Optional


class GeminiService:
    """Gemini AI 服务"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = os.getenv("GEMINI_BASE_URL", "https://api.shqbb.com/v1")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY 未设置")
        else:
            print(f"✅ Gemini 服务初始化，模型: {self.model}")
    
    async def analyze_health(self, measurement: dict, user: dict, metrics: dict) -> dict:
        """调用 Gemini 分析健康数据"""
        
        if not self.api_key:
            return self._fallback_analysis(metrics)
        
        prompt = self._build_prompt(measurement, user, metrics)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 使用 OpenAI 兼容格式（中转站通常支持）
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": """你是一位专业的健康管理师和营养师。请根据用户的身体数据提供：
1. 数据解读（当前状态评估）
2. 健康风险提醒（如有）
3. 个性化建议（饮食/运动/作息）
4. 目标设定建议

请用中文回答，语气专业但亲切，避免制造焦虑。建议要具体可操作。"""
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    text = result["choices"][0]["message"]["content"]
                    return self._parse_response(text)
                else:
                    print(f"❌ API错误: {response.status_code}")
                    print(f"响应: {response.text}")
                    return self._fallback_analysis(metrics)
                    
        except Exception as e:
            print(f"❌ 调用失败: {e}")
            return self._fallback_analysis(metrics)
    
    def _build_prompt(self, measurement: dict, user: dict, metrics: dict) -> str:
        """构建提示词"""
        gender = "男" if user.get("gender") == "male" else "女"
        activity_map = {
            "sedentary": "久坐不动",
            "light": "轻度活动",
            "moderate": "中度活动",
            "active": "高度活跃"
        }
        
        return f"""
请分析以下用户的身体数据：

【用户档案】
- 性别：{gender}
- 年龄：{user.get('age')}岁
- 身高：{user.get('height')}cm
- 活动水平：{activity_map.get(user.get('activity_level', 'moderate'), '未知')}

【测量数据】
- 体重：{measurement.get('weight', '未测量')}kg
- 体脂率：{measurement.get('body_fat_percent', '未测量')}%
- 肌肉率：{measurement.get('muscle_percent', '未测量')}%
- 水分率：{measurement.get('water_percent', '未测量')}%
- 骨量：{measurement.get('bone_mass', '未测量')}kg
- 基础代谢：{measurement.get('bmr', '未测量')}kcal

【计算指标】
- BMI：{metrics.get('bmi')}（{metrics.get('bmi_status')}）
- 理想体重范围：{metrics.get('ideal_weight_range', ['?', '?'])[0]:.1f}-{metrics.get('ideal_weight_range', ['?', '?'])[1]:.1f}kg

请提供详细的健康分析和改善建议。
"""
    
    def _parse_response(self, text: str) -> dict:
        """解析响应"""
        # 提取摘要（前两句）
        sentences = text.split('。')[:2]
        summary = '。'.join(sentences) + '。'
        
        # 提取建议列表（找 bullet points）
        recommendations = []
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                recommendations.append(line[1:].strip())
        
        return {
            "summary": summary,
            "full_analysis": text,
            "recommendations": recommendations if recommendations else [
                "保持规律作息，每天睡眠7-8小时",
                "均衡饮食，多吃蔬菜水果",
                "定期运动，每周至少150分钟中等强度运动"
            ]
        }
    
    def _fallback_analysis(self, metrics: dict) -> dict:
        """备用分析（API失败时使用）"""
        bmi_status = metrics.get("bmi_status", "正常")
        
        if bmi_status == "正常":
            summary = "您的体重在正常范围内，保持良好的生活习惯。"
            analysis = "恭喜！您的身体指标处于健康范围。建议：\n1. 继续保持均衡饮食\n2. 每周进行3-5次有氧运动\n3. 注意体脂率变化\n4. 定期测量，追踪身体数据趋势"
        elif bmi_status == "偏瘦":
            summary = "您的体重偏轻，建议适当增加营养摄入。"
            analysis = "根据您的身体数据，BMI指数显示体重偏轻。建议：\n1. 增加蛋白质摄入，多吃瘦肉、鸡蛋、牛奶\n2. 适当进行力量训练，增加肌肉量\n3. 保证充足睡眠，促进身体恢复"
        else:
            summary = "您的体重偏重，建议适当控制饮食并增加运动。"
            analysis = "根据分析，您的BMI指数略高。建议：\n1. 控制热量摄入，减少高糖高脂食物\n2. 增加有氧运动，如慢跑、游泳\n3. 每周运动4-5次，每次45分钟以上\n4. 多喝水，保证充足睡眠"
        
        return {
            "summary": summary,
            "full_analysis": analysis,
            "recommendations": [
                "保持规律作息，每天睡眠7-8小时",
                "多喝水，每天2000ml以上",
                "定期测量，记录身体变化"
            ]
        }


# 单例
gemini_service = GeminiService()