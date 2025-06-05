from flask import Flask, render_template_string
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generate_placename import generate_common_placenames

app = Flask(__name__)


@app.route("/")
def home():
    placename = generate_common_placenames()
    html = """
    <html>
        <head><title>Random Placename Generator</title></head>
        <body>
            <h1>Random Placename</h1>
            <p style="font-size:2em;">{{ placename }}</p>
            <form method="get">
                <button type="submit">Generate Another</button>
            </form>
        </body>
    </html>
    """
    return render_template_string(html, placename=placename)


if __name__ == "__main__":
    app.run(debug=True)
