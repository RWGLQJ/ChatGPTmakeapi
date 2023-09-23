from flask import Flask, request, jsonify
import requests
from selenium import webdriver

app = Flask(__name__)

def get_rendered_html(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print("使用Selenium模拟浏览器访问失败:", e)

@app.route('/api/get_info', methods=['GET'])
def get_info():
    up_id = request.args.get('up_id')
    url = f'https://space.bilibili.com/{up_id}'
    html_selenium = get_rendered_html(url)

    start_marker_1 = '"n-data-v space-fans">'
    end_marker_1 = '</p></div><!----><!----></div><'

    start_marker_2 = 'display: inline-block;">'
    end_marker_2 = '</span></a><a href='

    start_marker_3 = '</span><span class="n-num">'
    end_marker_3 = '</span></a><!----><a href='

    start_marker_4 = '="h-basic-spacing"><h4 title="'
    end_marker_4 = '" class="h-sign">'

    desired_text_2 = html_selenium.split(start_marker_2)[1].split(end_marker_2)[0]
    desired_text_1 = html_selenium.split(start_marker_1)[1].split(end_marker_1)[0]
    desired_text_3 = html_selenium.split(start_marker_3)[1].split(end_marker_3)[0]
    desired_text_4 = html_selenium.split(start_marker_4)[1].split(end_marker_4)[0]

    id = ''.join(desired_text_2.split())
    fensi = ''.join(desired_text_1.split())
    tougao = ''.join(desired_text_3.split())
    qianm = ''.join(desired_text_4.split())

    response = {
        "UP名称": id,
        "粉丝数": fensi,
        "投稿数": tougao,
        "签名": qianm
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()
