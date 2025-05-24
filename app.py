
from flask import Flask
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def homepage():
    try:
        return "<h1>✅ Xclusive Engine Live</h1><p>No errors.</p>", 200
    except Exception as e:
        import traceback
        return f"<h1>❌ Render Error</h1><pre>{traceback.format_exc()}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
