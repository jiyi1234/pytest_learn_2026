import logging
import random
import subprocess
import os
import time

import pytest
import pymysql
import ipaddress
from constant import db

logging.basicConfig(filename='tests.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s%(pathname)s%(filename)s%(funcName)s[Line:%(lineno)d]-%(levelname)s:%(message)s')
log = logging.getLogger()

def is_ipv6(ip):
    try:
        ip = ipaddress.ip_address(ip)
        if ip.version == 6:
            return f"[{ip}]"
        return ip
    except ValueError:
        return "Invalid IP address"

def pytest_addoption(parser):
    parser.addoption('--ip', action='store', default="127.0.0.1",help="ip")
    parser.addoption('--port', action='store', default="3306",help="port")
    parser.addoption('--env', action='store', default="prod",help="env")

@pytest.fixture(scope='session', autouse=True)
def server_ip_port(request):
    default_ip = '127.0.0.1'
    default_port = 8000
    default_env = "prod"

    server_ip = request.config.getoption('--ip') or default_ip
    server_port = request.config.getoption('--port') or default_port
    server_env_tags = request.config.getoption('--env') or default_env

    server_ip = is_ipv6(server_ip)
    log.info(f"Server IP: {server_ip}")
    log.info(f"Server port: {server_port}")
    log.info(f"Server env tags: {server_env_tags}")
    return server_ip, server_port, server_env_tags

@pytest.fixture(scope='session', autouse=True)
def connect_boedb(request):
    cnx = pymysql.connect(
            host = str(db['host']),
            port = db['port'],
            user = db['user'],
            password = db['password'],
            database = db['database'],
            charset = "utf8",
            cursorclass = pymysql.cursors.DictCursor
    )
    cur = cnx.cursor()
    return cnx, cur

def pytest_sessionfinish(session, exitstatus):
    if exitstatus is not None:
        subprocess.run(["allure", "generate",
                        ".allure-results",
                        "-o", ".allure-report",
                        "--clean"],
                       check=True)

        #打开报告
        time.sleep(1.5)
        random_port = random.randint(50000, 65000)

        # ✅ 后台打开报告，不卡住 pytest
        subprocess.Popen(
            [
                "allure", "open",
                ".allure-report",
                "--port", str(random_port)
            ],
            # 不输出日志，不影响 pytest 结果
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )



