import pandas as pd
from urllib.parse import urlparse, quote
import os
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from DrissionPage import Chromium, ChromiumOptions
import requests

CSV_FILE = "hosps.csv"

# 检查是否不包含bohe dxy 相关关键词
blacklist = ['bohe', 'dxy', 'baidu','jd.','weixin','weibo','zhihu','baike','wiki','wikipedia','360','sogou','sohu','99','39','ccvo','qq.com']


class BingSearcher:

    def __init__(self, query):
        self.query = query
        self.encoded_search_query = quote(query)
        self.bing_search_url = f'https://cn.bing.com/search?&q={self.encoded_search_query}'
        self.baidu_srarch_url = f'https://www.baidu.com/s?tn=75144485_5_dg&ch=2&wd={self.encoded_search_query}%E5%AE%98%E7%BD%91&usm=4&ie=utf-8&base_query={self.encoded_search_query}&tag_key=%E5%AE%98%E7%BD%91'
        self.result_url = None

    def bing_perform_search(self):
        """使用DrissionPage进行必应搜索"""
        browser = None
        try:
            # 为每个搜索创建完全独立的浏览器实例
            co = ChromiumOptions()
            co.incognito()
            co.no_imgs(True).mute(True)
            co.headless()  # 使用无头模式避免GUI冲突
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-dev-shm-usage')
            co.set_argument('--disable-blink-features=AutomationControlled')
            # 为每个实例分配不同的用户数据目录
            import tempfile
            temp_dir = tempfile.mkdtemp()
            co.set_argument(f'--user-data-dir={temp_dir}')
            
            browser = Chromium(co)
            page = browser.latest_tab
            
            print(f"🔍 正在搜索: {self.query}")
            
            # 访问搜索URL
            page.get(self.bing_search_url, timeout=15)
            
            # 等待页面加载
            time.sleep(random.uniform(2, 4))
            
            # 查找搜索结果
            results = page.eles('css:li.b_algo h2 a', timeout=10)
            
            if not results:
                print(f"❌ 未找到搜索结果")
                self.result_url = None
                return
            
            found = False
            for i, link in enumerate(results[:10]):  # 只检查前3个结果
                try:
                    result_url = link.attr('href')
                    if result_url:
                        print(f"⏳ 尝试第 {i + 1} 个结果: {result_url}")
                        
                        if not any(kw in result_url for kw in blacklist):
                            self.result_url = self.get_base_url(result_url)
                            print(f"✅ 找到医院网站: {self.result_url}")
                            found = True
                            break
                        else:
                            # 如果没有明显的医院关键词，也保存第一个结果作为备选
                            if i == 0:
                                self.result_url = self.get_base_url(result_url)
                                print(f"📝 保存第一个结果: {self.result_url}")
                                found = True
                except Exception as e:
                    print(f"⚠️ 处理链接时出错: {e}")
                    continue
            
            if not found:
                self.result_url = None
                print(f"❌ 未找到合适的网站")
                
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            self.result_url = "请求错误"
        finally:
            # 确保浏览器正确关闭
            if browser:
                try:
                    browser.quit()
                    # 清理临时目录
                    import shutil
                    if 'temp_dir' in locals():
                        try:
                            shutil.rmtree(temp_dir, ignore_errors=True)
                        except:
                            pass
                except Exception as cleanup_error:
                    print(f"⚠️ 清理浏览器时出错: {cleanup_error}")

    def baidu_perform_search(self):
        """使用DrissionPage进行百度搜索"""
        browser = None
        try:
            # 为每个搜索创建完全独立的浏览器实例
            co = ChromiumOptions()
            co.incognito()
            co.no_imgs(True).mute(True)
            co.headless()  # 使用无头模式避免GUI冲突
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-dev-shm-usage')
            # 为每个实例分配不同的用户数据目录
            import tempfile
            temp_dir = tempfile.mkdtemp()
            co.set_argument(f'--user-data-dir={temp_dir}')
            
            browser = Chromium(co)
            page = browser.latest_tab
            
            print(f"🔍 正在搜索: {self.query}")
            
            # 访问搜索URL
            page.get(self.baidu_srarch_url, timeout=15)
            
            # 等待页面加载
            time.sleep(random.uniform(2, 4))
            
            # 查找搜索结果
            results = page.eles('css:.result.c-container h3 a', timeout=10)
            
            if not results:
                print(f"❌ 未找到搜索结果")
                self.result_url = None
                return
            
            found = False
            for i, link in enumerate(results[:1]):  # 只检查前3个结果
                try:
                    result_url = link.attr('href')
                    if result_url:
                        print(f"⏳ 尝试第 {i + 1} 个结果: {result_url}")
                        
                        # 处理百度重定向链接
                        real_url = self.resolve_baidu_redirect(result_url)

                        if not any(kw in real_url for kw in blacklist):
                            self.result_url = self.get_base_url(real_url)
                            print(f"✅ 找到医院网站: {self.result_url}")
                            found = True
                            break
                        else:
                            found = False

                except Exception as e:
                    print(f"⚠️ 处理链接时出错: {e}")
                    continue
            
            if not found:
                self.result_url = None
                print(f"❌ 未找到合适的网站")
                
        except Exception as e:
            print(f"❌ 搜索失败: {e}")

    def get_result_url(self):
        return self.result_url

    def get_base_url(self, url):
        try:
            parsed_url = urlparse(url)
            return f"{parsed_url.scheme}://{parsed_url.netloc}"
        except:
            return url

    def resolve_baidu_redirect(self, baidu_url):
        """解析百度重定向链接，获取真实URL"""
        try:
            if 'baidu.com/link' not in baidu_url:
                # 如果不是百度重定向链接，直接返回
                return baidu_url
            
            print(f"🔄 解析百度重定向: {baidu_url}")
            
            # 使用requests请求百度重定向链接
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 设置不自动跟随重定向，手动处理
            response = requests.get(baidu_url, headers=headers, allow_redirects=False, timeout=10)
            
            # 检查是否有重定向
            if response.status_code in [301, 302, 303, 307, 308]:
                real_url = response.headers.get('Location')
                if real_url:
                    print(f"✅ 获取真实URL: {real_url}")
                    return real_url
            
            # 如果没有重定向，尝试解析响应内容中的URL
            if response.status_code == 200:
                content = response.text
                # 尝试从页面内容中提取真实URL
                import re
                url_pattern = r'URL=\'([^\']+)\''
                match = re.search(url_pattern, content)
                if match:
                    real_url = match.group(1)
                    print(f"✅ 从内容中提取URL: {real_url}")
                    return real_url
                    
                # 另一种提取方式
                url_pattern2 = r'window\.location\.replace\("([^"]+)"\)'
                match2 = re.search(url_pattern2, content)
                if match2:
                    real_url = match2.group(1)
                    print(f"✅ 从JS中提取URL: {real_url}")
                    return real_url
            
            print(f"⚠️ 无法解析重定向，返回原URL")
            return baidu_url
            
        except Exception as e:
            print(f"❌ 解析百度重定向失败: {e}")
            return baidu_url


# 线程锁
file_lock = threading.Lock()

def process_single_hospital(name, csv_file):
    """处理单个医院的搜索 - 修改为不传入共享的df"""
    try:
        # 在函数内部重新读取数据，避免共享DataFrame
        with file_lock:
            df = pd.read_csv(csv_file)
        
        # 检查是否已有有效URL
        hospital_row = df[df['name'] == name]
        if hospital_row.empty:
            print(f"❌ 未找到医院: {name}")
            return name, "未找到"
        
        current_url = hospital_row['url'].iloc[0]
        
        if pd.notna(current_url) and str(current_url).strip() and current_url != "请求错误":
            print(f"⏭️ 已有有效 URL，跳过: {name}")
            return name, current_url
        
        print(f"🔄 开始处理: {name}")
        
        # 搜索医院官网
        query = f'{name}'
        searcher = BingSearcher(query)
        searcher.baidu_perform_search()
        found_url = searcher.get_result_url()
        
        print(f"💾 已获取结果: {name} -> {found_url}")
        
        # 线程安全地更新CSV文件
        with file_lock:
            df = pd.read_csv(csv_file)  # 重新读取最新数据
            df.loc[df['name'] == name, 'url'] = found_url
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 添加随机延迟，避免请求过快
        time.sleep(random.uniform(1, 3))
        
        return name, found_url
        
    except Exception as e:
        print(f"❌ 处理 {name} 时出错: {e}")
        return name, "请求错误"

def main():
    """主函数"""
    # 读取原始CSV文件
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"❌ 文件 {CSV_FILE} 不存在")
        return
    
    if 'url' not in df.columns:
        df['url'] = ''
        df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
    
    # 获取需要处理的医院列表（只获取没有有效URL的）
    hospitals_to_process = []
    for _, row in df.iterrows():
        name = row['name']
        current_url = row.get('url', '')
        
        if pd.notna(name) and str(name).strip():
            # 只处理没有有效URL的医院
            if pd.isna(current_url) or not str(current_url).strip() or current_url == "请求错误":
                hospitals_to_process.append(name)
    
    print(f"📊 总共需要处理 {len(hospitals_to_process)} 家医院")
    
    if not hospitals_to_process:
        print("✅ 所有医院都已有URL，无需处理")
        return
    
    # 使用线程池进行并发处理 - 减少并发数避免资源冲突
    max_workers = 1  # 单线程，避免浏览器实例冲突
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务 - 不传入共享的DataFrame
        future_to_hospital = {
            executor.submit(process_single_hospital, name, CSV_FILE): name 
            for name in hospitals_to_process
        }
        
        completed = 0
        total = len(future_to_hospital)
        
        # 处理完成的任务
        for future in as_completed(future_to_hospital):
            hospital_name = future_to_hospital[future]
            try:
                name, url = future.result()
                completed += 1
                print(f"✅ 进度: {completed}/{total} - {name}")
                
                # 每完成10个任务显示一次详细进度
                if completed % 10 == 0:
                    print(f"📊 已完成 {completed}/{total} ({completed/total*100:.1f}%)")
                    
            except Exception as e:
                print(f"❌ 任务失败: {hospital_name} - {e}")
                completed += 1
    
    print("✅ 所有数据已处理完毕并保存。")

# 简化版本 - 单线程处理，避免所有并发问题
def main_single_thread():
    """单线程版本 - 更稳定"""
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"❌ 文件 {CSV_FILE} 不存在")
        return
    
    if 'url' not in df.columns:
        df['url'] = ''
    
    # 只处理没有有效URL的医院
    unprocessed_hospitals = []
    for _, row in df.iterrows():
        name = row['name']
        current_url = row.get('url', '')
        
        if pd.notna(name) and str(name).strip():
            if pd.isna(current_url) or not str(current_url).strip() or current_url == "请求错误":
                unprocessed_hospitals.append(name)
    
    total = len(unprocessed_hospitals)
    print(f"📊 需要处理 {total} 家医院")
    
    for i, name in enumerate(unprocessed_hospitals, 1):
        print(f"\n🔄 处理进度: {i}/{total} - {name}")
        
        try:
            # 搜索医院官网
            query = f'{name}官网'
            searcher = BingSearcher(query)
            searcher.baidu_perform_search()
            found_url = searcher.get_result_url()
            
            # 更新CSV文件
            df.loc[df['name'] == name, 'url'] = found_url
            df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
            
            print(f"💾 结果: {name} -> {found_url}")
            
            # 延迟
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"❌ 处理失败: {name} - {e}")
            df.loc[df['name'] == name, 'url'] = "请求错误"
            df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')

def filter_urls(path):
    """过滤重复和无效的URL"""
    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
        
        total_count = len(df)
        valid_before = df['url'].notna().sum()
        
        # 过滤重复URL（保留第一个）
        df.loc[df['url'].duplicated(keep='first'), 'url'] = None
        
        for keyword in blacklist:
            df.loc[df['url'].str.contains(keyword, na=False), 'url'] = None
        
        # 过滤请求错误
        df.loc[df['url'] == '请求错误', 'url'] = None
        
        df.to_csv(path, index=False, encoding='utf-8-sig')
        
        valid_after = df['url'].notna().sum()
        print(f"📊 过滤结果: {total_count}条记录，有效URL: {valid_before} -> {valid_after}")
        
    except Exception as e:
        print(f"❌ 过滤失败: {e}")

def count_valid_urls(path):
    """统计有效URL数量"""
    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
        valid_urls = df['url'].dropna()
        valid_count = len(valid_urls)
        total_count = len(df)
        
        print(f"📈 统计结果:")
        print(f"   总记录数: {total_count}")
        print(f"   有效URL数: {valid_count}")
        print(f"   完成率: {valid_count/total_count*100:.1f}%")
        
        # 显示一些样本
        if valid_count > 0:
            print(f"📋 样本结果:")
            sample_data = df[df['url'].notna()].head(5)
            for _, row in sample_data.iterrows():
                print(f"   {row['name']} -> {row['url']}")
        
        return valid_count
        
    except Exception as e:
        print(f"❌ 统计失败: {e}")
        return 0





if __name__ == "__main__":

    print("🚀 开始批量搜索医院官网...")
    
    # 使用单线程版本，更稳定
    main_single_thread()
    
    # # 过滤无效URL
    # print("\n🔧 开始过滤无效URL...")
    # filter_urls(CSV_FILE)
    
    # # 最终统计
    # print("\n📊 最终统计:")
    # count_valid_urls(CSV_FILE)
    
    # print("\n✅ 程序执行完毕!")