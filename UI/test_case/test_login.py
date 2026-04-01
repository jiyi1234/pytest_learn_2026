# UI/test_case/test_login.py
import pytest
from UI.pages.login_page import LoginPage
from UI.pages.base_page import BasePage

@pytest.mark.ui
@pytest.mark.forboe
class TestTikTokLoginByCookie:

    def test_tiktok_login_by_cookie(self, page):
        # 初始化页面
        login_page = LoginPage(page)
        # 执行cookie登录
        login_page.login_by_cookie()
        # 断言已经进入后台（验证登录成功）
        login_page.assert_url_contains("events_manager")
        login_page.wait_for_element("text=Connect data source")
        login_page.click_element("#main-root > div.Sidebar__Container-imbDkW.bCaiRK > div > div > div > span > div > button")
        login_page.wait_for_element("text=The first step to getting insights on customer interactions with your business, no matter where they happen.")
