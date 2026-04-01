# UI/pages/login_page.py
from UI.pages.base_page import BasePage
from constant import TIKTOK_COOKIES

class LoginPage(BasePage):

    # 只做一件事：注入cookie → 刷新 → 登录成功
    def login_by_cookie(self):
        # 1. 先打开任意页面
        self.page.goto("https://ads.tiktok.com/i18n/events_manager/datasource/list?aadvid=6757929450454646790", wait_until="commit")

        # 2. 添加cookie
        self.add_cookies(TIKTOK_COOKIES)

        # 3. 刷新页面 → 自动登录
        self.page.reload()

        # 4. 跳转到目标页面
        self.page.goto("https://ads.tiktok.com/i18n/events_manager/datasource/list?aadvid=6757929450454646790&open_from=ttam_nav")