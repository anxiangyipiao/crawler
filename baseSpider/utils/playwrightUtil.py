from playwright.sync_api import sync_playwright



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


