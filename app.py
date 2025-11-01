from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    products = []

    for item in soup.select(".manhattan--container")[:10]:
        title = item.select_one(".manhattan--titleText")
        image = item.select_one("img")
        if title and image:
            products.append({
                "title": title.text.strip(),
                "image": image["src"] if "src" in image.attrs else "",
            })

    return jsonify(products)

if __name__ == "__main__":
    app.run()
