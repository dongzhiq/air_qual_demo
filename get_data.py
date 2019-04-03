import json
import urllib.parse
import urllib.request
import copy
# configure the app_key
app_key = "5c97a50ce3df34957ca18c1833bb3a6b"


class CityAQIRecord:
    # city_name = {'ch': '', 'pinyin': '', 'detail': []}
    # date_time = {'date': '', 'time': ''}
    # air_quality = {'AQI': '', 'quality': '', 'PM2.5': '', 'PM10': ''}
    # details = {'lat': '', 'lon': '', 'others': []}

    def __init__(self, c_n=None, d_t=None, aq=None, det=None):

        self.city_name = {}
        self.date_time = {}
        self.air_quality = {}
        self.details = {}

        if c_n:
            self.city_name = {'ch': c_n[0]}
            if len(c_n) > 1:
                self.city_name['pinyin'], *self.city_name['detail'] = c_n[1:]

        if d_t:
            self.date_time = {'date': d_t[0]}
            if len(d_t) > 1:
                self.date_time['time'] = d_t[1]

        # always suppose that pm2.5 comes with pm10
        if aq:
            self.air_quality = {'AQI': aq[0], 'quality': aq[1]}
            if len(aq) > 2:
                self.air_quality.update({'PM2.5': aq[2], 'PM10': aq[3]})

        if det:
            self.details = {}
            self.details['lat'], self.details['lon'], *self.details['others'] = det[:]


class CityAQI:

    def __init__(self, c_n):
        self.city_name = {}
        self.latest_rec = CityAQIRecord()
        self.recent_rec = {}
        self.detailed_latest_rec = {}
        self.update(c_n)

    def update(self, c_n):
        if not c_n.strip():
            return None
        data = request_city_aqi(c_n.strip(), app_key, "GET")
        # data = {'citynow': {'city': '济南', 'AQI': '43', 'quality': '优', 'date': '2019-03-31 21:00'}, 'lastTwoWeeks': {'1': {'city': '济南', 'AQI': '137', 'quality': '轻度污染', 'date': '2019-03-03'}, '2': {'city': '济南', 'AQI': '113', 'quality': '轻度污染', 'date': '2019-03-04'}, '3': {'city': '济南', 'AQI': '148', 'quality': '轻度污染', 'date': '2019-03-05'}, '4': {'city': '济南', 'AQI': '92', 'quality': '良', 'date': '2019-03-06'}, '5': {'city': '济南', 'AQI': '69', 'quality': '良', 'date': '2019-03-07'}, '6': {'city': '济南', 'AQI': '78', 'quality': '良', 'date': '2019-03-08'}, '7': {'city': '济南', 'AQI': '97', 'quality': '良', 'date': '2019-03-09'}, '8': {'city': '济南', 'AQI': '136', 'quality': '轻度污染', 'date': '2019-03-10'}, '9': {'city': '济南', 'AQI': '69', 'quality': '良', 'date': '2019-03-11'}, '10': {'city': '济南', 'AQI': '52', 'quality': '良', 'date': '2019-03-12'}, '11': {'city': '济南', 'AQI': '73', 'quality': '良', 'date': '2019-03-13'}, '12': {'city': '济南', 'AQI': '63', 'quality': '良', 'date': '2019-03-14'}, '13': {'city': '济南', 'AQI': '83', 'quality': '良', 'date': '2019-03-15'}, '14': {'city': '济南', 'AQI': '95', 'quality': '良', 'date': '2019-03-16'}, '15': {'city': '济南', 'AQI': '91', 'quality': '良', 'date': '2019-03-17'}, '16': {'city': '济南', 'AQI': '89', 'quality': '良', 'date': '2019-03-18'}, '17': {'city': '济南', 'AQI': '65', 'quality': '良', 'date': '2019-03-19'}, '18': {'city': '济南', 'AQI': '95', 'quality': '良', 'date': '2019-03-20'}, '19': {'city': '济南', 'AQI': '49', 'quality': '优', 'date': '2019-03-21'}, '20': {'city': '济南', 'AQI': '72', 'quality': '良', 'date': '2019-03-22'}, '21': {'city': '济南', 'AQI': '49', 'quality': '优', 'date': '2019-03-23'}, '22': {'city': '济南', 'AQI': '98', 'quality': '良', 'date': '2019-03-24'}, '23': {'city': '济南', 'AQI': '102', 'quality': '轻度污染', 'date': '2019-03-25'}, '24': {'city': '济南', 'AQI': '96', 'quality': '良', 'date': '2019-03-26'}, '25': {'city': '济南', 'AQI': '135', 'quality': '轻度污染', 'date': '2019-03-27'}, '26': {'city': '济南', 'AQI': '80', 'quality': '良', 'date': '2019-03-28'}, '27': {'city': '济南', 'AQI': '123', 'quality': '轻度污染', 'date': '2019-03-29'}, '28': {'city': '济南', 'AQI': '56', 'quality': '良', 'date': '2019-03-30'}}, 'lastMoniData': {'1': {'city': '科干所', 'AQI': '50', 'America_AQI': '50', 'quality': '优', 'PM2.5Hour': '15', 'PM2.5Day': '15', 'PM10Hour': '50', 'lat': '36.6114', 'lon': '116.988'}, '2': {'city': '农科所', 'AQI': '42', 'America_AQI': '64', 'quality': '优', 'PM2.5Hour': '22', 'PM2.5Day': '22', 'PM10Hour': '42', 'lat': '36.67', 'lon': '116.93'}, '3': {'city': '开发区', 'AQI': '43', 'America_AQI': '80', 'quality': '优', 'PM2.5Hour': '30', 'PM2.5Day': '30', 'PM10Hour': '38', 'lat': '36.6739', 'lon': '117.114'}, '4': {'city': '济南化工厂', 'AQI': '36', 'America_AQI': '52', 'quality': '优', 'PM2.5Hour': '16', 'PM2.5Day': '16', 'PM10Hour': '35', 'lat': '', 'lon': ''}, '5': {'city': '省种子仓库', 'AQI': '44', 'America_AQI': '44', 'quality': '优', 'PM2.5Hour': '12', 'PM2.5Day': '12', 'PM10Hour': '44', 'lat': '36.6853', 'lon': '117.051'}, '6': {'city': '机床二厂', 'AQI': '38', 'America_AQI': '46', 'quality': '优', 'PM2.5Hour': '14', 'PM2.5Day': '14', 'PM10Hour': '38', 'lat': '36.6489', 'lon': '116.943'}, '7': {'city': '市监测站', 'AQI': '37', 'America_AQI': '40', 'quality': '优', 'PM2.5Hour': '12', 'PM2.5Day': '12', 'PM10Hour': '37', 'lat': '36.6622', 'lon': '117.049'}, '8': {'city': '长清党校', 'AQI': '52', 'America_AQI': '52', 'quality': '良', 'PM2.5Hour': '13', 'PM2.5Day': '13', 'PM10Hour': '54', 'lat': '', 'lon': ''}}}
        if not data:
            return None

        data_tmp = data['citynow']
        cn_ch = data_tmp['city']            # current city name in Chinese
        self.city_name = {'ch': cn_ch}
        dt_now = data_tmp['date'].split()   # latest record date-time

        cn_tmp = [cn_ch]
        dt_tmp, aq_tmp = dt_now, [data_tmp['AQI'], data_tmp['quality']]
        self.latest_rec = CityAQIRecord(cn_tmp, dt_tmp, aq_tmp)

        data_tmp = data['lastTwoWeeks']
        for i in data_tmp:
            dt_tmp, aq_tmp = data_tmp[i]['date'], [data_tmp[i]['AQI'], data_tmp[i]['quality']]
            self.recent_rec[dt_tmp] = CityAQIRecord(cn_tmp, dt_tmp, aq_tmp)

        data_tmp = data['lastMoniData']
        for i in data_tmp:
            cn_tmp = [cn_ch, ''] + [data_tmp[i]['city']]
            dt_tmp = dt_now
            aq_tmp = [data_tmp[i]['AQI'], data_tmp[i]['quality'], data_tmp[i]['PM2.5Hour'], data_tmp[i]['PM10Hour']]
            dtls_tmp = [data_tmp[i]['lat'], data_tmp[i]['lon']]
            self.detailed_latest_rec[data_tmp[i]['city']] = CityAQIRecord(cn_tmp, dt_tmp, aq_tmp, dtls_tmp)

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
