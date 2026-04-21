import os, requests

def notify():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    repo = os.getenv('GITHUB_REPOSITORY') # "user/repo"
    
    # 严谨的 GitHub Pages 链接构建逻辑
    user, project = repo.split('/')
    report_url = f"https://{user}.github.io/{project}/"

    msg = f"🚀 **Amazon US 选品日报已生成**\n\nAI 已完成对北美市场的深度分析。\n👉 [点击查看网页报告]({report_url})"
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    notify()
