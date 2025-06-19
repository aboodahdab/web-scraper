from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)


def get_links_and_headlines(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for a in soup.find_all("a", href=True):
            link = a['href']
            full_link = urljoin(url, link)

            # نحاول نحصل على عنوان داخل الرابط
            headline = a.get_text(strip=True)

            if headline:  # نتأكد انه مو فاضي
                articles.append({
                    "title": headline,
                    "link": full_link
                })

        return articles

    except Exception as e:
        return [{"title": "Error", "link": str(e)}]


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        url = request.form.get("url")
        results = get_links_and_headlines(url)
    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
