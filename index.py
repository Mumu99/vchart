import requests
import time
import json
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# 微信公众号信息
APPID = 'wx37a18e9aa1adee48'
APPSECRET = '6a5c6ca4517d2e0f70628368d77eecf2'
# 和风天气 API Key
HEFENG_API_KEY = '23af373708bf4fd6bfb2d5ca5a456051'
# 用户的微信 openid
USER_OPENID = 'o_a2B6KhcAZV14TsVG6dlyxSS3BA'
# 城市代码，可在和风天气官网查询
CITY_CODE = 'Nanchang'


def get_access_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    response = requests.get(url)
    access_token = response.json().get('access_token')
    return access_token


def get_weather():
    url = f'https://devapi.qweather.com/v7/weather/now?location={CITY_CODE}&key={HEFENG_API_KEY}'
    response = requests.get(url)
    weather_data = response.json()
    now_weather = weather_data['now']
    weather_text = f"当前{now_weather['text']}，气温{now_weather['temp']}℃，体感温度{now_weather['feelsLike']}℃"
    return weather_text


def send_weather_message():
    access_token = get_access_token()
    weather_text = get_weather()
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    template_id = 'your_template_id'
    data = {
        "touser": USER_OPENID,
        "template_id": template_id,
        "data": {
            "weather": {
                "value": weather_text
            }
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 每天 8 点推送天气消息
    scheduler.add_job(send_weather_message, 'cron', hour=8)
    scheduler.start()