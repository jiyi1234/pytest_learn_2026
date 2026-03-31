import pytest

class TestCustomConversionList:

    @pytest.mark.forboe
    @pytest.mark.parametrize("aadvid",[1,75960823018])
    def test_custom_conversion_list(self, pixel_func, aadvid):
        url = "web/dataset/list"
        resp, resp_text = pixel_func.send_request(url=url,
                                                  aadvid=aadvid)
        if aadvid == 75960823018:
            assert resp.status_code == 200
            code = resp_text["data"]["event_source_list"][0]["event_source_id"]
            result = pixel_func.query_sql(code=str(code))
            assert len(result) == 1
            assert result[0]["id"] == 6987671487956123654
        else:
            assert resp.status_code == 401
            assert resp_text["code"] == 1400103


