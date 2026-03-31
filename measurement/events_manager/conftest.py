import pytest
import requests
import json
from measurement.events_manager.constant import request_header
from conftest import log

@pytest.fixture(scope="function")
def pixel_func(server_ip_port, connect_boedb):
    class PixelFunc(object):

        def send_request(self, url, aadvid, request_body=None, data=None, method="GET", headers=None, page=1,
                         page_size=10, search_string=None, req_src = "events_manager"):
            server_ip, server_port, server_env = server_ip_port
            full_url = "http://" + server_ip + ":" + str(server_port) + "/i18n/events_manager/v2/api/custom_conversion/"
            param = {}
            if page is not None:
                param["page"] = page
            if page_size:
                param["page_size"] = page_size
            if search_string:
                param["search_string"] = search_string
            if aadvid:
                param["aadvid"] = aadvid
            if req_src:
                param["req_src"] = req_src

            param_str = '&'.join(f'{k}={v}' for k, v in param.items())
            full_url = full_url + url + "?" + param_str
            if headers:
                temp_headers = headers.copy()
            else:
                temp_headers = request_header
            temp_headers["x-tt-env"] = server_env
            log.info(f"Request headers: {temp_headers}")
            log.info(f"Request body: {data}")
            log.info(f"Request method: {method}")
            log.info(f"Request url: {full_url}")
            log.info(f"Request request_body: {request_body}")
            if method == "GET":
                response = requests.get(url=full_url, headers=temp_headers)
            else:
                response = requests.post(url=full_url, json=request_body, headers=temp_headers, data=data)

            resp_text = json.loads(response.text)
            formatted_resp = json.dumps(resp_text, indent=2, ensure_ascii=False)
            log_id = response.headers.get("x-log-id")
            log.info(f"Response text: {formatted_resp}")
            log.info(f"response header: {response.headers}")
            log.info(f"response log_id: {log_id}")
            return response, resp_text

        def handle_db_by_query(self,query,fetch=None):
            cnx, cur = connect_boedb
            try:
                cur.execute(query)
                if fetch is not None:
                    result = cur.fetchone()
                if fetch is None:
                    result = cur.fetchall()
                cnx.commit()
                return result
            finally:
                cnx.close()
                cur.close()

        def query_sql(self, code):
            if id is not None:
                query = f"select * from analytics_pixel where pixel_code='{code}'"
                log.info(f"query sql: {query}")
                result = self.handle_db_by_query(query)
                log.info(f"result sql: {result}")
                return result
            else:
                return "id is null"


    return PixelFunc()
