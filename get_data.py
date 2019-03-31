import json
import urllib.parse, urllib.request


def get_data():
    # configure the appkey
    appkey = "5c97a50ce3df34957ca18c1833bb3a6b"

    # 1.城市空气质量
    request_city_AQI(appkey, "GET")



# city air quality index
def request_city_AQI(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/cityair"
    params = {
        "city": "shanghai",  # 城市名称的中文名称或拼音，如：上海 或 shanghai
        "key": appkey,  # APP Key
    }
    params = {"city": "shanghai","key": appkey}
    params = urllib.parse.urlencode(params)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


if __name__ == '__main__':
    get_data()

