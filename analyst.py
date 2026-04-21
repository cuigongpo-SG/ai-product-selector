import json, os, requests

def analyze_data():
    api_key = os.getenv('GEMINI_API_KEY')
    # 使用 v1beta 接口以支持最新的 2.5 系列模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    with open('raw_data.json', 'r') as f:
        raw_data = json.load(f)

    prompt = f"作为选品专家，分析以下亚马逊北美站数据并给出爆款预测：{json.dumps(raw_data)}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload)
    
    with open('analysis_report.json', 'w') as f:
        json.dump(response.json(), f)

if __name__ == "__main__":
    analyze_data()
