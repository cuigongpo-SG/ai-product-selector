import json
import os
from playwright.sync_api import sync_playwright

def collect_data():
    # 获取类目变量，例如 'kitchen', 'beauty', 'electronics'
    category = os.getenv('TARGET_CATEGORY', 'kitchen').lower()
    
    # 目的地：明确指向亚马逊美国站 (Amazon.com)
    # 这里的链接结构是北美站 Bestsellers 的标准格式
    target_url = f"https://www.amazon.com/Best-Sellers-{category}/zgbs/{category}"
    
    print(f"📡 正在接入美国站目的地：{target_url}")

    with sync_playwright() as p:
        # 启动浏览器，设置语言为英文 (en-US)，确保抓取到的是原汁原味的美式英语标题
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            locale="en-US" 
        )
        page = context.new_page()
        
        try:
            # 访问美国站
            page.goto(target_url, timeout=60000, wait_until="networkidle")
            
            # 等待商品网格加载
            page.wait_for_selector('div[id^="gridItemRoot"]')

            # 抓取排名前 3 的商品
            items = page.locator('div[id^="gridItemRoot"]').all()[:3]
            
            product_list = []
            for index, item in enumerate(items):
                # 精准定位标题文字：亚马逊 Bestseller 标题通常在这个类名下
                # 使用 inner_text() 确保拿到的是干净的文字
                try:
                    title_element = item.locator('div._cDE_v_title_3u94M')
                    title_text = title_element.inner_text().strip()
                except:
                    title_text = "无法解析标题"

                product_list.append({
                    "rank": index + 1,
                    "platform": "Amazon US",
                    "product_title": title_text
                })
            
            # 封装成 AI 分析器喜欢的格式
            raw_results = {
                "market": "USA",
                "source": "Amazon.com",
                "category": category,
                "platform_data": product_list
            }
            print(f"✅ 成功抓取到 {len(product_list)} 条美国站准确数据")

        except Exception as e:
            print(f"❌ 采集过程出错: {e}")
            raw_results = {"error": "采集失败，请检查网络或 URL"}
        
        browser.close()

    # 存入原始数据文件
    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(raw_results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    collect_data()
