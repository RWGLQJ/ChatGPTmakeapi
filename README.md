![maven](https://img.shields.io/badge/python-3.11%2B-blue)
# ChatGPT制作的api接口
## 部署教程
* 下载仓库中的 requirements.txt运行以下内容
```
pip install -r requirements.txt
```
* 下载 总和.py在命令行运行：
```
py 总和.py
```
## 声明

此项目仅用于学习交流，请勿用于非法用途

## 代码说明
* 这是一个基于 Flask 框架的简单 API 代码，提供了以下几个功能：
* 获取 B 站热播视频列表接口：/api/hot_videos
* 使用 requests 库发送 HTTP GET 请求获取热播视频数据。
* 解析响应数据，提取热播视频的标题和播放量。
* 返回 JSON 格式的热播视频列表。
```
请求方法：GET
请求示例：
GET http://localhost:5000/api/hot_videos
```

## 发送邮件接口：/api/send_email
* 通过调用 smtplib 库实现发送邮件功能。
* 从请求参数中获取收件人邮箱、发信人名称、标题和内容，并创建包含邮件内容的 MIMEMultipart 对象。
* 使用 SMTP 服务器发送邮件，并记录日志。
* 返回 JSON 格式的发送结果。
```
请求方法:GET
请求参数：
  receiver_email：目标邮箱
  sender_name：发信人名称
  subject：标题
  message：内容
请求示例：
GET http://localhost:5000/api/send_email?receiver_email=example@example.com&sender_name=Sender&subject=Hello&message=Hello%20World
```
## 获取接口信息接口：/api/text
* 返回一段包含 API 接口路径的 JSON 文本。
```
请求方法：GET
请求示例：
GET http://localhost:5000/api/text
```
## 获取天气接口：/api/weather
* 通过调用第三方天气API获取指定城市的天气信息。
* 从请求参数中获取城市名。
* 返回 JSON 格式的天气信息。
```
请求方法：GET
请求参数：
  city：城市名
请求示例：
GET http://localhost:5000/api/weather?city=上海
```

## 获取必应每日图片接口：/api/bing-image
* 通过调用必应每日图片API获取当日的图片地址。
* 可以选择返回图片链接或直接返回图片文件。
```
请求方法：GET
请求参数：
  format：返回格式，默认为'image'，可选值为'image'或'json'
请求示例：
GET http://localhost:5000/api/bing-image?format=json
```
## IP 地址定位接口：/ip_location
* 通过调用高德地图API获取指定IP地址的地理位置信息。
* 从请求参数中获取 IP 地址。
* 返回 JSON 格式的定位信息。
```
请求方式：GET
请求参数：
  ip：IP 地址
请求示例：
GET http://localhost:5000/ip_location?ip=192.168.0.1
```
## IP 地址定位接口(全球)：/ip_quanqiu
* 通过调用高德地图API以及GeoLite2-City数据库获取指定IP地址的地理位置信息。
* 此接口需要GeoLite2-City数据库，自行前往https://dev.maxmind.com/geoip/docs/databases/city-and-country下载
* 从请求参数中获取 IP 地址。
* 返回 JSON 格式的定位信息。
```
请求方式：GET
请求参数：
  ip：IP 地址
请求示例：
GET http://localhost:5000/ip_location?ip=192.168.0.1
```
