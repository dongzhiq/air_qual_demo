import json
import urllib.parse
import urllib.request

# configure the app_key
app_key = "5c97a50ce3df34957ca18c1833bb3a6b"


class CityAQIRecord:

    def __init__(self, raw_record=None, main_city_name=None):

        if not raw_record:
            self.city_name = {}
            self.date_time = {}
            self.air_quality = {}
            self.details = {}
            return

        # Always assume raw_record is a normal record.
        cn_vals = [main_city_name, raw_record['city']]
        if None in cn_vals:
            cn_vals.remove(None)
        self.city_name = {key: val for key, val in zip(['cn', 'detail'], cn_vals)}

        dt_vals = raw_record['date'].split()
        self.date_time = {key: val for key, val in zip(['date', 'time'], dt_vals)}

        aq_keys = ['AQI', 'quality', 'PM2.5Hour', 'PM10Hour']
        self.air_quality = {key: raw_record[key] for key in aq_keys if (raw_record.get(key) is not None)}

        dtls_keys = ['lat', 'lon']
        self.details = {key: raw_record[key] for key in dtls_keys if (raw_record.get(key) is not None)}

        keys = ['city', 'date'] + aq_keys + dtls_keys
        self.details['others'] = {key: raw_record[key] for key in raw_record.keys() if (key not in keys)}


class CityAQI:

    def __init__(self, c_n):
        self.city_name = ''
        self.latest_rec = CityAQIRecord()   # A blank record
        self.recent_rec = {}
        self.detailed_latest_rec = {}
        self.error_description = ''
        self.update(c_n)

    def update(self, c_n):
        # It is sure that c_n is a str object; check if c_n (city name) is blank.
        # It is okay for the API request to have a blank city_name; however it would save some counts by checking this.
        if not c_n.strip():
            self.error_description = 'City name should not be blank.'
            return
        self.error_description, data = request_city_aqi(c_n.strip(), app_key)   # Obtain data and error description.
        if not data:    # There must be some error, which could be obtained via self.error_description
            return

        data_tmp = data['citynow']
        cn_now = data_tmp['city']           # Current city name in Chinese
        dt_now = data_tmp['date']           # Latest update time

        self.city_name = cn_now
        self.latest_rec = CityAQIRecord(data_tmp)

        data_tmp = data['lastTwoWeeks']
        self.recent_rec = {rec['date']: CityAQIRecord(rec) for key, rec in data_tmp.items()}

        data_tmp = data['lastMoniData']
        for i in data_tmp:
            data_tmp[i].update({'date': dt_now})
        self.detailed_latest_rec = {rec['city']: CityAQIRecord(rec, cn_now) for key, rec in data_tmp.items()}


# Request city air quality index using API
def request_city_aqi(city, appkey):
    url = 'http://web.juhe.cn:8080/environment/air/cityair'
    city_key = {
        'city': city,   # Name of the city; e.g. '济南' or 'jinan'
        'key': appkey,  # APP Key
    }
    city_key = urllib.parse.urlencode(city_key)             # Generate the string 'city=jinan&key=appkey'
    try:
        # Request the record; returns a http.client.HTTPResponse obj
        f = urllib.request.urlopen('%s?%s' % (url, city_key))
    except Exception as error_code:
        return str(error_code), None    # In some cases urlopen could fail, e.g. no Internet connection
    else:
        content = f.read()                                      # HTTPResponse.read method
        res = json.loads(content)                               # Decode the JSON to Python
        if res:
            error_code = res['error_code']
            if error_code == 0:
                # res['result'] looks like [ {...} ] and the desired results are in the dict
                return 'Successful', res['result'][0]
            else:
                # print('%s:%s' % (res['error_code'], res['reason']))
                return (str(res['error_code']) + ':' + res['reason']), None                      #
        else:
            return 'Request API error.', None


if __name__ == '__main__':
    jn = CityAQI('jinan')
