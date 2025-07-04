from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# טוען את קובץ .env
load_dotenv()

# הגדרות Cloudinary מהסביבה
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app = Flask(__name__)
CORS(app)  # לא להגביל ל־/api/* – פותח לכול

# מוסיף כותרות CORS לכל תגובה, כדי למנוע שגיאות מהדפדפן
@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,OPTIONS"
    return response

BASE_URL = "https://www.skidrowreloaded.com/page/{}/"

@app.route("/api/games")
def get_games():
    games = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, 35):
        url = BASE_URL.format(page)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        posts = soup.select("div.post")

        for post in posts:
            a_tag = post.select_one("h2 a")
            title = a_tag.text.strip()
            link = a_tag["href"]
            img_tag = post.select_one("div.post-excerpt a img")
            image_url = img_tag["src"] if img_tag and "logoo" not in img_tag["src"] else None

            if image_url:
                try:
                    # העלאה ישירות מ־URL דרך Cloudinary (type=fetch מהיר ובטוח)
                    res = cloudinary.uploader.upload(image_url, type="fetch")
                    cloud_image_url = res['secure_url']
                    games.append({"title": title, "link": link, "image": cloud_image_url})
                except Exception as e:
                    print(f"❌ Error uploading image: {e}")
                    continue

        if len(games) >= 300:
            break

    return jsonify(games)

if __name__ == "__main__":
    app.run(debug=True)
