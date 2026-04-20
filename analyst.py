import os
import json
import requests

def analyze_data():
    # 1. 读取上一步生成的原始数据
    try:
        with open('raw_data.json', 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到原始数据文件")
        return

    # 2. 准备 Gemini API 请求
    api_key = os.getenv('GEMINI_API_KEY')
    # 这里使用的是 Google AI Studio 的标准 API 端点
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # 3. 构造给 AI 的提示词 (Prompt)
    prompt = f"""
    你是一个资深的跨境电商选品专家。请分析以下采集到的原始数据，并给出选品建议。
    
    原始数据: {json.dumps(raw_data)}
    
    请输出以下格式的 JSON 结果:
    {{
        "product_name": "产品名称",
        "trend_analysis": "趋势分析",
        "risk_level": "风险评估(低/中/高)",
        "recommendation": "最终建议"
    }}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # 4. 调用 API
    print("🧠 正在请求 Gemini 进行深度分析...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        analysis_result = response.json()
        # 提取 AI 返回的文本（简单处理，后续可优化）
        content = analysis_result['candidates'][0]['content']['parts'][0]['text']
        print("✅ 分析完成！")
        
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"❌ AI 分析失败: {response.text}")

if __name__ == "__main__":
    analyze_data()
