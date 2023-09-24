import requests
from flask import Flask, jsonify
#http://localhost:5000/api/hot_videos

app = Flask(__name__)

def get_hot_videos():
    try:
        # 发送HTTP GET请求获取热播视频数据
        url = 'https://api.bilibili.com/x/web-interface/popular'
        response = requests.get(url)
        data = response.json()

        # 解析响应数据，提取热播视频信息（包括vb号）
        hot_videos = []
        for video in data['data']['list']:
            title = video['title']
            play_count = video['stat']['view']
            vb_number = video['bvid']
            hot_videos.append({'title': title, 'play_count': play_count, 'vb_number': vb_number})

        return jsonify({'hot_videos': hot_videos})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
