import json
import os

def render_html():
    try:
        with open('analysis_report.json', 'r', encoding='utf-8') as f:
            # 去掉 AI 可能返回的 Markdown 标记
            content = f.read().replace('```json', '').replace('```', '')
            data = json.loads(content)
    except Exception as e:
        print(f"渲染失败: {e}")
        return

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AI 选品日报</title>
        <style>
            body {{ font-family: sans-serif; background: #f4f7f6; padding: 20px; }}
            .card {{ background: white; border-radius: 8px; padding: 20px; max-width: 600px; margin: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .tag {{ display: inline-block; background: #3498db; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; }}
            .content {{ line-height: 1.6; color: #34495e; margin-top: 20px; }}
            .footer {{ text-align: center; font-size: 12px; color: #95a5a6; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 发现爆款潜力产品</h1>
            <div class="tag">深度 AI 分析报告</div>
            <div class="content">
                <p><strong>产品名称：</strong>{data.get('product_name', '未知')}</p>
                <p><strong>趋势分析：</strong>{data.get('trend_analysis', '暂无')}</p>
                <p><strong>风险评估：</strong>{data.get('risk_level', '未知')}</p>
                <p><strong>推荐建议：</strong>{data.get('recommendation', '暂无')}</p>
            </div>
            <div class="footer">报告生成时间：2026年 (Gemini 自动化系统)</div>
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("✅ 网页报告 index.html 已生成")

if __name__ == "__main__":
    render_html()
