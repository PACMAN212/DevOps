from flask import Flask, jsonify, request, abort
import requests

urlhaus_url = "https://urlhaus-api.abuse.ch/v1/urls/recent/"

app = Flask(__name__)

@app.route("/")
def home():
    return "Ana yaprak. Hoş geldiniz! Gitmek istediğiniz veriye /malware/(sayı) yazarak gidebilirsiniz. Girilen sayı son açıklanan zararlı malware dosyalarının içeriğini göstermektedir."

@app.route("/query")
def query():
    query = request.args.get("q")
    if query in ["url", "host", "payload", "tag"]:
        url = urlhaus_url + "?query=" + query
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": response.text})
    else:
        return jsonify({"message": "Geçersiz sorgu parametresi. Lütfen şunlardan birini kullanın: url, host, payload, tag."})

@app.route("/malware/<int:n>")
def number(n):
    if n > 0:
        response = requests.get(urlhaus_url)
        if response.status_code == 200:
            data = response.json()
            urls = data['urls']
            last_n_urls = urls[-n:]
            return jsonify(last_n_urls)
        else:
            return jsonify({"error": response.text})
    else:
        return jsonify({"message": "Geçersiz sayı parametresi. Lütfen pozitif bir tamsayı kullanın."})

@app.route("/hoşgeldiniz")
def welcome():
    return "HOŞGELDİNİZ! Gitmek istediğiniz veriye /malware/(sayı) yazarak gidebilirsiniz. Girilen sayı son açıklanan zararlı malware dosyalarının içeriğini göstermektedir."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
