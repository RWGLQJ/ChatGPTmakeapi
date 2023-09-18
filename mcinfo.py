from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/mcs/<host>/<int:port>', methods=['GET'])
def get_minecraft_server_info(host, port):
    url = f"https://api.mcsrvstat.us/2/{host}:{port}"
    response = requests.get(url)

    if response.status_code == 200:
        server_info = response.json()
        
        # 从服务器信息中提取所需的信息
        version = server_info.get('version', 'N/A')
        players_online = server_info.get('players', {}).get('online', 0)
        max_players = server_info.get('players', {}).get('max', 0)
        motd = server_info.get('motd', {}).get('clean', 'N/A')
        
        # 构建包含所需信息的字典
        result = {
            'ip': host,
            'port': port,
            'version': version,
            'players_online': players_online,
            'max_players': max_players,
            'motd': motd
        }

        return jsonify(result)
    else:
        return jsonify({"error": "Unable to fetch server info"})

if __name__ == '__main__':
    app.run(debug=True)
