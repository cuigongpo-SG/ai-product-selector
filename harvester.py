import json
import os

def collect_data():
    # A. 获取你在 GitHub 界面输入的变量
    category = os.getenv('TARGET_CATEGORY', 'General')
    keywords = os.getenv('TARGET_KEYWORDS', '')

    print(f"🎯 正在执行选品指令：品类[{category}]，关键词[{keywords}]")

    # B. 模拟从 TikTok 和 Amazon 获取 Top 3 的数据 [cite: 34, 35]
    # 后续我们会在这里填充真正的 Playwright 爬虫逻辑
    raw_results = {
        "config": {"category": category, "keywords": keywords},
        "platform_data": [
            {
                "source": "TikTok", 
                "product": f"Viral {category} {keywords}".strip(), 
                "metric": "Trending (Simulated)"
            },
            {
                "source": "Amazon", 
                "product": f"Best Seller {category} {keywords}".strip(), 
                "metric": "High Sales (Simulated)"
            }
        ]
    }

    # C. 将抓取到的“原始数据”保存为 JSON 文件 [cite: 41]
    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(raw_results, f, ensure_ascii=False, indent=4)
    print("✅ 原始数据采集成功，已存入 raw_data.json")

if __name__ == "__main__":
    collect_data()
