import json, os, requests, re

def analyze_data():
    api_key = os.getenv('GEMINI_API_KEY')
    # 严谨：确保 URL 是纯字符串，无引号外的括号
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    if not os.path.exists('raw_data.json'):
        print("❌ 错误：找不到 raw_data.json")
        return

    with open('raw_data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    prompt = f"分析亚马逊北美站选品：{json.dumps(raw_data)}。请严格按 JSON 格式返回：product_name, trend_analysis, risk_assessment, recommendation"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            content = res_json['candidates'][0]['content']['parts'][0]['text']
            # 使用正则清洗掉 AI 可能带出的 Markdown 标签
            clean_content = re.sub(r'```json|```', '', content).strip()
            # 尝试解析一次，确保它是合法的 JSON
            json.loads(clean_content)
            with open('analysis_report.json', 'w', encoding='utf-8') as f:
                f.write(clean_content)
            print("✅ AI 分析成功")
        else:
            print(f"❌ API 失败: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")

if __name__ == "__main__":
    analyze_data()
