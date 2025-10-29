from flask import Flask, request, jsonify, render_template
import requests
import os

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
    3. 输出JSON格式：
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
            "temperature": 0.8
        }
        response = requests.post(GROQ_URL, json=data, headers=headers)
        result = response.json()['choices'][0]['message']['content'].strip()
        import json
        return jsonify(json.loads(result))
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
