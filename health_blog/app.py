from flask import Flask, jsonify, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_articles():
    with open("articles.json", "r") as f:
        return json.load(f)

def save_articles(articles):
    with open("articles.json", "w") as f:
        json.dump(articles, f, indent=4)

@app.route("/api/articles")
def api_articles():
    return jsonify(load_articles())

@app.route("/")
def home():
    articles = load_articles()
    return render_template("index.html", articles=articles)


@app.route("/add", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        articles = load_articles()
        new_article = {
            "id": len(articles) + 1,
            "title": title,
            "content": content
        }
        articles.append(new_article)
        save_articles(articles)

        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/delete/<int:article_id>", methods=["POST"])
def delete_article(article_id):
    articles = load_articles()
    articles = [a for a in articles if a["id"] != article_id]


    for i, article in enumerate(articles, start=1):
        article["id"] = i

    save_articles(articles)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
