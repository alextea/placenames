from flask import Flask, render_template, request
from placenames.generate_placename import generate_common_placename, generate_rude_placename
import requests
import os

from dotenv import load_dotenv
import traceback
load_dotenv()

app = Flask(__name__)

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")  # Set this in your environment

def get_unsplash_image_url():
    if not UNSPLASH_ACCESS_KEY:
        # Fallback image and dummy credit if no API key is set
        return {
            "url": "https://images.unsplash.com/photo-1653230752943-6d6af552e547?auto=format&fit=crop&w=1200&q=80",
            "user_name": "Lāsma Artmane",
            "user_url": "https://unsplash.com/@lasmaa"
        }
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": "england village town",
        "orientation": "landscape",
        "client_id": UNSPLASH_ACCESS_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "url": data["urls"]["regular"],
            "user_name": data["user"]["name"],
            "user_url": data["user"]["links"]["html"]
        }
    except Exception:
        print("Error fetching image from Unsplash:")
        traceback.print_exc()
        return {
            "url": "https://images.unsplash.com/photo-1653230752943-6d6af552e547?auto=format&fit=crop&w=1200&q=80",
            "user_name": "Lāsma Artmane",
            "user_url": "https://unsplash.com/@lasmaa"
        }

@app.route("/")
def home():
    rude_places = request.args.get("rude_places") == "true"
    if rude_places:
        placename = generate_rude_placename()
    else:
        placename = generate_common_placename()
    image_data = get_unsplash_image_url()
    return render_template(
        "home.html",
        placename=placename,
        rude_places=rude_places,
        background_url=image_data["url"],
        unsplash_user_name=image_data["user_name"],
        unsplash_user_url=image_data["user_url"]
    )

if __name__ == "__main__":
    app.run(debug=True)
