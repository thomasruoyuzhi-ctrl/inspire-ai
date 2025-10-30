import requests
import json
import re
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_content(theme="励志"):
    prompt = f"""
    你现在是抖音顶级文案大师，风格随机切换！
    主题：{theme}

    随机选择一种风格生成（不要重复）：
    1. 热血燃爆型（如“冲啊兄弟！”）
    2. 温柔治愈型（如“慢慢来也很好”）
    3. 反转金句型（如“越努力越幸运？不，是越坚持越自由！”）
    4. 段子手型（如“早安？不，是早安暴富！”）

    要求：
    - 句子 10-20 字，押韵更好
    - 情绪感染力爆棚
    - 输出纯 JSON：
    {{
      "quote": "金句",
      "tags": ["#随机tag1", "#tag2", "#tag3", "#tag4"],
      "desc": "视频描述，30字内，带动作号召"
    }}
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 1.3,
            "top_p": 0.95,
            "max_tokens": 200,
            "presence_penalty": 0.6,
            "frequency_penalty": 0.8
        }
        response = requests.post(GROQ_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()

        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            return fallback_content(theme)
    except Exception as e:
        print(f"Error: {e}")
        return fallback_content(theme)

def fallback_content(theme):
    return {
        "quote": f"{theme}就是胜利！",
        "tags": [f"#{theme}", "#励志", "#抖音", "#正能量"],
        "desc": f"每天{theme}1%，成功离你更近！"
    }
