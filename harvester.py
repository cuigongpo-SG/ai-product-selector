import json, os, urllib.parse
from playwright.sync_api import sync_playwright

def collect_amazon_us_data():
    # 1. 严谨处理类目名称
    raw_category = os.getenv('TARGET_CATEGORY', 'press on nails').lower()
    encoded_category = urllib.parse.quote(raw_category)
    
    # 策略 A：直接搜索页（成功率最高，不易触发验证码）
    search_url = f"https://www.amazon.com/s?k={encoded_category}"
    # 策略 B：Bestsellers 页面（备用）
    bs_url = f"https://www.amazon.com/Best-Sellers/zgbs/search?_encoding=UTF8&field-keywords={encoded_category}"
    
    print(f"📡 正在尝试北美站目的地: {search_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 模拟真实的 Mac Chrome 浏览器指纹
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800},
            locale="en-US"
        )
        page = context.new_page()
        
        try:
            # 放弃 networkidle，改用更务实的 domcontentloaded
            page.goto(search_url, timeout=45000, wait_until="domcontentloaded")
            
            # 如果出现验证码，保存截图用于调试
            if "api-services-support@amazon.com" in page.content() or "captcha" in page.url.lower():
                print("⚠️ 触发了亚马逊验证码验证")
                page.screenshot(path="debug_captcha.png")
                # 尝试点击刷新或作为异常处理
                raise Exception("Blocked by CAPTCHA")

            # 等待搜索结果中的产品标题
            page.wait_for_selector('h2 span', timeout=15000)
            
            # 抓取前 5 个商品标题（扩大样本量供 AI 分析）
            titles = page.locator('h2 span').all_text_contents()[:5]
            
            product_list = [{"platform": "Amazon US", "title": t.strip()} for t in titles if len(t) > 10]
            
            output = {"status": "success", "market": "US", "data": product_list}
            print(f"✅ 成功采集到 {len(product_list)} 个北美站准确商品")

        except Exception as e:
            print(f"❌ 采集失败详细原因: {e}")
            page.screenshot(path="debug_error.png")
            output = {"status": "error", "message": str(e), "data": []}
        
        browser.close()

    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    collect_amazon_us_data()
