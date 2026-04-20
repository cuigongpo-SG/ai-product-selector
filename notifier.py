import os
import requests

def send_tg_message():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    # 这里的链接我们将利用 GitHub Pages 的默认格式
    repo_name = os.getenv('GITHUB_REPOSITORY') # 格式为 "username/repo"
    user = repo_name.split('/')[0]
    project = repo_name.split('/')[1]
    report_url = f"https://{user}.github.io/{project}/"

    text = f"🚀 **AI 选品新发现！**\n\n最新的深度分析报告已生成，快去看看吧：\n👉 [点击查看完整网页报告]({report_url})"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    requests.post(url, json=payload)
    print("✅ Telegram 通知已发出")

if __name__ == "__main__":
    send_tg_message()
