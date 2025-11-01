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
        return jsonify({"error": "Missing search"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    
    # Updated simple fallback product cards selector
    items = soup.find_all("a", class_="search-card-item")
    results = []

    for item in items[:10]:
        title = item.get("title") or "No title"
        image_tag = item.find("img")
        image = image_tag["src"] if image_tag and image_tag.get("src") else ""
        results.append({
            "title": title,
            "image": image
        })

    return jsonify(results)
if __name__ == "__main__":
    app.run()
