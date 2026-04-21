import json, os
from playwright.sync_api import sync_playwright

def collect_amazon_us_data():
    raw_category = os.getenv('TARGET_CATEGORY', 'beauty').lower()
    # 针对北美站进行 URL 编码
    category_path = raw_category.replace(' ', '-')
    
    # 我们尝试两种可能的 URL 格式
    target_url = f"https://www.amazon.com/Best-Sellers-{category_path}/zgbs/beauty"
    
    print(f"📡 目标目的地: {target_url}")

    with sync_playwright() as p:
        # 尝试使用真正的浏览器指纹
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale="en-US"
        )
        page = context.new_page()
        
        try:
            # 增加等待时间，并模拟人类行为
            page.goto(target_url, timeout=60000, wait_until="networkidle")
            
            # 这里的逻辑：如果遇到验证码，这个选择器就会超时
            # 我们把超时时间延长到 20 秒
            print("⏳ 正在等待商品列表渲染...")
            page.wait_for_selector('div[id^="gridItemRoot"]', timeout=20000)
            
            items = page.locator('div[id^="gridItemRoot"]').all()[:3]
            
            extracted_data = []
            for item in items:
                # 尝试更稳健的标题抓取方式
                title = item.locator('span').first.inner_text().strip()
                extracted_data.append({"platform": "Amazon US", "title": title})
            
            output = {"status": "success", "market": "US", "data": extracted_data}
            print(f"✅ 成功采集到 {len(extracted_data)} 个准确商品标题")

        except Exception as e:
            print(f"⚠️ 采集异常 (可能是触发了验证码): {e}")
            # 【重要】如果失败了，保存一张截图，这样你可以去 Actions 里的 Artifacts 查看
            page.screenshot(path="debug_screenshot.png")
            print("📸 已保存调试截图 debug_screenshot.png")
            output = {"status": "error", "message": "Amazon blocked or URL incorrect", "data": []}
        
        browser.close()

    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    collect_amazon_us_data()
