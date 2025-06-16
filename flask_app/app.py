from flask import Flask, render_template, request
from placenames.generate_placename import generate_common_placenames, generate_rude_placename

app = Flask(__name__)


@app.route("/")
def home():
    rude_places = request.args.get("rude_places") == "true"
    if rude_places:
        placename = generate_rude_placename()
    else:
        placename = generate_common_placenames()
    return render_template("home.html", placename=placename, rude_places=rude_places)

if __name__ == "__main__":
    app.run(debug=True)
