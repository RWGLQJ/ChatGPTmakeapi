from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

def get_weather(city):
    url = "https://api.woeo.net/API/other/weather/?city=" + city
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/weather', methods=['GET'])
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

if __name__ == '__main__':
    
    app.run()

