import requests
from selenium import webdriver

def get_rendered_html(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print("使用Selenium模拟浏览器访问失败:", e)

url = "https://www.bilibili.com/video/BV1M8411z7oz/" 


# 使用Selenium模拟浏览器访问获取完整渲染的内容
html_selenium = get_rendered_html(url)
print("使用Selenium模拟浏览器访问获取的完整渲染内容:")
print(html_selenium)

#with open("output.txt", "w", encoding="utf-8") as file:
 # file.write(html_selenium)

start_marker_1 = 'rollshow="true"><h1 title="'
end_marker_1 = '" class="video-title" dat'

start_marker_2 = '=""></svg>'
end_marker_2 = '</span><span class="dm item'

start_marker_3 = '</span><span class="dm item" data-v-3b903b56=""><svg class="dm-icon" style="width:20px;height:20px;" data-v-3b903b56=""></svg>'
end_marker_3 = '</span><span class="pubdate-ip item" data-v-3b'

start_marker_4 = 'pubdate" data-v-3b903b56=""><span class="pubdate-text" data-v-3b903b56="">'
end_marker_4 = '</span></span><!----></span><span class="copyright item" data-v-3b903b56=""><'

start_marker_5 = 'ike-info video-toolbar-item-text">'
end_marker_5 = '</span></div><!----></div><div class="toolbar-left-item-wrap" data-v'

start_marker_6 = 'an class="video-coin-info video-toolbar-item-text" data-v-36000414="">'
end_marker_6 = '</span></div><!----><!----></div><div class="toolbar-left-item-wrap" da'

start_marker_7 = 'info video-toolbar-item-text" data-v-edb4b09a="">'
end_marker_7 = '</span></div><!----><!----></div><div class="toolbar-left-item-wrap" data-v-2a'

start_marker_8 = '"video-share-info video-toolbar-item-text" data-v-c27fd710="">'
end_marker_8 = '</span></div></div></div><div class="triple-oldfan-entry" style="display:no'





desired_text_1 = html_selenium.split(start_marker_1)[1].split(end_marker_1)[0]
desired_text_2 = html_selenium.split(start_marker_2)[1].split(end_marker_2)[0]
desired_text_3 = html_selenium.split(start_marker_3)[1].split(end_marker_3)[0]
desired_text_4 = html_selenium.split(start_marker_4)[1].split(end_marker_4)[0]
desired_text_5 = html_selenium.split(start_marker_5)[1].split(end_marker_5)[0]
desired_text_6 = html_selenium.split(start_marker_6)[1].split(end_marker_6)[0]
desired_text_7 = html_selenium.split(start_marker_7)[1].split(end_marker_7)[0]
desired_text_8 = html_selenium.split(start_marker_8)[1].split(end_marker_8)[0]



title= ''.join(desired_text_1.split())
look= ''.join(desired_text_2.split())
barrage= ''.join(desired_text_3.split())
time= ''.join(desired_text_4.split())
zan= ''.join(desired_text_5.split())
bi= ''.join(desired_text_6.split())
shocang= ''.join(desired_text_7.split())
zhuanfa= ''.join(desired_text_8.split())


print("标题：" + title)
print("播放量：" + look)
print("弹幕数量：" + barrage)
print("发布时间：" + time)
print("点赞数：" + zan)
print("投币数：" + bi)
print("收藏量：" + shocang)
print("转发：" + zhuanfa)