import json
import urllib.parse
import urllib.request

# configure the app_key
app_key = "5c97a50ce3df34957ca18c1833bb3a6b"


class CityAQIRecord:
    city_name = {'ch': '', 'pinyin': '', 'detail': []}
    date_time = {'date': '', 'time': ''}
    air_quality = {'AQI': '', 'quality': '', 'PM2.5': '', 'PM10': ''}
    details = {'lat': '', 'lon': '', 'others': []}

    def __init__(self, c_n, d_t, aq, det = []):

        # always suppose that len(c_n) >= 2
        self.city_name['ch'], self.city_name['pinyin'], *self.city_name['detail'] = c_n

        self.date_time['date'] = d_t[0]
        if len(d_t) > 1:
            self.date_time['time'] = d_t[1]

        # always suppose that pm2.5 comes with pm10
        self.air_quality['AQI'], self.air_quality['quality'] = aq[0:2]
        if len(aq) > 2:
            self.air_quality['PM2.5'], self.air_quality['PM10'] = aq[2:4]

        if len(det) >= 2:
            self.details['lat'], self.details['lon'], *self.details['others'] = det


class CityAQI:
    city_name = None
    latest_rec = None
    recent_rec = {}
    detailed_latest_rec = {}

    def __init__(self, c_n):
        self.update(c_n)

    def update(self, c_n):
        assert c_n != ''
        data = request_city_aqi(c_n, app_key, "GET")
        assert data

        data_tmp = data['citynow']
        cn_ch = data_tmp['city']            # current city name in Chinese
        dt_now = data_tmp['date'].split()   # latest record date-time

        self.city_name = [cn_ch, '']

        dt_tmp, aq_tmp = dt_now, [data_tmp['AQI'], data_tmp['quality']]
        print('ln54', dt_tmp, aq_tmp)
        print(data_tmp)
        self.latest_rec = CityAQIRecord(self.city_name, dt_tmp, aq_tmp)
        print('ln57', self.latest_rec.city_name, self.latest_rec.date_time, self.latest_rec.air_quality)

        data_tmp = data['lastTwoWeeks']
        for i in data_tmp:
            dt_tmp, aq_tmp = data_tmp[i]['date'], [data_tmp[i]['AQI'], data_tmp[i]['quality']]
            self.recent_rec[dt_tmp] = CityAQIRecord(self.city_name, dt_tmp, aq_tmp)
            print('ln63', i, dt_tmp, self.latest_rec.city_name, self.latest_rec.date_time, self.latest_rec.air_quality)

        data_tmp = data['lastMoniData']
        for i in data_tmp:
            cn_tmp = self.city_name + [data_tmp[i]['city']]
            dt_tmp = dt_now
            aq_tmp = [data_tmp[i]['AQI'], data_tmp[i]['quality'], data_tmp[i]['PM2.5Hour'], data_tmp[i]['PM10Hour']]
            dtls_tmp = [data_tmp[i]['lat'], data_tmp[i]['lon']]
            self.detailed_latest_rec[data_tmp[i]['city']] = CityAQIRecord(cn_tmp, dt_tmp, aq_tmp, dtls_tmp)
            print('ln72', i, cn_tmp, self.latest_rec.city_name, self.latest_rec.date_time, self.latest_rec.air_quality)


# city air quality index
def request_city_aqi(city, appkey, m="GET"):
    url = "http://web.juhe.cn:8080/environment/air/cityair"
    # airCities cityair
    city_key = {
        "city": city,  # 城市名称的中文名称或拼音，如：上海 或 shanghai
        "key": appkey,  # APP Key
    }
    city_key = urllib.parse.urlencode(city_key)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, city_key))
    else:
        f = urllib.request.urlopen(url, city_key)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            # print(res["result"])
            return res["result"][0]
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return None
    else:
        print("request api error")
        return None


if __name__ == '__main__':
    jn = CityAQI('jinan')
    print(jn.city_name)
    print(jn.recent_rec)
    print(jn.latest_rec.city_name, jn.latest_rec.air_quality, jn.latest_rec.details, jn.latest_rec.date_time)
    print(jn.detailed_latest_rec)


