import requests
from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/bing-image')
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

if __name__ == '__main__':
    app.run(debug=True)
