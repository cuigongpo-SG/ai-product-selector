import json, os, requests, re

def analyze_data():
    api_key = os.getenv('GEMINI_API_KEY')
    # 严谨提醒：请确保下方字符串内只有网址文字
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    if not os.path.exists('raw_data.json'):
        print("❌ 错误：找不到原始数据文件")
        return

    with open('raw_data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    prompt = f"分析亚马逊北美站选品：{json.dumps(raw_data)}。请严格按JSON格式返回：product_name, trend_analysis, risk_assessment, recommendation"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, json=payload)
    
    # 增加状态码检查
    if response.status_code == 200:
        res_json = response.json()
        content = res_json['candidates'][0]['content']['parts'][0]['text']
        # 清洗可能存在的 Markdown 标签
        clean_content = re.sub(r'```json|```', '', content).strip()
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            f.write(clean_content)
        print("✅ AI 分析成功")
    else:
        print(f"❌ API 调用失败，状态码：{response.status_code}，原因：{response.text}")

if __name__ == "__main__":
    analyze_data()
