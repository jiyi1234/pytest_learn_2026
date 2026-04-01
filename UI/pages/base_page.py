# UI/pages/base_page.py
from playwright.sync_api import Page, expect
import re

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # 打开网址
    def open_url(self, url: str):
        self.page.goto(url)

    # 点击元素
    def click_element(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).click(timeout=timeout)

    # 输入文本
    def input_text(self, selector: str, text: str, timeout: int = 10000):
        self.page.locator(selector).fill(text, timeout=timeout)

    # 获取元素文本
    def get_element_text(self, selector: str) -> str:
        return self.page.locator(selector).text_content(timeout=10000)

    # 断言元素可见
    def assert_element_visible(self, selector: str, timeout: int = 10000):
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    # 断言元素文本
    def assert_element_text(self, selector: str, expected_text: str, timeout: int = 10000):
        expect(self.page.locator(selector)).to_have_text(expected_text, timeout=timeout)

    # 等待元素加载
    def wait_for_element(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).wait_for(timeout=timeout)

    def add_cookies(self, cookies):
        self.page.context.add_cookies(cookies)

    # -------------------- 断言 --------------------
    # 断言元素可见
    def assert_visible(self, selector):
        expect(self.page.locator(selector)).to_be_visible()

    # 断言元素不可见
    def assert_hidden(self, selector):
        expect(self.page.locator(selector)).to_be_hidden()

    # 断言包含文本
    def assert_contains_text(self, selector, text):
        expect(self.page.locator(selector)).to_contain_text(text)

    # 断言完全等于文本
    def assert_text(self, selector, text):
        expect(self.page.locator(selector)).to_have_text(text)

    # 断言URL包含
    def assert_url_contains(self, url_part):
        expect(self.page).to_have_url(re.compile(url_part))

    # 断言输入框值
    def assert_input_value(self, selector, value):
        expect(self.page.locator(selector)).to_have_value(value)