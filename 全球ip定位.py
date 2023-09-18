from flask import Flask, request, jsonify
import geoip2.database
import requests

app = Flask(__name__)

# GeoLite2 数据库文件的路径
database_path = 'GeoLite2-City.mmdb'

# 高德地图逆地理编码API的URL
gaode_geocode_url = 'https://restapi.amap.com/v3/geocode/regeo'

# 高德地图开发者API Key
gaode_api_key = '40ebd68f25461c49eefc1102b2a096ed'

@app.route('/ip_quanqiu', methods=['GET'])
def ip_location():
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
    app.run()
