import json, os
from datetime import datetime

def render_html():
    try:
        with open('analysis_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
    except:
        report = {"product_name": "未生成报告", "trend_analysis": "无", "risk_assessment": "无", "recommendation": "无"}

    # 获取当前时间（格式化）
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 选品日报</title>
        <style>
            body {{ font-family: sans-serif; background: #f4f7f6; padding: 20px; }}
            .card {{ background: white; border-radius: 8px; padding: 20px; max-width: 500px; margin: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .item {{ margin: 15px 0; }}
            .label {{ font-weight: bold; color: #7f8c8d; }}
            .footer {{ text-align: center; font-size: 12px; color: #bdc3c7; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚀 发现爆款潜力产品</h2>
            <div class="item"><span class="label">产品名称：</span>{report.get('product_name', '未知')}</div>
            <div class="item"><span class="label">趋势分析：</span>{report.get('trend_analysis', '暂无')}</div>
            <div class="item"><span class="label">风险评估：</span>{report.get('risk_assessment', '未知')}</div>
            <div class="item"><span class="label">推荐建议：</span>{report.get('recommendation', '暂无')}</div>
        </div>
        <div class="footer">报告生成时间: {now} (Gemini 2.5 系统)</div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    render_html()
