from flask import Flask, render_template, redirect, request, url_for
from orm.setting import db
import string, random
from models.URL import URL
from flask_migrate import Migrate
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)
migrate = Migrate(app, db)


def generate_short_id(num_chars=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=num_chars))


def get_page_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title Found"
        return title.strip()
    except Exception:
        return "Error fetching title"


@app.route("/")
def index():
    return render_template("url/index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.form
    long_url = data.get("long_url")

    existing_url = db.session.query(URL).filter_by(long_url=long_url).first()
    if existing_url:
        return render_template(
            "URL/_generateURL.html",
            short_url=request.host_url + existing_url.short_id,
            description=existing_url.description,
            long_url=long_url,
        )

    description = get_page_title(long_url)

    short_id = generate_short_id()
    new_url = URL(short_id=short_id, long_url=long_url, description=description)

    db.session.add(new_url)
    db.session.commit()

    short_url = request.host_url + short_id
    return render_template(
        "url/_generateURL.html",
        short_url=short_url,
        description=description,
        long_url=long_url,
    )


@app.route("/<short_id>")
def redirect_to_long(short_id):
    url_entry = URL.query.filter_by(short_id=short_id).first()
    if url_entry and url_entry.enabled:
        return redirect(url_entry.long_url)
    return "URL Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
