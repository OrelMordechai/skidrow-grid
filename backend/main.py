from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS  # 👈 חדש

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
BASE_URL = "https://www.skidrowreloaded.com/page/{}/"

@app.route("/api/games")
def get_games():
    games = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for page in range(1, 35):  # עד 30 עמודים או כל עוד צריך
        url = BASE_URL.format(page)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        posts = soup.select("div.post")

        for post in posts:
            a_tag = post.select_one("h2 a")
            title = a_tag.text.strip()
            link = a_tag["href"]
            img_tag = post.select_one("div.post-excerpt a img")
            image = img_tag["src"] if img_tag and "logoo" not in img_tag["src"] else None

            if image:
                games.append({"title": title, "link": link, "image": image})

        if len(games) >= 300:
            break

    return jsonify(games)

if __name__ == "__main__":
    app.run(debug=True)
