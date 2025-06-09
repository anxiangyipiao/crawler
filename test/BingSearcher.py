import pandas as pd
import urllib.parse
from playwright.sync_api import sync_playwright
import time
import os

CSV_FILE = "gov.csv"


class BingSearcher:
    
    def __init__(self, query):
        self.query = query
        self.encoded_search_query = urllib.parse.quote(query)
        self.search_url = f'https://cn.bing.com/search?q={self.encoded_search_query}'
        self.result_url = None

    def perform_search(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            print(f"🔍 正在搜索: {self.query}")
            page.goto(self.search_url)

            try:
                # 等待第一个结果出现 
                page.wait_for_selector("li.b_algo h2 a", timeout=10000)
            except:
                print("❌ 页面加载超时或无结果")
                browser.close()
                return

            # 获取所有结果（最多取前3个）
            results = page.query_selector_all("li.b_algo h2 a")

            found = False
            for i in range(min(8, len(results))):
                link = results[i]
                result_url = link.get_attribute("href")
                print(f"⏳ 尝试第 {i + 1} 个结果: {result_url}")

                if ".gov.cn" in result_url and 'zwfw' not in result_url and 'dzsw' not in result_url.lower():
                        self.result_url = self.get_base_url(result_url)
                        print(f"✅ 找到政府网站: {self.result_url}")
                        found = True
                        break

            if not found:
                self.result_url = None
                print("❌ 未找到政府网站")

            browser.close()

        # time.sleep(1)  # 避免请求过快

    def get_result_url(self):

        return self.get_base_url(self.result_url) if self.result_url else None
    
    def get_base_url(self, url):
        """提取域名根路径"""
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"


# === 主程序逻辑 ===
if __name__ == "__main__":
    # 读取原始 CSV 文件
    df = pd.read_csv(CSV_FILE)

    # 如果没有 url 列，创建一个
    if 'url' not in df.columns:
        df['url'] = ''

    for index, row in df.iterrows():
        name = row['name']
        current_url = row['url']

        # 如果已有有效 URL，则跳过
        if pd.notna(current_url) and current_url is not None and current_url.strip():
            print(f"⏭️ 已有有效 URL，跳过: {name}")
            continue

        print(f"🔄 开始处理: {name}")


        search_name = name.replace("广西壮族自治区", "")

        # 构造查询词
        query = f"{search_name}政府"

        # 执行搜索
        searcher = BingSearcher(query)
        searcher.perform_search()
        found_url = searcher.get_result_url()

        # 更新当前行的 URL
        df.at[index, 'url'] = found_url

        # 🟢 实时保存：每次处理完一行就写回 CSV
        df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
        print(f"💾 已实时保存: {name} -> {found_url}\n")

    print("✅ 所有数据已处理完毕并保存。")