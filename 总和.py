import requests
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from flask import Flask, request, jsonify
import datetime
from bs4 import BeautifulSoup
import geoip2.database
#http://localhost:5000/api/hot_videos
#http://localhost:5000/api/send_email?receiver_email=目标邮箱&sender_name=发信人名称&subject=标题&message=内容
#http://localhost:5000/api/history
#/api/weather
#b站热播
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
@app.route('/api/hot_videos', methods=['GET'])
def get_hot_videos():
    try:
        # 发送HTTP GET请求获取热播视频数据
        url = 'https://api.bilibili.com/x/web-interface/popular'
        response = requests.get(url)
        data = response.json()

        # 解析响应数据，提取热播视频信息
        hot_videos = []
        for video in data['data']['list']:
            title = video['title']
            play_count = video['stat']['view']
            hot_videos.append({'title': title, 'play_count': play_count})

        return jsonify({'hot_videos': hot_videos})

    except Exception as e:
        return jsonify({'error': str(e)})

#邮箱发信api
#email = Flask(__name__)
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 587
SENDER_EMAIL = 'yhtmailapi@qq.com'
SENDER_PASSWORD = 'psbhsxoyulcxdehg'

# 设置日志记录
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')

def create_message(receiver_email, sender_name, subject, message):
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), SENDER_EMAIL))
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    return msg

@app.route('/api/send_email', methods=['GET'])
def send_email():
    try:
        receiver_email = request.args.get('receiver_email')
        sender_name = request.args.get('sender_name')
        subject = request.args.get('subject')
        message = request.args.get('message')

        # 尝试获取 X-Forwarded-For 请求头字段
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        user_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.remote_addr
        
        msg = create_message(receiver_email, sender_name, subject, message)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        # 记录日志
        log_message = f"Email sent. IP: {user_ip}, " \
                      f"Receiver: {receiver_email}, " \
                      f"Sender Name: {sender_name}, " \
                      f"Subject: {subject}, " \
                      f"Message: {message}"
        logging.info(log_message)
		
        # 构建正确的 JSON 响应
        response = {
            'status': 'success',
            'data': {
                'receiver_email': receiver_email,
                'sender_name': sender_name,
                'subject': subject,
                'message_content': message,
                'user_ip': user_ip,
            },
            'message': 'Email sent successfully'
        }
        return jsonify(response)
    except Exception as e:
        # 记录错误日志
        error_message = f"Error sending email. IP: {user_ip}, " \
                        f"Error: {str(e)}"
        logging.error(error_message)

        # 返回错误消息的 JSON 响应
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)



#api = Flask(__name__)
@app.route('/api/text', methods=['GET'])
def get_text():
    text = {
        "text": [
            "/api/hot_videos",
            "/api/send_email?receiver_email=目标邮箱&sender_name=发信人名称&subject=标题&message=内容",            
            "/api/weather",
            "/api/bing-image",
            "/ip_location",
            "/ip_quanqiu"
        ]
    }
    return jsonify(text)
#天气    
def get_weather(city):
    url = "https://api.woeo.net/API/other/weather/?city=" + city
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/api/weather', methods=['GET'])
def weather_api():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': '请输入城市名'})
    
    weather_data = get_weather(city)
    
    if weather_data["code"] == 1:
        result = {
            'city': weather_data["data"]["city"],
            'temp': weather_data["data"]["tempn"] + "℃",
            'weather': weather_data["data"]["weather"],
            'wind': weather_data["data"]["wind"],
            'time': weather_data["data"]["time"]
        }
        
        if weather_data["data"]["warning"]:
            result['warning'] = weather_data["data"]["warning"]
        
        return jsonify(result)
    else:
        return jsonify({'error': '获取天气失败'})
        
        
@app.route('/api/bing-image')
def get_bing_image():
    format = request.args.get('format', 'image')
    if format == 'json':
        bing_api_url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
        response = requests.get(bing_api_url)
        image_obj = response.json()['images'][0]
        image_url = f"https://www.bing.com{image_obj['url']}"
        return {"image_url": image_url}
    else:
        bing_api_url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
        response = requests.get(bing_api_url)
        image_obj = response.json()['images'][0]
        image_url = f"https://www.bing.com{image_obj['url']}"
        image_response = requests.get(image_url)
        return Response(
            image_response.content,
            mimetype='image/jpeg',
            headers={'Content-Disposition': 'inline'}
        )

# 高德地图逆地理编码API的URL
gaode_geocode_url = 'https://restapi.amap.com/v3/ip'
# 高德地图地理编码API的URL
gaode_geocode_geo_url = 'https://restapi.amap.com/v3/geocode/geo'

# 高德地图开发者API Key
gaode_api_key = '40ebd68f25461c49eefc1102b2a096ed'

@app.route('/ip_location', methods=['GET'])
def ip_location():
    ip = request.args.get('ip', '')

    if not ip:
        return jsonify({'error': 'IP地址参数不能为空'}), 400

    try:
        query_params = {
            'key': gaode_api_key,
            'ip': ip
        }
        response = requests.get(gaode_geocode_url, params=query_params)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == '1':
                adcode = result['adcode']

                # 使用地理编码API获取更详细的地址信息和经纬度信息
                query_params_geo = {
                    'key': gaode_api_key,
                    'address': adcode,
                    'output': 'json'
                }
                response_geo = requests.get(gaode_geocode_geo_url, params=query_params_geo)
                if response_geo.status_code == 200:
                    result_geo = response_geo.json()
                    if result_geo['status'] == '1' and len(result_geo['geocodes']) > 0:
                        district = result_geo['geocodes'][0]['district']

                        # 获取经纬度信息
                        location_lnglat = result_geo['geocodes'][0]['location'].split(',')
                        longitude = location_lnglat[0]
                        latitude = location_lnglat[1]
                    else:
                        district = ''
                        longitude = ''
                        latitude = ''

                    province = result['province']
                    city = result['city']

                    location = {
                        'ip': ip,
                        'province': province,
                        'city': city,
                        'district': district,
                        'longitude': longitude,
                        'latitude': latitude
                    }
                    return jsonify(location), 200
                else:
                    return jsonify({'error': '请求高德地图地理编码API失败'}), 500
            else:
                return jsonify({'error': '无法获取IP地址的位置信息'}), 500
        else:
            return jsonify({'error': '请求高德地图API失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GeoLite2 数据库文件的路径
database_path = 'GeoLite2-City.mmdb'

# 高德地图逆地理编码API的URL
gaode_geocode_url = 'https://restapi.amap.com/v3/geocode/regeo'

# 高德地图开发者API Key
gaode_api_key = '40ebd68f25461c49eefc1102b2a096ed'

@app.route('/ip_quanqiu', methods=['GET'])
def ip_quanqiu():
    ip = request.args.get('ip', '')

    if not ip:
        return jsonify({'error': 'IP地址参数不能为空'}), 400

    try:
        reader = geoip2.database.Reader(database_path)
        response = reader.city(ip)

        location = {
            'ip': ip,
            'country': response.country.names.get('zh-CN', response.country.name),
            'city': response.city.names.get('zh-CN', response.city.name),
            'latitude': response.location.latitude,
            'longitude': response.location.longitude
        }

        # 使用高德地图逆地理编码API获取更高的位置信息
        query_params = {
            'key': gaode_api_key,
            'location': f'{response.location.longitude},{response.location.latitude}',
            'output': 'json',
            'radius': '1000',
            'extensions': 'all'
        }
        response = requests.get(gaode_geocode_url, params=query_params)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == '1':
                regeocode = result['regeocode']
                address = regeocode['formatted_address']
                location['address'] = address
                pois = regeocode['pois']
                if pois:
                    location['poi'] = pois[0]['name']
            else:
                return jsonify({'error': '无法获取更高的位置信息'}), 500
        else:
            return jsonify({'error': '请求高德地图API失败'}), 500

        return jsonify(location), 200
    except geoip2.errors.AddressNotFoundError:
        return jsonify({'error': '无法找到指定IP地址的地理位置信息'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    #api.run()
    app.run()
    #email.run()
    #today.run()