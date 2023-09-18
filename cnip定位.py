from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()
