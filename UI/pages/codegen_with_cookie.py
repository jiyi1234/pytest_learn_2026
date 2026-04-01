# codegen_with_cookie.py
from playwright.sync_api import sync_playwright
import json
from constant import TIKTOK_COOKIES

# 目标页面
URL = "https://ads.tiktok.com/i18n/events_manager/datasource/list?aadvid=6757929450454646790&open_from=ttam_nav"

with sync_playwright() as p:
    # 启动浏览器并开启 codegen 录制
    browser = p.chromium.launch(headless=False, args=["--remote-debugging-port=9223"])
    context = browser.new_context()

    # 注入Cookie
    context.add_cookies(TIKTOK_COOKIES)

    # 打开已登录页面
    page = context.new_page()
    page.goto(URL)

    # 启动 codegen 录制
    p.codegen.start_recording(context)

    # 保持打开
    input("已登录！现在你可以随便点页面，自动生成代码！按回车退出\n")