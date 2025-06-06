import asyncio
import pandas as pd
from urllib.parse import urlparse, quote
from playwright.async_api import async_playwright
import os
import random



CSV_FILE = "gov.csv"


class BingSearcher:
    def __init__(self, query):
        self.query = query
        self.encoded_search_query = quote(query)
        self.search_url = f'https://cn.bing.com/search?q={self.encoded_search_query}'
        self.result_url = None

    async def perform_search(self):
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            print(f"🔍 正在搜索: {self.query}")
            try:
               
                await page.goto(self.search_url)
                await page.wait_for_selector("li.b_algo h2 a", timeout=10000)

                results = await page.query_selector_all("li.b_algo h2 a")

                found = False
                for i in range(min(3, len(results))):
                    link = results[i]
                    result_url = await link.get_attribute("href")
                    print(f"⏳ 尝试第 {i + 1} 个结果: {result_url}")

                    if ".gov.cn" in result_url:
                        self.result_url = self.get_base_url(result_url)
                        print(f"✅ 找到政府网站: {self.result_url}")
                        found = True
                        break

                if not found:
                    self.result_url = None

            except Exception as e:
                print(f"❌ 搜索失败: {e}")
                self.result_url = "请求错误"

            await browser.close()

    def get_result_url(self):
        return self.result_url

    def get_base_url(self,url):
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"


# 全局锁，用于控制并发写入 
df_lock = asyncio.Lock()
df_global = None  # 用于缓存全局 DataFrame


async def process_row(name, semaphore, csv_file):
    global df_global

    async with semaphore:  # 控制最大并发数
        current_url = df_global.loc[df_global['name'] == name, 'url'].values[0]

        if pd.notna(current_url) and current_url.strip() and current_url is not None and current_url != "请求错误":
            print(f"⏭️ 已有有效 URL，跳过: {name}")
            return

        print(f"🔄 开始处理: {name}")
        query = f"{name}政府官网"
        searcher = BingSearcher(query)
        await searcher.perform_search()
        found_url = searcher.get_result_url()

        print(f"💾 已获取结果: {name} -> {found_url}\n")

        # 加锁写入文件
        async with df_lock:
            df_global.loc[df_global['name'] == name, 'url'] = found_url
            df_global.to_csv(csv_file, index=False, encoding='utf-8-sig')

        return


async def main():
    global df_global

    # 读取原始 CSV 文件
    df_global = pd.read_csv(CSV_FILE)
    if 'url' not in df_global.columns:
        df_global['url'] = ''

    # 设置最大并发数量（推荐 5~10）
    semaphore = asyncio.Semaphore(1)

    tasks = []
    for _, row in df_global.iterrows():
        name = row['name']
        task = process_row(name, semaphore, CSV_FILE)
        tasks.append(task)

    await asyncio.gather(*tasks)

    print("✅ 所有数据已处理完毕并保存。")



def filter_urls(path):

    """
    过滤掉重复的 URL，将重复的 URL 设置为 None
    """

    df = pd.read_csv(path, encoding='utf-8-sig')

    duplicate_urls = df['url'][df['url'].duplicated(keep=False)]  # 找到重复的 URL
    # print(f"检测到重复的 URL: {duplicate_urls.tolist()}")

    # 将重复的 URL 设置为 None
    df.loc[df['url'].isin(duplicate_urls), 'url'] = None
    
    # 保存修改后的 DataFrame
    df.to_csv(path, index=False, encoding='utf-8-sig')


def count(path):
    """
    统计 CSV 文件中有效的 URL 数量
    """
    df = pd.read_csv(path, encoding='utf-8-sig')
    valid_urls = df['url'].dropna().tolist()
    print(f"有效的 URL 数量: {len(valid_urls)}")
    return len(valid_urls)



if __name__ == "__main__":
    # asyncio.run(main())

    # filter_urls(CSV_FILE)

    count(CSV_FILE)