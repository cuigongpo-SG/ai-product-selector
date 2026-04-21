import json, os, requests, re

def analyze_data():
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=){api_key}"
    
    # 1. 读取原始数据
    with open('raw_data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    # 2. 严谨的 Prompt：规定死输出格式
    prompt = f"""
    你是一个亚马逊北美站选品专家。请分析以下采集到的原始数据：
    {json.dumps(raw_data)}

    请严格按照以下 JSON 格式返回，不要包含任何解释性文字或 Markdown 标签：
    {{
        "product_name": "分析出的核心产品名称",
        "trend_analysis": "一句话描述该产品在北美的趋势",
        "risk_assessment": "该产品的潜在风险（版权、物流等）",
        "recommendation": "最终操作建议"
    }}
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        # 提取 AI 的文本内容
        raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # 3. 核心清洗逻辑：只保留 {} 之间的内容
        clean_json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if clean_json_match:
            final_data = clean_json_match.group(0)
        else:
            final_data = raw_text

        # 验证是否为合法 JSON
        json.loads(final_data) 
        
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            f.write(final_data)
        print("✅ AI 报告解析成功并保存")
        
    except Exception as e:
        print(f"❌ 解析出错: {e}")
        # 保底方案：避免 renderer 读到空文件
        fallback = {"product_name": "解析失败", "trend_analysis": "无", "risk_assessment": "无", "recommendation": "请检查日志"}
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(fallback, f)

if __name__ == "__main__":
    analyze_data()
