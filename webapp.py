from flask import Flask, render_template, request, redirect
from spoticloud import get_wordcloud, get_playlist


app = Flask(__name__, static_folder='static')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/playlist", methods=["POST"])
def playlist():
    playlist = request.form["playlist"]
    return redirect("/result?playlist=" + get_playlist(playlist).replace("https://open.spotify.com/playlist/", ""))


@app.route("/result")
def result():
    playlist = request.args.get("playlist")
    image = get_wordcloud(playlist)
    return render_template("result.html", playlist=playlist, image=image)


if __name__ == "__main__":
    app.run()