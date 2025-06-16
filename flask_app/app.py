from flask import Flask, render_template, request
from placenames.generate_placename import generate_common_placenames, generate_rude_placename
import requests
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")  # Set this in your environment

def get_unsplash_image_url():
    if not UNSPLASH_ACCESS_KEY:
        # Fallback image if no API key is set
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": "english village",
        "orientation": "landscape",
        "client_id": UNSPLASH_ACCESS_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data["urls"]["regular"]
    except Exception:
        # Fallback image if API call fails
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"

@app.route("/")
def home():
    rude_places = request.args.get("rude_places") == "true"
    if rude_places:
        placename = generate_rude_placename()
    else:
        placename = generate_common_placenames()
    background_url = get_unsplash_image_url()
    return render_template("home.html", placename=placename, rude_places=rude_places, background_url=background_url)

if __name__ == "__main__":
    app.run(debug=True)
