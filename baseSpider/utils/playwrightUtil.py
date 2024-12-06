from playwright.sync_api import sync_playwright

'''
import subprocess
from playwright.sync_api import sync_playwright

# 自动启动浏览器
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
debugging_port = "--remote-debugging-port=9999"
command = f"{chrome_path} {debugging_port}"
subprocess.Popen(command, shell=True)

# 使用 Playwright 连接浏览器
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9999")
    content = browser.contexts[0]
    page = content.new_page()
    page.goto('https://example.com')
    print(page.title())
    browser.close()
## 说明

此方法是playwright与本地浏览器以ws方式通信

可以绕过基本上大部分浏览器检测，因为这就是一个真正的浏览器

两种使用方式:

1. 每次运行程序之后先打开浏览器

> 1. 找到自己桌面chrome的快捷方式键
> 2. 点击属性
> 3. 在目标一栏的最后添加 --remote-debugging-port=9999 端口可自定义
> 4. ```
>    with sync_playwright() as p:
>    # 创建一个连接
>    browser = p.chromium.connect_over_cdp("http://localhost:9999")
>    content = browser.contexts[0]
>    page = content.new_page()
>    ```
> 5. 在上述page下进行浏览器操作即可

2. 不打开浏览器，自行打开
> 在程序中添加下面的代码即可
>```
>import subprocess
># 这个路径可以是Google浏览器的exe路径，也可以是快捷方式的路径
>chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
>debugging_port = "--remote-debugging-port=9999"
>
>command = f"{chrome_path} {debugging_port}"
>subprocess.Popen(command, shell=True)
>```
>之后就是
> ```
>    with sync_playwright() as p:
>    # 创建一个连接
>    browser = p.chromium.connect_over_cdp("http://localhost:9999")
>    content = browser.contexts[0]
>    page = content.new_page()
>    ```
> 在上述page下进行浏览器操作即可
> 
> __注意__:
> 此方法不可以在打开了普通版(非第一种情况)的浏览器使用

'''







stealth_path = 'stealth.min.js'


class PlaywrightUtil:
    def __init__(self, stealth_path=stealth_path, user_agent=None):

        self.stealth_path = stealth_path
        self.user_agent = user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        self.browser = None
        self.context = None
        self.page = None

    def start_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            chromium_sandbox=False,
            ignore_default_args=["--enable-automation"],
            channel="chrome",
        )
        self.context = self.browser.new_context(user_agent=self.user_agent)
        self.context.add_init_script(path=self.stealth_path)
        self.page = self.context.new_page()

    def goto(self, url):
        if not self.page:
            raise Exception("Browser not started. Call start_browser() first.")
        self.page.goto(url)

    def wait_for_timeout(self, timeout):
        if not self.page:
            raise Exception("Browser not started. Call start_browser() first.")
        self.page.wait_for_timeout(timeout)

    def close(self):
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


