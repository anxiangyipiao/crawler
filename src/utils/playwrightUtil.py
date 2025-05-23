import asyncio
import os
import shutil
from playwright.async_api import async_playwright
import subprocess

# stealth.min.js 文件应与此脚本位于同一目录
STEALTH_PATH = os.path.join(os.path.dirname(__file__), 'stealth.min.js')

class PlaywrightUtil:
    def __init__(self, headless=True, proxy_server=None, user_agent=None, viewport_size=None, timeout=30000):
        """
        初始化 PlaywrightUtil。

        :param headless: 是否以无头模式运行浏览器。
        :param proxy_server: 代理服务器地址，例如 "http://localhost:8888"。
        :param user_agent: 自定义 User-Agent。
        :param viewport_size: 浏览器视口大小，例如 {"width": 1920, "height": 1080}。
        :param timeout: 默认超时时间（毫秒）。
        """
        self.headless = headless
        self.proxy_server = proxy_server
        self.user_agent = user_agent
        self.viewport_size = viewport_size or {"width": 1280, "height": 720} # 默认视口大小
        self.timeout = timeout
        self.browser = None
        self.playwright = None

    async def start_browser(self):
        """启动浏览器实例."""
        self.playwright = await async_playwright().start()
        browser_args = []
        if self.proxy_server:
            browser_args.append(f"--proxy-server={self.proxy_server}")

        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=browser_args
        )
        return self.browser

    async def new_page(self, new_context_options=None):
        """
        创建一个新的浏览器页面。

        :param new_context_options: 创建新上下文的选项，可以包含代理、User-Agent 等。
        :return: 新的 Page 对象。
        """
        if not self.browser:
            await self.start_browser()

        context_options = {
            "user_agent": self.user_agent,
            "viewport": self.viewport_size,
        }
        if new_context_options:
            context_options.update(new_context_options)
        
        # 如果在类级别设置了代理，并且没有在 new_context_options 中覆盖，则使用类级别的代理
        if self.proxy_server and "proxy" not in context_options:
            context_options["proxy"] = {"server": self.proxy_server}


        context = await self.browser.new_context(**context_options)
        
        # 应用 stealth.js
        await context.add_init_script(path=STEALTH_PATH)
        
        page = await context.new_page()
        await page.set_default_timeout(self.timeout)
        return page

    async def get_page_content(self, url, page=None, wait_until="load", wait_for_selector=None, wait_for_timeout=None):
        """
        获取指定 URL 的页面内容。

        :param url: 要访问的 URL。
        :param page: 可选，已存在的 Page 对象。如果未提供，将创建一个新页面。
        :param wait_until: 导航等待条件，例如 "load", "domcontentloaded", "networkidle"。
        :param wait_for_selector: 等待特定选择器出现的选择器字符串。
        :param wait_for_timeout: 等待选择器的超时时间（毫秒）。
        :return: 页面 HTML 内容。
        """
        close_page_after = False
        if page is None:
            page = await self.new_page()
            close_page_after = True

        try:
            await page.goto(url, wait_until=wait_until)
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector, timeout=wait_for_timeout or self.timeout)
            content = await page.content()
            return content
        finally:
            if close_page_after and page:
                await page.close()

    async def close_browser(self):
        """关闭浏览器实例和 Playwright 连接."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    @staticmethod
    def kill_chrome_processes():
        """杀死所有 Chrome 进程（Windows 特定）。"""
        try:
            if os.name == 'nt': # 只在 Windows 上执行
                subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("已尝试终止所有 Chrome 进程。")
        except Exception as e:
            print(f"终止 Chrome 进程时出错: {e}")

    @staticmethod
    def start_chrome_with_debugging(chrome_path=None, port=9222, user_data_dir=None):
        """
        以远程调试模式启动 Chrome。

        :param chrome_path: Chrome 可执行文件的路径。如果为 None，则尝试从常见位置查找。
        :param port: 远程调试端口。
        :param user_data_dir: 用户数据目录。如果为 None，则使用默认或临时目录。
        """
        if chrome_path is None:
            # 尝试在 Windows 的常见位置找到 Chrome
            possible_paths = [
                os.path.join(os.environ.get("ProgramFiles", ""), "Google\Chrome\Application\chrome.exe"),
                os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Google\Chrome\Application\chrome.exe"),
                os.path.join(os.environ.get("LocalAppData", ""), "Google\Chrome\Application\chrome.exe"),
            ]
            chrome_path = next((path for path in possible_paths if os.path.exists(path)), None)

        if not chrome_path or not os.path.exists(chrome_path):
            print(f"未找到 Chrome 可执行文件。请指定 chrome_path。")
            return

        command = [
            chrome_path,
            f"--remote-debugging-port={port}",
        ]
        if user_data_dir:
            command.append(f"--user-data-dir={user_data_dir}")
        
        print(f"正在启动 Chrome: {' '.join(command)}")
        try:
            subprocess.Popen(command)
            print(f"Chrome 已以远程调试模式启动在端口 {port}。")
            print(f"浏览器WebSocket端点 (用于 Playwright connect): ws://127.0.0.1:{port}/devtools/browser/...")
        except Exception as e:
            print(f"启动 Chrome 失败: {e}")


# 示例用法:
async def main():
    # 示例1: 基本用法
    util = PlaywrightUtil(headless=False) # 设置 headless=False 以便看到浏览器操作
    page = await util.new_page()
    await page.goto("https://www.baidu.com")
    print(await page.title())
    await page.screenshot(path="baidu.png")
    await util.close_browser()

    # 示例2: 使用代理和自定义 User-Agent
    # util_proxy = PlaywrightUtil(
    #     headless=False,
    #     proxy_server="http://your_proxy_server:port", # 替换为你的代理服务器
    #     user_agent="MyCustomBrowser/1.0"
    # )
    # page_proxy = await util_proxy.new_page()
    # try:
    #     await page_proxy.goto("https://httpbin.org/ip") # 测试代理是否生效
    #     print(await page_proxy.content())
    #     await page_proxy.goto("https://httpbin.org/user-agent") # 测试 User-Agent
    #     print(await page_proxy.content())
    # finally:
    #     await util_proxy.close_browser()

    # 示例3: 获取页面内容并等待特定元素
    # util_content = PlaywrightUtil(headless=True)
    # content = await util_content.get_page_content(
    #     "https://quotes.toscrape.com/",
    #     wait_for_selector="div.quote" # 等待第一个名言元素加载
    # )
    # print(f"获取到的内容长度: {len(content)}")
    # await util_content.close_browser()

    # 启动 Chrome 进行远程调试 (可选)
    # PlaywrightUtil.kill_chrome_processes() # 先关闭所有已有的 Chrome 实例
    # chrome_user_data = os.path.join(os.getcwd(), "chrome_dev_user_data")
    # if not os.path.exists(chrome_user_data):
    #     os.makedirs(chrome_user_data)
    # PlaywrightUtil.start_chrome_with_debugging(user_data_dir=chrome_user_data)
    # print("现在你可以使用 playwright.chromium.connect_over_cdp('ws://127.0.0.1:9222/devtools/browser/...') 来连接这个浏览器实例了。")


if __name__ == "__main__":
    # asyncio.run(main())
    # 注意: 如果在已经运行 asyncio 事件循环的环境中（如 Jupyter Notebook, Scrapy），
    # 直接调用 asyncio.run(main()) 可能会导致错误。
    # 你可能需要使用 await main() 或者其他适合你环境的异步执行方式。
    print("PlaywrightUtil 模块已加载。取消注释 main() 中的示例以运行。")
    print(f"Stealth.js 路径: {STEALTH_PATH}")
    if not os.path.exists(STEALTH_PATH):
        print(f"警告: stealth.min.js 未在预期路径找到: {STEALTH_PATH}")
