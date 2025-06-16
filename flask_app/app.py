from flask import Flask, render_template
from placenames.generate_placename import generate_common_placenames

app = Flask(__name__)


@app.route("/")
def home():
    placename = generate_common_placenames()
    return render_template("home.html", placename=placename)

if __name__ == "__main__":
    app.run(debug=True)
