from flask import Flask, request, jsonify, render_template
import requests
import os
import json
import re

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    theme = request.json.get('theme', '励志')
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
            "temperature": 1.3,  # 疯狂创意模式！1.0+ 才够随机
            "top_p": 0.95,       # 词汇多样性
            "max_tokens": 200,
            "presence_penalty": 0.6,  # 避免重复词
            "frequency_penalty": 0.8  # 避免重复句子
        }
        response = requests.post(GROQ_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()

        # 提取 JSON（防止多余文字）
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            data = json.loads(json_str)
        else:
            # 兜底
            data = {
                "quote": "坚持就是胜利！",
                "tags": ["#坚持", "#励志", "#正能量", "#抖音"],
                "desc": "每一天的坚持，都是成功的开始！"
            }

        return jsonify(data)
    except Exception as e:
        return jsonify({
            "quote": "AI 正在思考人生...",
            "tags": ["#励志", "#抖音", "#早安", "#正能量"],
            "desc": "错误：" + str(e)[:20]
        })

if __name__ == '__main__':
    app.run()
