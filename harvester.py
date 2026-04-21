import json, os
from playwright.sync_api import sync_playwright

def collect_amazon_us_data():
    # 处理类目中的空格，将其转为亚马逊认可的格式
    raw_category = os.getenv('TARGET_CATEGORY', 'kitchen').lower()
    category = raw_category.replace(' ', '-')
    
    # 目的地：北美站准确路径
    target_url = f"https://www.amazon.com/Best-Sellers-{category}/zgbs/{category}"
    print(f"📡 正在接入北美站目的地: {target_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US"
        )
        page = context.new_page()
        
        try:
            page.goto(target_url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_selector('div[id^="gridItemRoot"]', timeout=10000)
            items = page.locator('div[id^="gridItemRoot"]').all()[:3]
            
            extracted_data = []
            for item in items:
                title = item.locator('div._cDE_v_title_3u94M').inner_text().strip()
                extracted_data.append({"platform": "Amazon US", "title": title})
            
            output = {"status": "success", "market": "US", "data": extracted_data}
            print(f"✅ 成功采集 {len(extracted_data)} 个产品")
        except Exception as e:
            print(f"❌ 采集出错: {e}")
            output = {"status": "error", "message": str(e)}
        
        browser.close()

    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    collect_amazon_us_data()
