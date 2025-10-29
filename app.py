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
    生成一条抖音风格的{theme}励志短句，适合发视频。
    要求：
    1. 句子简短有力，10-20字
    2. 带情绪感染力
    3. 输出纯JSON格式（不要任何说明）：
    {{
      "quote": "句子",
      "tags": ["#tag1", "#tag2", "#tag3", "#tag4"],
      "desc": "视频描述文案，30字内"
    }}
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 150
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
