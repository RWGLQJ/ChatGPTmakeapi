from flask import Flask, jsonify
import datetime
import requests
from bs4 import BeautifulSoup
#http://localhost:5000/history/events

app = Flask(__name__)

@app.route('/history/events', methods=['GET'])
def get_historical_events():
    today = datetime.date.today()
    month = today.month
    day = today.day

    page_name = f"{month}月{day}日"
    url = f"https://baike.baidu.com/item/{page_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # 尝试找到包含历史事件的父元素或类名，并相应地进行调整
        content = soup.find(class_='lemma-summary')
        if content:
            events = [event.text for event in content.find_all('div', recursive=False)]
            return jsonify(events)
        else:
            return "Failed to fetch historical events: Content not found", 500
    else:
        return "Failed to fetch historical events: Request failed", 500

if __name__ == '__main__':
    app.run()
