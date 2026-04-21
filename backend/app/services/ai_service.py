import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量（从 .env 文件读取 API Key）
load_dotenv()


class AIAnalyzer:
    def __init__(self):
        # 优先读取 DeepSeek 配置，如果没有则读取 OpenAI
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

        # 初始化客户端
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_health_report(self, weight, fat_rate):
        """
        根据体重和体脂率生成 AI 健康分析报告
        """
        try:
            prompt = f"""
            你是一位专业的健身和营养专家。
            用户测量数据如下：
            - 体重：{weight} kg
            - 体脂率：{fat_rate} %
            请根据这些数据，给出 100 字左右的简短建议，包括饮食和运动两个方面。
            语气要像朋友一样随和、直接。
            """

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个有用的健康助手"},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI分析暂时开小差了，错误原因：{str(e)}"


# 测试代码
if __name__ == "__main__":
    analyzer = AIAnalyzer()
    # 模拟一个 75kg, 25% 体脂的数据
    print(analyzer.generate_health_report(75, 25))
